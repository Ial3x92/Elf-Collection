---
name: related-project-add
description: Add, update, or reindex related projects and documentation sources into related-projects with a deep summary markdown and synchronized .claude/MEMORY.md entry.
context: fork
---

# Related Project Add

Use this skill when the user asks to ingest a new external source or refresh an existing one for development knowledge.

This skill supports three source classes:

1. Git repositories.
2. Documentation/wiki pages.
3. Raw markdown/html reference sources.

The skill always produces three outputs:

1. Source artifact folder at `related-projects/{raw_source}/`.
2. Deep summary file at `related-projects/{raw_source}.md`.
3. Memory update in `.claude/MEMORY.md` under `Related Projects Knowledge Base`.

The expected quality bar is a durable technical reference, not a lightweight overview.
For implementation-heavy sources, the summary must be detailed enough that future work can proceed from the markdown without rescanning the entire upstream source tree unless verification is needed.

## Naming Rules

1. Derive `raw_source` from the canonical source name.
2. Normalize to lowercase slug with dashes.
3. Use the same slug for folder and summary file base name.
4. If a legacy mixed-case summary exists, migrate to slugified naming when safe and keep links updated.

Examples:

- `ShadowMountPlus` -> `shadowmountplus`
- `PS5 FPKG Wiki` -> `ps5-fpkg-wiki`

## Trigger Conditions

Use this skill when user intent includes any of the following:

- Add related project.
- Reindex related project.
- Build/update knowledge base from external repo/docs.
- Convert research into related-projects markdown plus memory entry.

Do not use this skill for isolated code fixes inside `src/` unless the request explicitly includes external-source ingestion.

## Phase 1: Intake and Scope

Collect and normalize these inputs:

1. Source URLs.
2. Source type: `git` or `docs`.
3. Topic focus (for relevance filtering).
4. Optional draft summary provided by user.
5. Optional explicit slug override.

Decision logic:

1. If the source is a git repo, use submodule flow.
2. If the source is docs/wiki/html/md, use snapshot flow.
3. If mixed sources are provided, process all and merge into one summary if they represent a single topic.

## Phase 2: Acquire Source Artifacts

### A) Git repository flow

1. Ensure `.gitignore` allows:
   - `related-projects/{raw_source}`
   - `related-projects/*.md`
2. Resolve the upstream repository default branch before adding or updating the submodule.
3. Add or update submodule at:
   - `related-projects/{raw_source}`
4. When adding a new submodule:
   - Add it with the upstream default branch recorded in `.gitmodules`.
   - Immediately initialize nested submodules recursively so the local artifact folder is complete.
   - Preferred command pattern:
     - `git submodule add -b {default_branch} {repo_url} related-projects/{raw_source}`
     - `git submodule update --init --recursive related-projects/{raw_source}`
5. After adding or updating a git submodule, ensure the top-level `.gitmodules` entry includes:
   - `branch = {default_branch}`
6. If already present:
   - Fetch latest refs if reindex requested.
   - Update recursively so nested submodules are present.
   - Keep submodule pinned to explicit commit unless user asks for newest HEAD.
   - When the user asks to track the latest upstream state, use the configured default branch and recurse into nested submodules.

### B) Documentation/wiki/html/md flow

1. Create snapshot folder:
   - `related-projects/{raw_source}`
2. Download only topic-relevant content.
3. Preserve traceability by storing:
   - original URL list
   - fetched artifacts
   - optional mini-manifest with URL -> local filename mapping
4. Avoid full-site mirror unless user explicitly asks.

## Phase 3: Deep Summary Authoring

Create `related-projects/{raw_source}.md` with evidence-backed, source-centric analysis.

Required sections:

1. Title and source identity.
2. Scope and indexing metadata:
   - indexed date
   - source URLs
   - source artifact folder path
3. Executive summary explaining what the source does, what it implements, and why it is technically important on its own terms.
4. Table of contents when the report is long or multi-topic.
5. Relevant structure/modules.
6. Critical technical findings tied to topic focus.
7. Behavior, compatibility, and operational notes evidenced by the source itself.
8. Constraints, caveats, discrepancies, and unresolved unknowns.
9. Practical checklist for implementation/testing reuse.
10. Source index with direct local file links and upstream links.

When the source is a technical implementation repo or protocol/filesystem reference, also include the following where applicable:

1. Supported formats, modes, or variants as a table.
2. End-to-end flow or pipeline description.
3. Important structs, constants, flags, config keys, and path conventions.
4. Data layout or folder layout rules.
5. Validation rules and failure conditions.
6. Tooling/scripts/build helpers relevant to reproducing behavior.
7. A concrete generator/consumer checklist if the source implies one.

Depth requirements:

1. Prefer exhaustive coverage of topic-relevant behavior over brief summaries.
2. If a finding controls compatibility or implementation decisions, explain the actual code path and decision points.
3. Call out mismatches between code defaults, docs, examples, and runtime behavior.
4. Include enough source references that a future reader can audit every important claim quickly.
5. If the user supplied a draft, preserve useful insights but do not inherit its structure if the repo demands deeper organization.

Citation rules:

1. Every non-trivial claim must point to a concrete source.
2. Prefer local snapshot/submodule links first, then upstream URL.
3. Keep claim-to-source mapping auditable.
4. For high-value findings, cite the most direct implementation file rather than only README-level docs.
5. For discrepancies, cite both sides of the discrepancy when available.

If user provided a draft:

1. Treat draft as a hypothesis layer.
2. Verify each important claim against source.
3. Correct mismatches and preserve valid insights.
4. Reflect reconciled result in final summary.

## Phase 4: Memory Synchronization

Update `.claude/MEMORY.md` in `Related Projects Knowledge Base`.

For each source entry include:

1. Canonical source identity (repo/doc root link).
2. Local artifact folder link (`related-projects/{raw_source}`).
3. Deep summary link (`related-projects/{raw_source}.md`).
4. Short summary bullets (3 to 5 bullets).
5. Priority files/pages list for fast re-validation.

Idempotency rules:

1. If entry already exists, update in place.
2. Do not duplicate entries for same `raw_source`.
3. Keep unrelated entries untouched.

## Phase 5: Quality Gates

Before completion, verify all checks:

1. Output folder exists and is non-empty.
2. Summary markdown exists and references valid sources.
3. Memory entry exists under correct section.
4. Local links resolve.
5. Naming follows slug standard.
6. Reindex path did not create duplicate memory entries.
7. Summary is sufficiently deep for the source type:
   - implementation repos should document architecture, flow, and key constants/config
   - docs/wiki sources should capture only relevant pages but preserve traceability
8. Summary contains actionable technical information derived from the source itself, not just descriptive prose.
9. Important compatibility-affecting claims are backed by direct source references.
10. Summary does not rely on or reference implementation details from the parent repository, other related-project entries, or prior local knowledge unless the user explicitly requested a comparison.

## Source-Centric Analysis Rule

When analyzing a related project, extract as much knowledge as possible from that related project itself.

Required behavior:

1. Prefer the related project's own code, docs, configs, build files, tests, examples, and submodules as evidence.
2. Treat user-provided drafts as hypotheses to verify, not as facts to inherit.
3. Do not import technical claims from the parent repository unless the user explicitly asks for cross-project comparison or integration mapping.
4. Do not import technical claims from other entries under `related-projects/` unless the user explicitly asks for comparison.
5. If a concept is not evidenced by the related project itself, mark it unknown rather than filling gaps from prior knowledge.

Forbidden by default:

1. "This matters to mkpfs because..." framing inside the deep summary.
2. Explaining the parent repository's implementation as if it were part of the related project.
3. Pulling format or workflow details from another related project to complete the report.

Allowed only when explicitly requested:

1. Cross-project comparison sections.
2. Integration notes between the related project and the parent repository.
3. "How this compares to X" analysis.

If any check fails, fix before completing.

## Reindex Mode

When user asks reindex/update:

1. Refresh source artifacts.
2. Recompute summary with explicit change-focused verification.
3. Update indexed date and changed findings.
4. Patch memory entry; do not append duplicate entry.

## Failure Handling

If source is partially inaccessible:

1. Continue in degraded mode with available artifacts.
2. Mark missing sources explicitly in summary.
3. List follow-up actions needed to reach full fidelity.

Never fabricate findings for unavailable content.

## Repository-Specific Guardrails

1. Keep transient files under `tmp/` only.
2. Keep durable related-source artifacts under `related-projects/`.
3. Do not create standalone docs outside requested output paths.
4. Preserve existing formatting/style in `.claude/MEMORY.md`.

## Recommended Companion Templates

Use these templates for consistency:

1. `references/report-template.md`
2. `references/memory-entry-template.md`
3. `references/source-manifest-template.md`

Use template content as structure, but always prefer source-truth over boilerplate.

## ShadowMountPlus-Level Standard

Use the ShadowMountPlus result as the benchmark for a successful technical summary when the source is similarly implementation-heavy.

That means the summary should usually include, where relevant:

1. Project structure breakdown.
2. Format/support matrix.
3. End-to-end execution or mount/build flow.
4. Internal constants, structs, and option tables.
5. Layout rules and required files.
6. Config/default discrepancies and runtime caveats.
7. System paths, limits, and operational constraints.
8. Source file index for fast follow-up inspection.
9. A distilled checklist directly usable for future work derived from this source alone.
