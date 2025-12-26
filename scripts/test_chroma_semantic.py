import argparse
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
# 兼容未做 pip install -e . 的场景：确保能 import src/ 下的包
sys.path.insert(0, str(REPO_ROOT / "src"))

from xiaoshuo_ai.config import load_settings
from xiaoshuo_ai.memory.chroma_client import (
    COLLECTION_CHAPTER_SUMMARIES,
    COLLECTION_SCENE_MEMORY,
    COLLECTION_STYLE_SNIPPETS,
    ChromaMemoryClient,
)
from xiaoshuo_ai.memory.embedding import EmbeddingProvider

EXIT_OK = 0
EXIT_CHROMA_FAIL = 31
EXIT_TOP1_FAIL = 32
EXIT_EMBED_FAIL = 33

TEST_DATA = {
    COLLECTION_CHAPTER_SUMMARIES: {
        "id": "test_ch_0001",
        "text": "第1章：林风在青云城被逐出家族，得到一枚黑色戒指，立誓逆袭。",
        "metadata": {
            "type": "chapter_summary",
            "chapter": 1,
            "char": "林风",
            "loc": "青云城",
            "test": True,
        },
        "query": "林风在青云城受辱被赶走，捡到戒指立志翻身",
    },
    COLLECTION_STYLE_SNIPPETS: {
        "id": "test_style_0001",
        "text": "他总爱先冷笑一声，再慢条斯理地补刀：‘就这？’（反差爽点+短句）",
        "metadata": {
            "type": "style_snippet",
            "tag": "冷笑补刀",
            "test": True,
        },
        "query": "先冷笑再嘲讽一句‘就这’这种口癖",
    },
    COLLECTION_SCENE_MEMORY: {
        "id": "test_scene_0001",
        "text": "夜雨里，旧巷灯影摇晃，青云城北门外的泥路上脚步声急促。",
        "metadata": {
            "type": "scene",
            "loc": "青云城北门",
            "weather": "雨",
            "test": True,
        },
        "query": "下雨的旧巷子和青云城北门外的泥路",
    },
}


def heartbeat_or_exit(settings) -> None:
    url = f"http://{settings.chroma_host}:{settings.chroma_port}/api/v2/heartbeat"
    try:
        resp = requests.get(url, timeout=settings.healthcheck_timeout)
        if resp.status_code != 200:
            print(f"[失败] Chroma 心跳失败：HTTP {resp.status_code}")
            sys.exit(EXIT_CHROMA_FAIL)
        payload = resp.json()
        heartbeat = (
            payload.get("heartbeat")
            or payload.get("nanosecond heartbeat")
            or payload.get("nanosecond_heartbeat")
        )
        if heartbeat is None:
            print(f"[失败] Chroma 心跳字段缺失：{payload}")
            sys.exit(EXIT_CHROMA_FAIL)
        print(f"[Chroma] 通过：heartbeat={heartbeat}")
    except Exception as exc:
        print(f"[失败] Chroma 心跳失败：{type(exc).__name__}: {exc}")
        sys.exit(EXIT_CHROMA_FAIL)


def maybe_reset(client: ChromaMemoryClient, reset: bool) -> None:
    if not reset:
        return
    for name in TEST_DATA.keys():
        try:
            client.delete_collection(name)
            print(f"[重置] 已删除集合 {name}")
        except Exception:
            print(f"[重置] 集合 {name} 不存在或无需删除")


def upsert_test_data(client: ChromaMemoryClient) -> None:
    for collection, item in TEST_DATA.items():
        client.upsert_texts(
            collection=collection,
            ids=[item["id"]],
            texts=[item["text"]],
            metadatas=[item["metadata"]],
        )
        print(f"[写入] 集合 {collection}: {item['id']}")


def _first_list(value, default=None):
    """
    兼容 chroma 返回结构差异：
    - [[...]] -> 取第一层
    - [...]   -> 原样
    - None    -> default
    """
    if value is None:
        return default if default is not None else []
    if isinstance(value, list) and value and isinstance(value[0], list):
        return value[0]
    if isinstance(value, list):
        return value
    return default if default is not None else []


def summarize_hit(ids, distances, documents) -> str:
    summary = []
    for idx in range(min(3, len(ids))):
        doc = documents[idx] if documents and idx < len(documents) else ""
        snippet = (doc[:60] + "...") if doc and len(doc) > 60 else doc
        dist = distances[idx] if distances and idx < len(distances) else None
        dist_str = f"{dist:.6f}" if isinstance(dist, (int, float)) else "NA"
        summary.append(f"{ids[idx]} | {dist_str} | {snippet}")
    return "\n".join(summary)


def verify_top1(client: ChromaMemoryClient) -> None:
    for collection, item in TEST_DATA.items():
        result = client.query_text(collection, item["query"], n_results=3)
        ids = _first_list(result.get("ids"))
        distances = _first_list(result.get("distances"))
        documents = _first_list(result.get("documents"))

        if not ids:
            print(f"[失败] 查询无结果：{collection}")
            sys.exit(EXIT_TOP1_FAIL)

        if ids[0] != item["id"]:
            print(f"[失败] 首位未命中：{collection}")
            print(f"  期望: {item['id']}")
            print(f"  实际: {ids[0]}")
            print(summarize_hit(ids, distances, documents))
            sys.exit(EXIT_TOP1_FAIL)

        print(f"[通过] 首位命中：{collection} -> {ids[0]}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Chroma 语义检索验收")
    parser.add_argument("--reset", action="store_true", help="删除测试集合并重建")
    args = parser.parse_args()

    settings = load_settings()

    # 1) 心跳（连通性）
    heartbeat_or_exit(settings)

    # 2) embedding 可用性（向量在 A 机算）
    try:
        embedder = EmbeddingProvider(settings.embed_model)
        embedder.embed_texts(["模型加载探测"])
    except Exception as exc:
        print(f"[失败] 向量模型不可用：{type(exc).__name__}: {exc}")
        return EXIT_EMBED_FAIL

    client = ChromaMemoryClient(settings, embedder=embedder)

    # （可选）reset
    maybe_reset(client, args.reset)

    # 3) 写入 + Top1 验证
    try:
        upsert_test_data(client)
        verify_top1(client)
    except SystemExit:
        raise
    except Exception as exc:
        print(f"[失败] 语义检索执行失败：{type(exc).__name__}: {exc}")
        return EXIT_TOP1_FAIL

    print("[通过] Chroma 语义检索验收（首位命中）")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
