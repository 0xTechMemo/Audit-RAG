# C4 Intake Notes

## Extraction Priority

1. Parse C4 audit page directly.
2. Probe repository README (`main` then `master`) for missing scope fields.
3. Probe public report URL (`/reports/<slug>`) for known findings.
4. Fall back to slug-derived repo guess when page does not expose repository.

## Access-Restricted Audits

Live C4 audits can hide details behind "Join audit". In that case:

- `requires_join` is set to `true`
- `in_scope_files` may be empty or partial
- `repo_url` may be unverified

Do not submit findings until manual scope is confirmed.

## Known Finding De-duplication

Treat known finding entries as signatures:

- normalize by lowercasing and removing punctuation
- match by root cause and impact, not exact sentence structure
- if equivalent to known finding, mark duplicate and suppress

## Out-of-Scope Guardrail

If the issue is in a file not included in the final in-scope list, drop it even if technically valid.

