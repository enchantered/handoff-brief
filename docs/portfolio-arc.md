# Portfolio arc — adaptive, not a checklist

The twelve reference themes remain a useful map: Python/async foundations; LLM fundamentals; tool calling and structured outputs; memory/state; single-agent workflows; multi-agent orchestration; human approval; evaluation and QA; observability/tracing; security/guardrails; production deployment; and open-source/portfolio work. The portfolio will combine and reorder these themes when the evidence and engineering dependency justify it; a project does not complete a theme merely by naming it.

## Current progression

1. **Local retrieval and state:** Context Pocket explores source-linked, exact retrieval from user-selected text. It demonstrates deterministic parsing and readback, not semantic search, persistence or session capture.
2. **Checkable outputs:** Eval Gate exercises async foundations, structured result boundaries, metadata traces and adversarial fixtures without a live model call. It does not prove factual truth or provider reliability.
3. **Effect reliability:** Effect Ledger focuses on uncertain writes, receipts, idempotency boundaries and safe inspection before retry. A success-shaped response is not proof an external action completed.
4. **Human-curated handoff:** Handoff Brief packages explicit Markdown notes with bounded file access and source labels. It avoids building a general memory store or autonomous summarizer.

## Why this ordering changed

Several discussions describe cross-agent context loss, but mature substitutes (AGENTS.md, HANDOFF.md, notes, Git history, issue trackers) and direct commercial/open-source products are already present. Papers propose much broader portable memory/context lifecycles, and standards activity is still exploratory. Therefore this stage narrows *what crosses a boundary* before adding any agent or automation: the person selects source files, the program checks basic filesystem and size constraints, then the person reviews the result. The sequence moves human curation and data safety earlier than multi-agent orchestration. It is a useful engineering exercise, not proof of a unique venture opportunity.

## Not yet demonstrated

The projects remain independent local prototypes. No cross-project SDK, live LLM agent, remote service, continuous monitoring, release pipeline for production, customer deployment or paid product is claimed. Next stage selection depends on observing real user handoffs and seeing whether ordinary files are insufficient. If they are sufficient, leave the project small or stop rather than adding an interoperability protocol for its own sake.
