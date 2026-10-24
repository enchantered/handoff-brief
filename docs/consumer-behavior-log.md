# Consumer and developer behavior log

Earlier dated portfolio observations from October 19–23 are preserved in the [public portfolio history](https://github.com/enchantered/effect-ledger/blob/main/docs/consumer-behavior-log.md). Continue this log by appending dated entries; earlier observations and their evidence limits should not be rewritten silently.

## 2026-10-24 — Developers keep asking how to carry project context

**Repeated problem signal, not prevalence:** a May Cursor Forum discussion, a broader GitHub Community discussion, and an October 23 Reddit question independently raise cross-tool or cross-session context continuity. The reports are self-selected and one is explicitly market research; they do not establish the frequency of failure or buyer demand. A maker showcase for an existing handoff CLI and October 24 Product Hunt listings for Context Engine and Inyon are counterevidence to novelty. Handoff scripts, `AGENTS.md`, Markdown status notes, Git history, and manual re-explanation are low-cost incumbents. The [dated decision](2026-10-24-decision.md) details dates, sources, survey scope, product maturity, papers and patents.

**AI-native versus established practice:** agents can be swapped or interrupted, but developers still use ordinary files, repo instructions, commits, tickets and human-edited handoff notes. A stable instruction file is useful but is not a current task-state record. The selected experiment therefore compiles only explicitly chosen local notes; it does not create autonomous or persistent memory.

**Dated signal and limit:** Stack Overflow's 2026 developer survey and current GitHub/AI-agent launches establish that AI tooling is widely discussed and used in developer workflows, while GitHub's usage-metrics change shows increasing attention to agent/skill/MCP observability. None measures handoff friction, usage of this particular project, demand in India, retention or willingness to pay. Most available consumer adoption research is not directly about software development; do not generalize developer anecdotes to general consumers.

**Decision and validation:** prototype one reproducible local Markdown packet with strict input bounds and source labels. Compare it with existing notes and competing handoff products in observed user tasks before adding integrations or automatic capture. No buyer interviews or paid tests have yet been conducted. Stop if ordinary files solve the problem for most target users.

**Run record:** 22 offline tests pass; compilation and the documented two-file CLI example pass. The example uses synthetic notes. See the decision for the exact feature, limitations, papers/patents and source links.

**Social-channel check (October 24):** two opened X posts reinforce that context continuity is part of current product marketing: Linear ties cross-functional context to Linear Agent, and Beacon promotes a cross-agent memory service. Both posts are product positioning/promotion, not independent user research; one reports a seed round, but financing is not demand for this project. See the [decision addendum](2026-10-24-decision.md#social-channel-check-october-24).

**Validation correction (final run):** after adding one regression for terminal escape sequences, the suite expanded from the earlier 22 to **23 passing tests**; compilation and the README two-file example still pass. This correction supersedes the earlier count in this entry.

**Memory-risk evidence:** TechCrunch's June 10 report links to two papers about user beliefs and memory affecting answer quality. One is an ICLR 2026 workshop evaluation of three memory tools; a second reports preference-related sycophancy in agentic financial tasks and tests input filtering. They are bounded research results, not prevalence evidence. They support keeping this prototype as an explicit file transport helper rather than automatically learning user preferences; even a reviewed handoff can transmit wrong or malicious content. [Decision sources](2026-10-24-decision.md#research-update-memory-can-mislead-as-well-as-help).
