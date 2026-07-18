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

## D5 — Deploy target: Streamlit Community Cloud (not HuggingFace)

Task 8 named HF Spaces, but HuggingFace turned out to be a dead end for a free
Streamlit app, discovered in this order:

1. Deploy could not run from the build sandbox at all — its egress policy denies
   `huggingface.co` (proxy `403` on `CONNECT`, same allowlist that blocks
   `google.com`); a policy 403 must not be routed around.
2. Deploying from Umut's own machine, the token authenticated fine (`whoami` →
   `umuutakarsu`), but `repos/create` with `space_sdk="streamlit"` returned
   **400** — `expected one of "gradio"|"docker"|"static"`. HF no longer offers
   the `streamlit` SDK for this account.
3. Reconfigured as a **Docker** Space; `space_sdk="docker"` then returned
   **402 Payment Required** — "Static Spaces are free for everyone, but hosting
   Gradio and Docker Spaces on free cpu-basic requires a PRO subscription."

Conclusion: HF's free tier only hosts *Static* Spaces, which cannot run a
server-side Streamlit app. **Decision:** deploy to **Streamlit Community Cloud**
instead — free, Streamlit-native, deploys directly from `github.com/umutakarsu/loop`
with zero code changes. The HF-specific artifacts (README front-matter, the
`Dockerfile`, and `.dockerignore`) were removed as no longer needed. Live URL:
deployed by Umut at a `*.streamlit.app` address (see README "Deploy" section for
the one-time GitHub-connect steps).

**Security note:** the HF token was shared in chat, so it is compromised and must
be rotated by Umut (HF → Settings → Access Tokens). It was never written to any
file or commit in this repo (verified by grep across the full history).

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
