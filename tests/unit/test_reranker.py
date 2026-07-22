"""Reproduction tests for issue #34: missing LLM chunk re-ranking step.

These tests document the *feature gap*: today `rag/retriever/hybrid.py`
returns hybrid search results straight to the generator, with no
LLM-based relevance re-ranking, and `rag/retriever/reranker.py` does not
exist yet.

Run them with:

    pytest tests/unit/test_reranker.py -v

Current state (the reproduction):
  * ``test_reranker_module_does_not_exist_yet`` PASSES  -> proves the module
    is missing right now.
  * ``test_reranker_reorders_chunks_by_llm_relevance`` is XFAIL -> the desired
    behavior is not implemented, so it is expected to fail.

Once the reranker is implemented and wired in, the xfail test should start
passing (XPASS) and the "module does not exist" test should be deleted.
That flip from XFAIL -> XPASS is the signal that issue #34 is resolved.
"""

import importlib

import pytest


@pytest.mark.unit
class TestRerankerReproduction:
    """Reproduces the missing LLM re-ranking step (issue #34)."""

    def test_reranker_module_does_not_exist_yet(self) -> None:
        """Core reproduction: the module issue #34 asks us to build is missing.

        Importing ``rag.retriever.reranker`` currently raises
        ModuleNotFoundError. Delete this test once the module is created.
        """
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module("rag.retriever.reranker")

    @pytest.mark.xfail(
        reason="Issue #34: LLM re-ranking not implemented yet (reranker.py missing).",
        raises=(ModuleNotFoundError, ImportError, AttributeError, AssertionError),
        strict=True,
    )
    def test_reranker_reorders_chunks_by_llm_relevance(self) -> None:
        """Desired behavior: an LLM reranker re-sorts chunks by true relevance.

        The hybrid retriever can rank a keyword-heavy but off-topic chunk
        above the genuinely relevant one. An LLM reranker should promote the
        actually-relevant chunk to the top. This test defines that contract
        and will pass once ``reranker.py`` implements ``Reranker.rerank()``.
        """
        from rag.retriever.reranker import Reranker

        reranker = Reranker()

        query = "python web framework"
        # Chunk id=1 has a higher hybrid score but is off-topic;
        # chunk id=2 is the genuinely relevant answer.
        chunks = [
            {"id": 1, "text": "java spring boot enterprise application", "score": 0.9},
            {"id": 2, "text": "python django web framework tutorial", "score": 0.4},
        ]

        reranked = reranker.rerank(query, chunks, top_k=2)

        # After LLM re-ranking, the relevant chunk should be first.
        assert reranked[0]["id"] == 2
