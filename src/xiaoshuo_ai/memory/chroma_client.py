"""Chroma 软记忆客户端（A 机算向量，B 机存储与检索）。"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

import requests

from xiaoshuo_ai.config import Settings
from xiaoshuo_ai.memory.embedding import EmbeddingProvider

COLLECTION_CHAPTER_SUMMARIES = "chapter_summaries"
COLLECTION_STYLE_SNIPPETS = "style_snippets"
COLLECTION_SCENE_MEMORY = "scene_memory"

HEARTBEAT_KEYS = ("heartbeat", "nanosecond heartbeat", "nanosecond_heartbeat")
DEFAULT_TENANT = "default_tenant"
DEFAULT_DATABASE = "default_database"
INCLUDE_FIELDS = ["documents", "metadatas", "distances"]


class ChromaMemoryClient:
    def __init__(self, settings: Settings, embedder: Optional[EmbeddingProvider] = None) -> None:
        self._settings = settings
        self._embedder = embedder
        self._client_cache = None

        # REST v2 base
        self._rest_base = f"http://{settings.chroma_host}:{settings.chroma_port}/api/v2"
        self._tenant = DEFAULT_TENANT
        self._database = DEFAULT_DATABASE

    # -------------------------
    # Low-level helpers
    # -------------------------
    def _client(self):
        if self._client_cache is not None:
            return self._client_cache

        try:
            import chromadb  # noqa: F401
        except Exception as exc:
            raise RuntimeError("chromadb 未安装或不可用（请 pip install chromadb）") from exc

        try:
            # chromadb 的 HttpClient 版本差异较大，这里尽量保持参数最少
            client = chromadb.HttpClient(
                host=self._settings.chroma_host,
                port=int(self._settings.chroma_port),
            )
        except Exception as exc:
            raise RuntimeError(f"Chroma HttpClient 连接失败：{type(exc).__name__}: {exc}") from exc

        self._client_cache = client
        return client

    def _json_or_text(self, response: requests.Response) -> Dict[str, Any]:
        if not response.text:
            return {}
        try:
            data = response.json()
            if isinstance(data, dict):
                return data
            return {"_json": data}
        except Exception:
            return {"_raw": response.text}

    def _rest_request(self, method: str, path: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self._rest_base}{path}"
        response = requests.request(
            method=method.upper(),
            url=url,
            json=payload,
            timeout=self._settings.healthcheck_timeout,
        )
        if response.status_code >= 400:
            detail = response.text[:500] if response.text else ""
            raise RuntimeError(f"Chroma REST 错误：HTTP {response.status_code} {detail}")
        return self._json_or_text(response)

    def _rest_get_collection(self, name: str) -> Optional[Dict[str, Any]]:
        # 注意：有的实现允许用 name 取 collection，有的只允许 id。
        # 若这里总是 404，_rest_create_collection(get_or_create=True) 也能兜底返回已存在的集合信息。
        url = (
            f"{self._rest_base}/tenants/{self._tenant}/databases/{self._database}"
            f"/collections/{name}"
        )
        response = requests.get(url, timeout=self._settings.healthcheck_timeout)
        if response.status_code == 404:
            return None
        if response.status_code >= 400:
            detail = response.text[:500] if response.text else ""
            raise RuntimeError(f"Chroma REST 错误：HTTP {response.status_code} {detail}")
        data = self._json_or_text(response)
        return data

    def _rest_create_collection(self, name: str) -> Dict[str, Any]:
        payload = {
            "name": name,
            "metadata": {"hnsw:space": "cosine"},
            "get_or_create": True,
        }
        return self._rest_request(
            "post",
            f"/tenants/{self._tenant}/databases/{self._database}/collections",
            payload,
        )

    def _extract_collection_id(self, info: Dict[str, Any]) -> Optional[str]:
        # 兼容不同返回结构：id / collection_id / collection:{id/...}
        for key in ("id", "collection_id"):
            v = info.get(key)
            if isinstance(v, str) and v:
                return v

        nested = info.get("collection")
        if isinstance(nested, dict):
            for key in ("id", "collection_id"):
                v = nested.get(key)
                if isinstance(v, str) and v:
                    return v
        return None

    def _rest_get_collection_id(self, name: str) -> str:
        info = self._rest_get_collection(name)
        if info is None:
            info = self._rest_create_collection(name)

        cid = self._extract_collection_id(info)
        if not cid:
            raise RuntimeError(f"Chroma 返回缺少 collection id：{info}")
        return cid

    # -------------------------
    # Public APIs
    # -------------------------
    def healthcheck(self) -> Any:
        url = f"http://{self._settings.chroma_host}:{self._settings.chroma_port}/api/v2/heartbeat"
        response = requests.get(url, timeout=self._settings.healthcheck_timeout)
        if response.status_code != 200:
            raise RuntimeError(f"Chroma 心跳失败：HTTP {response.status_code}")
        payload = response.json()
        heartbeat = None
        for key in HEARTBEAT_KEYS:
            if key in payload:
                heartbeat = payload[key]
                break
        if heartbeat is None:
            raise RuntimeError(f"Chroma 心跳字段缺失：{payload}")
        print(f"[Chroma] 通过：heartbeat={heartbeat}")
        return heartbeat

    def get_or_create_collection(self, name: str) -> Union[str, Any]:
        """
        返回：
        - 优先：chromadb collection 对象
        - fallback：REST collection_id（str）
        """
        try:
            client = self._client()
            try:
                return client.get_collection(name)
            except Exception:
                return client.create_collection(name=name, metadata={"hnsw:space": "cosine"})
        except Exception:
            return self._rest_get_collection_id(name)

    def delete_collection(self, name: str) -> None:
        # python client 优先
        try:
            client = self._client()
            try:
                client.delete_collection(name)
            except TypeError:
                client.delete_collection(name=name)
            return
        except Exception:
            pass

        # REST fallback：建议用 collection_id 删除
        cid = self._rest_get_collection_id(name)
        self._rest_request(
            "delete",
            f"/tenants/{self._tenant}/databases/{self._database}/collections/{cid}",
        )

    def upsert_texts(
        self,
        collection: str,
        ids: List[str],
        texts: List[str],
        metadatas: List[Dict[str, Any]],
        embeddings: Optional[List[List[float]]] = None,
    ) -> None:
        if not (len(ids) == len(texts) == len(metadatas)):
            raise ValueError("id/文本/元数据长度必须一致")

        if embeddings is None:
            if not self._embedder:
                raise RuntimeError("未提供向量计算器（embedder）")
            embeddings = self._embedder.embed_texts(texts)

        # python client path
        try:
            col = self.get_or_create_collection(collection)
            if not isinstance(col, str):
                if hasattr(col, "upsert"):
                    col.upsert(ids=ids, documents=texts, metadatas=metadatas, embeddings=embeddings)
                    return
                if hasattr(col, "add"):
                    try:
                        col.delete(ids=ids)
                    except Exception:
                        pass
                    col.add(ids=ids, documents=texts, metadatas=metadatas, embeddings=embeddings)
                    return
        except Exception:
            pass

        # REST fallback
        cid = self._rest_get_collection_id(collection)
        payload: Dict[str, Any] = {
            "ids": ids,
            "embeddings": embeddings,
            "metadatas": metadatas,
            "documents": texts,
        }
        self._rest_request(
            "post",
            f"/tenants/{self._tenant}/databases/{self._database}/collections/{cid}/upsert",
            payload,
        )

    def query_text(
        self,
        collection: str,
        query: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not self._embedder:
            raise RuntimeError("未提供向量计算器（embedder）")

        embedding = self._embedder.embed_texts([query])[0]

        # python client path
        try:
            col = self.get_or_create_collection(collection)
            if not isinstance(col, str) and hasattr(col, "query"):
                return col.query(
                    query_embeddings=[embedding],
                    n_results=n_results,
                    where=where,
                    include=INCLUDE_FIELDS,
                )
        except Exception:
            pass

        # REST fallback
        cid = self._rest_get_collection_id(collection)
        payload: Dict[str, Any] = {
            "query_embeddings": [embedding],
            "n_results": n_results,
            "where": where,
            "where_document": None,
            "include": INCLUDE_FIELDS,
        }
        return self._rest_request(
            "post",
            f"/tenants/{self._tenant}/databases/{self._database}/collections/{cid}/query",
            payload,
        )
