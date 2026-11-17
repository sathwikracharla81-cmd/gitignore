# R46-T003 — Ninja ignore fixtures

## Temporary .gitignore rules

.ninja_deps
.ninja_log

!keep.ninja_log

## Test fixtures

| File | Expected result | Actual result |
|---|---|---|
| .ninja_deps | Ignored | Ignored |
| build/.ninja_deps | Ignored | Ignored |
| .ninja_log | Ignored | Ignored |
| build/.ninja_log | Ignored | Ignored |
| .ninja_deps-backup | Not ignored | Not ignored |
| .ninja_log-backup | Not ignored | Not ignored |
| keep.ninja_log | Not ignored | Not ignored |

## Negation demonstration

The last matching rule wins. The rule !keep.ninja_log
overrides the earlier .ninja_log rule for keep.ninja_log.

## Tracked-file behaviour

A tracked .ninja_deps file remains tracked.
Normal git check-ignore does not report it.
Using --no-index identifies the matching ignore rule.

## Test result

All 16 automated checks passed.

## Tool versions

Git 2.55.0
Python 3.14.7
