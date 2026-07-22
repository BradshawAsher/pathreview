# Week 7 — Issue Selection

**Issue link:** https://github.com/ascherj/pathreview/issues/34

**Issue title:** Implement a re-ranking step that uses an LLM to score retrieved chunks before generation

**Tier:** ☐ Tier 1 ☐ Tier 2 ☑ Tier 3

## Problem Summary

Currently, the system relies solely on vector and keyword scores to rank retrieved document chunks, which may not always capture the nuance of semantic relevance to a user's query. This issue involves building a re-ranking layer that utilizes a smaller, efficient LLM to evaluate the relevance of these initial chunks before they are sent to the primary generator. A successful implementation will prune less relevant results, ultimately increasing the accuracy and quality of the context provided to the LLM. This work will primarily involve creating a new `reranker.py` module in the `rag/retriever/` directory and integrating it into the existing flow within `rag/retriever/hybrid.py`.

## Setup

- **Branch name:** `feat/34-llm-chunk-reranker`
- **Setup confirmation:** ☑ App runs locally at `localhost:5173`
- **Cohort ledger:** ☑ Issue added to cohort ledger

## "Is this right for me?" Checklist Reasoning

**Part 1 — Understanding the Issue:** I can clearly define the problem: the current system lacks a secondary relevance check after initial retrieval, leading to potentially noisy context. The expected behavior is that retrieved chunks will pass through an LLM re-ranker, which will score and filter them before the generator receives them.

**Part 2 — Tier Fit:** While this is a Tier 3 issue, it is a realistic match for my background in RAG architectures and Python engineering. I have already built full RAG pipelines, which provides the necessary foundation to navigate this architectural change safely.

**Part 3 — Codebase Readiness:** I have located `rag/retriever/hybrid.py` and identified where the integration point for the new `reranker.py` module belongs. I have reviewed the existing retrieval logic and feel confident that I can inject the re-ranking logic without destabilizing the current flow.

**Part 4 — Scope and Time:** The estimated effort is 7–10 hours. Given my familiarity with the codebase and the upcoming two-week window for implementation and testing, this is well within my capacity for the Week 9 deadline. There are no blockers or dependencies listed on the issue.


## Week 8 — Reproduction & Solution Planning

**Reproduction commit link:** https://github.com/BradshawAsher/pathreview/commit/046fb0f4677d29945c093bf1b6818ade6a097d46

**Reproduction commit branch link:** https://github.com/BradshawAsher/pathreview/tree/feat/34-llm-chunk-reranker

**Reproduction summary:**
Confirmed that `rag/retriever/hybrid.py` returns hybrid search results directly to the generator with no LLM re-ranking pass, and that `rag/retriever/reranker.py` does not exist (no `rerank` references anywhere in the codebase). Documented the gap with a reproduction test at `tests/unit/test_reranker.py`: one test passes because the reranker module is absent, and one `xfail` test defines the desired `rerank()` behavior. Running `pytest tests/unit/test_reranker.py -v` yields `1 passed, 1 xfailed`; the xfail will flip to xpass once the reranker is implemented.

**PLAN.md link:** https://github.com/BradshawAsher/pathreview/blob/feat/34-llm-chunk-reranker/PLAN.md

**Walkthrough video (recommended):** _Insert Loom link if recorded, or leave blank_

**Blockers or open questions:**
None at the moment — one open question is which model to configure for the re-ranking pass (a small/fast model to keep latency low).