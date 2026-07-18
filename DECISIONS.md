# DECISIONS

Decisions made during implementation that the HANDOFF spec did not fully cover.
Per §9, the rule is: make the reasonable call, write it here, keep moving.

---

## D1 — Where the product lives

The session harness handed a boilerplate instruction to develop on a branch
inside `brainnn`. That directly conflicts with the HANDOFF (§2, §5) and Umut's
explicit instruction to build in a **new** repo `umutakarsu/loop`. Umut's direct
instruction wins: the product is built in `umutakarsu/loop`, standalone, with no
import from `brainnn`. `brainnn` is left untouched.

## D2 — Python package name

`loop` is a reserved-ish word and shadows nothing in stdlib, so the package is
named `loop/` as the spec's tree shows. The Streamlit entry point stays at repo
root as `app.py`.

## D5 — HuggingFace deploy (Task 8) is prepared, not executed

Task 8 asks to deploy to HF Spaces under `umuutakarsu`. This session has no HF
token, no HF CLI, and no cached HF credentials — deploying would require Umut's
account secret, which is not available here and must not be fabricated. This is a
capability limit, not a spec question, so per §9 the call is:

- The repo is made **one-command deployable**: the README front-matter is a valid
  HF Spaces config (`sdk: streamlit`, `app_file: app.py`), `app.py` is at the
  repo root, and `requirements.txt` is torch-free for fast free-tier cold starts.
- Exact deploy steps are documented in the README ("Deploy" section).
- The full four-screen flow was verified end-to-end in a real browser
  (see `docs/screenshots/`), so what would be deployed is known-good.

**Action needed from Umut:** run the three documented commands with his HF login,
or paste an HF token into a follow-up and this can be pushed for him.

## D4 — Where narration strings live

§5 puts narration in `narrate.py`; §6 says "every user-facing string in ONE
file" (`copy.py`). These conflict for the phase narration. Call: the
phase-narration templates live in `narrate.py` because they are tightly coupled
to the phase-detection logic that fills their placeholders, and `copy.py` holds
all *static* chrome (labels, questions, disclaimer, resources). Both files obey
the §6 tone rules. `copy.py` documents this split at the top so a reader still
has one place that points to every string.

## D3 — Branding constant

Per §2 ("leave branding in one config constant so it is a one-line change"), the
product name lives as `APP_NAME` in `loop/copy.py`. Changing the name is a
one-line edit there.
