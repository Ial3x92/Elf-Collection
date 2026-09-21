# {Display Name} — Related Source Deep Summary

> Use this template as a scaffold. Remove sections that are truly irrelevant, but keep the report technically deep when the source is implementation-heavy.

## Source Identity

- Canonical name: {display_name}
- Type: {git|docs|mixed}
- Upstream source(s):
  - {url_1}
  - {url_2}
- Local artifact folder: [related-projects/{raw_source}](related-projects/{raw_source})
- Indexed on: {YYYY-MM-DD}

## Executive Summary

- {what_this_source_implements_1}
- {what_this_source_implements_2}

## Table of Contents

1. Source Identity
2. Scope
3. Project Structure
4. Supported Formats / Variants
5. Architecture / Flow
6. Technical Findings
7. Compatibility and Behavior Notes
8. Constraints and Caveats
9. Actionable Checklist
10. Source Index
11. Reindex Notes

## Scope

- Topic focus: {topic_focus}
- Evidence policy: derive findings from this source itself unless the user explicitly requested comparison
- Included content:
  - {included_scope_1}
  - {included_scope_2}
- Excluded content:
  - {excluded_scope_1}

## Project Structure

```text
related-projects/{raw_source}/
├── ...
└── ...
```

- High-value directories/files:
  - [related-projects/{raw_source}/{path_1}](related-projects/{raw_source}/{path_1})
  - [related-projects/{raw_source}/{path_2}](related-projects/{raw_source}/{path_2})

## Supported Formats / Variants

| Variant | Meaning | Status | Evidence |
|--------|---------|--------|----------|
| {variant_1} | {variant_meaning_1} | {status_1} | {evidence_1} |
| {variant_2} | {variant_meaning_2} | {status_2} | {evidence_2} |

## Structure and Modules

- Key modules/pages:
  - [{module_or_page_1}](related-projects/{raw_source}/{path_1})
  - [{module_or_page_2}](related-projects/{raw_source}/{path_2})

## Architecture / Flow

1. {flow_step_1}
2. {flow_step_2}
3. {flow_step_3}

## Important Constants / Config / Paths

- Constants/flags:
  - {constant_or_flag_1}
  - {constant_or_flag_2}
- Config keys/defaults:
  - {config_key_1}
  - {config_key_2}
- Path conventions:
  - {path_rule_1}
  - {path_rule_2}

## Layout and Validation Rules

- Required layout rule: {layout_rule_1}
- Validation rule: {validation_rule_1}
- Failure condition: {failure_condition_1}

## Technical Findings

1. {finding_1}
  - Evidence: [{local_source_link_1}](related-projects/{raw_source}/{evidence_path_1})
  - Upstream: {upstream_link_1}
2. {finding_2}
  - Evidence: [{local_source_link_2}](related-projects/{raw_source}/{evidence_path_2})
  - Upstream: {upstream_link_2}

## Compatibility and Behavior Notes

- {compat_note_1}
- {compat_note_2}

## Discrepancies and Caveats

- {discrepancy_1}
- {discrepancy_2}

## Constraints and Caveats

- {caveat_1}
- {caveat_2}

## Actionable Checklist

1. {action_1}
2. {action_2}
3. {action_3}

## Source-Centric Guardrail

- Avoid referencing the parent repository unless the user explicitly asked for integration notes.
- Avoid pulling facts from other related-project reports unless the user explicitly asked for comparison.
- Mark gaps as unknown when this source does not evidence them directly.

## Source Index

- Local folder root: [related-projects/{raw_source}](related-projects/{raw_source})
- Key local sources:
  - [related-projects/{raw_source}/{path_1}](related-projects/{raw_source}/{path_1})
  - [related-projects/{raw_source}/{path_2}](related-projects/{raw_source}/{path_2})
- Upstream references:
  - {upstream_reference_1}
  - {upstream_reference_2}

## Reindex Notes

- Previous index date: {previous_index_date_or_na}
- Delta summary:
  - {delta_1}
  - {delta_2}
