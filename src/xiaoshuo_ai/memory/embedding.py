"""Embedding 计算器（A 机本地计算）。"""

from __future__ import annotations

from typing import Dict, List, Optional, Any


class EmbeddingProvider:
    """
    A 机本地计算向量：
    - 懒加载
    - 进程内缓存（同模型名只加载一次）
    - 输出可 JSON 序列化的 list[list[float]]
    """

    _model_cache: Dict[str, Any] = {}

    def __init__(self, model_name: str) -> None:
        self._model_name = model_name
        self._model: Optional[Any] = None

    def _load(self) -> None:
        if self._model is not None:
            return
        if self._model_name in self._model_cache:
            self._model = self._model_cache[self._model_name]
            return

        try:
            from sentence_transformers import SentenceTransformer
        except Exception as exc:
            raise RuntimeError(
                "sentence-transformers 未安装或不可用，请先 pip install sentence-transformers"
            ) from exc

        try:
            model = SentenceTransformer(self._model_name)
        except Exception as exc:
            raise RuntimeError(f"模型加载失败：{self._model_name}") from exc

        self._model_cache[self._model_name] = model
        self._model = model

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []

        self._load()
        assert self._model is not None

        vectors = self._model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        # numpy array / torch tensor -> python float list
        return [list(map(float, vec)) for vec in vectors]
