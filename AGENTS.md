# Project instructions

This is Alex Palmer's public Sales, GTM and AI publication. Keep it plain HTML
and CSS, preserve existing URLs and avoid adding infrastructure without approval.

## Read before working

Read these files in full before writing or editing content:

1. `DESIGN.md` for visual direction.
2. `WRITING.md` for voice and sentence-level editing.
3. `EDITORIAL.md` for evidence, format requirements and the input contract.
4. `PUBLISHING.md` for files, preview, approval and publication.

Read the affected article and relevant linked pieces. An older published article
is context, not permission to repeat a pattern prohibited by current guidance.
When using only a GitHub connector, fetch these files explicitly before editing.

## Non-negotiables

- Use Australian English. Apply the zero-em-dash rule in `WRITING.md` to all
  authored website copy and channel drafts. Do not use HTML entities to hide it.
- Never invent Alex's experience, customer details, results, quotations or sources.
- If a substantive article needs personal material, interview Alex one question
  at a time before drafting. Confirm the thesis and usable evidence with him.
- Keep illustrative workflows clearly distinct from firsthand experiments.
- Keep private notes, transcripts and unapproved drafts outside this repository.
  A draft PR is public. Ask before putting new personal material in public code.
- Use a branch from current `main`. Preserve unrelated user changes.
- Require explicit approval of the exact revision before merging or publishing.
  Approval of one PR does not authorize publication of a later PR.

## Verification and handoff

Run `python3 scripts/check_site.py` and
`python3 -m unittest discover -s scripts -p 'test_*.py'`.
Also run `git diff --check`. Follow the human voice and evidence checks in
`WRITING.md` and `EDITORIAL.md`; automated checks cannot establish authenticity.

Update repeated metadata and reading estimates consistently when article copy
changes. Report what is done, pending and blocked. Distinguish saved changes,
previewed changes and a verified live deployment. Never claim a review happened
when it did not. Keep review summaries concise and explain the relevant HTML/CSS
relationship so Alex learns how to inspect the work.
