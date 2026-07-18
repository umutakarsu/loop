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

## D6 — Standalone repo (initially blocked, now resolved)

Task 1 / §2 call for a standalone repo `umutakarsu/loop`. The build session could
not create it (the GitHub integration returned 403 "Resource not accessible by
integration"; its scope was limited to `umutakarsu/brainnn`, and no token was
available to create one). As an interim durable home — the container is
ephemeral — the full product was pushed to the feature branch
`claude/product-pivot-implementation-5ldhcn` on `brainnn`, isolated under a
top-level `loop/` directory, touching none of the grant-critical files
(`src/brainnn/bci/`, `bci_dashboard.py`, `README.md`, `docs/`) and leaving
`brainnn`'s default branch untouched.

**Resolved (GitHub):** Umut created `umutakarsu/loop`; this repo's full per-task
history was pushed there as `main`. The `loop/` copy on the `brainnn` feature
branch is now a redundant mirror and can be deleted at leisure (it never polluted
`main`).

## D5 — HuggingFace deploy (Task 8): blocked by network egress policy

Task 8 asks to deploy to HF Spaces under `umuutakarsu`. Umut provided a valid HF
token, but deployment **cannot run from the build environment**: this session's
outbound egress policy denies `huggingface.co` (the agent proxy answers `403` to
`CONNECT huggingface.co:443` — the same allowlist that blocks e.g. `google.com`).
The proxy rules are explicit that a policy 403 must not be routed around. So this
is an infrastructure limit of the build sandbox, not a token or code problem.

The repo is **deploy-ready** and the four-screen flow was verified end-to-end in
a real browser (see `docs/screenshots/`), so what deploys is known-good. Deploy
from any machine that can reach huggingface.co, using the snippet in the README's
"Deploy" section.

**SDK note (discovered during deploy):** HF's `repos/create` API rejects the
`streamlit` SDK for this account (`expected one of "gradio"|"docker"|"static"`).
So the Space runs as a **Docker** Space via the repo's `Dockerfile`
(`sdk: docker`, `app_port: 8501`). Docker runs the identical Streamlit app — no
code change, still torch-free, still fast cold start. The Docker image was built
and run locally and confirmed to serve the app before this was committed.

**Security note:** the HF token was shared in chat, so it should be treated as
compromised — rotate it (HF → Settings → Access Tokens) and use the fresh one for
the command above. Nothing in this repo contains the token.

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
