"""Loop — map a behavioural loop, see the mechanism (§4 flow, richer-but-simpler).

Run: streamlit run app.py

No PyTorch, no ML, no database, no auth, no payments. All six presets get
identical UI treatment. Screen 3 leads with a plain-language story and a picture
unique to each loop; the curves + science live behind "Show the detail".
"""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from loop import copy as C
from loop import charts
from loop import simulate as sim
from loop.narrate import narrate
from loop.presets import all_selectable, get_preset, GENERIC_KEY
from loop.stories import get_story
from loop.copy import PRESET_SUBTITLES

BLUE = charts.BLUE
AMBER = charts.AMBER
GREY = charts.GREY

st.set_page_config(page_title=C.APP_NAME, page_icon="🔁", layout="centered")

# Consumer-facing charts: no plotly toolbar clutter.
PLOTLY_CONFIG = {"displayModeBar": False}


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

def _init_state() -> None:
    ss = st.session_state
    ss.setdefault("screen", 1)
    ss.setdefault("preset_key", None)
    ss.setdefault("frequency", "daily")
    ss.setdefault("duration", "months")
    ss.setdefault("intensity", 6)


def _goto(screen: int) -> None:
    st.session_state.screen = screen


def _episode_count() -> float:
    return sim.episodes_from_frequency_duration(
        st.session_state.frequency, st.session_state.duration
    )


# ---------------------------------------------------------------------------
# Screen-4 figures
# ---------------------------------------------------------------------------

def recovery_figure(rec: dict) -> go.Figure:
    fig = go.Figure()
    fig.add_hline(y=1.0, line=dict(color=GREY, width=1.5, dash="dash"),
                  annotation_text="intact baseline")
    fig.add_trace(go.Scatter(x=rec["days"], y=rec["baseline"], line=dict(color=BLUE, width=3),
                             fill="tozeroy", fillcolor="rgba(46,134,222,0.08)"))
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10),
                      xaxis_title="Days with no repetition", yaxis_title="Baseline",
                      yaxis=dict(range=[0, 1.1]), showlegend=False)
    return fig


def delay_figure(cmp: dict) -> go.Figure:
    fig = go.Figure()
    fig.add_hline(y=cmp["baseline"], line=dict(color=GREY, width=1.2, dash="dash"))
    fig.add_trace(go.Scatter(x=cmp["t"], y=cmp["now"], name="now",
                  line=dict(color=BLUE, width=3)))
    fig.add_trace(go.Scatter(x=cmp["t"], y=cmp["delayed"], name=f"delayed {cmp['delay_hours']:.0f}h",
                  line=dict(color=AMBER, width=3, dash="dot")))
    fig.update_layout(height=290, margin=dict(l=10, r=10, t=10, b=10),
                      xaxis_title=C.t("axis_time"), yaxis_title=C.t("axis_level"),
                      legend=dict(orientation="h", yanchor="bottom", y=-0.35, x=0))
    return fig


def frequency_bar(cmp: dict) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=["Current frequency", "Half the frequency"],
        y=[cmp["current_baseline"], cmp["reduced_baseline"]],
        marker_color=[AMBER, BLUE],
        text=[f"{cmp['current_baseline']:.2f}", f"{cmp['reduced_baseline']:.2f}"],
        textposition="outside"))
    fig.add_hline(y=1.0, line=dict(color=GREY, width=1.2, dash="dash"),
                  annotation_text="intact baseline")
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10),
                      yaxis=dict(range=[0, 1.1], title="Resulting baseline"), showlegend=False)
    return fig


# ---------------------------------------------------------------------------
# Persistent chrome
# ---------------------------------------------------------------------------

def footer() -> None:
    st.divider()
    st.caption("⚕️ " + C.t("disclaimer"))
    st.caption("📞 " + C.t("resources"))
    with st.expander(C.t("about_title")):
        st.markdown(C.t("about_body"))


# ---------------------------------------------------------------------------
# Screens
# ---------------------------------------------------------------------------

def screen_pick() -> None:
    st.title(C.APP_NAME)
    st.markdown(f"**{C.TAGLINE}**")
    st.subheader(C.t("s1_title"))
    st.caption(C.t("s1_subtitle"))

    cols = st.columns(2)
    for i, (key, label) in enumerate(all_selectable()):
        story = get_story(key)
        subtitle = story["headline"] if story else PRESET_SUBTITLES.get(key, "")
        with cols[i % 2]:
            if st.button(f"**{label}**\n\n{subtitle}", key=f"preset_{key}",
                         use_container_width=True):
                st.session_state.preset_key = key
                _goto(2)
                st.rerun()


def screen_customise() -> None:
    st.subheader(C.t("s2_title"))
    st.caption(C.t("s2_subtitle"))

    freq_opts = C.frequency_options()
    dur_opts = C.duration_options()

    freq_labels = [lab for _, lab in freq_opts]
    freq_keys = [k for k, _ in freq_opts]
    freq_idx = freq_keys.index(st.session_state.frequency) if st.session_state.frequency in freq_keys else 1
    freq_choice = st.radio(C.t("q_frequency"), freq_labels, index=freq_idx)
    st.session_state.frequency = freq_keys[freq_labels.index(freq_choice)]

    dur_labels = [lab for _, lab in dur_opts]
    dur_keys = [k for k, _ in dur_opts]
    dur_idx = dur_keys.index(st.session_state.duration) if st.session_state.duration in dur_keys else 1
    dur_choice = st.radio(C.t("q_duration"), dur_labels, index=dur_idx)
    st.session_state.duration = dur_keys[dur_labels.index(dur_choice)]

    st.session_state.intensity = st.slider(
        C.t("q_intensity"), 1, 10, st.session_state.intensity,
        help=f"1 = {C.t('intensity_min')}, 10 = {C.t('intensity_max')}")

    c1, c2 = st.columns(2)
    if c1.button(C.t("cta_back"), use_container_width=True):
        _goto(1); st.rerun()
    if c2.button(C.t("cta_next"), type="primary", use_container_width=True):
        _goto(3); st.rerun()


def screen_narrated() -> None:
    key = st.session_state.preset_key
    preset = get_preset(key)
    story = get_story(key)
    intensity = st.session_state.intensity
    n_episodes = _episode_count()

    timeline = sim.simulate_timeline(preset, intensity=intensity, n_episodes=n_episodes)
    phases = narrate(preset, timeline, loop_key=key)

    # Headline + one-liner (plain language, per loop).
    headline = story["headline"] if story else C.t("generic_headline")
    one_line = story["one_line"] if story else C.t("generic_one_line")
    st.header(headline)
    st.caption(f"{preset['label']} — {one_line}")

    # The signature picture (unique per loop); generic falls back to the timeline.
    fig = charts.signature_figure(key, preset, intensity=intensity, n_episodes=n_episodes)
    if fig is None:
        fig = charts.detail_timeline_figure(timeline, phases)
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)

    # Four plain steps.
    st.markdown(f"**{C.t('phases_heading')}**")
    for p in phases:
        st.markdown(
            f"<span style='color:{charts.PHASE_COLORS[p.key]}'>●</span> "
            f"**{p.label}** — {p.text}", unsafe_allow_html=True)

    # The reframe — the whole point.
    what = story["what_this_means"] if story else C.t("generic_what_this_means")
    st.info(f"**{C.t('what_this_means_label')}** — {what}")

    # Depth on demand: the curves + the science.
    with st.expander(C.t("detail_expander")):
        st.plotly_chart(charts.detail_timeline_figure(timeline, phases),
                        use_container_width=True, config=PLOTLY_CONFIG)
        drift = timeline["drift"]
        if drift < -0.01:
            st.caption(
                f"After the repetitions you described, the baseline this curve is "
                f"measured against has drifted down by {abs(drift) * 100:.0f}%. That "
                f"is the allostatic shift — the same peak now lands on lower ground.")
        if story:
            st.markdown(f"**{C.t('detail_science_label')}**")
            st.markdown(story["detail_note"])
        st.caption(C.t("science_frame"))

    c1, c2 = st.columns(2)
    if c1.button(C.t("cta_back"), use_container_width=True):
        _goto(2); st.rerun()
    if c2.button(C.t("cta_whatif"), type="primary", use_container_width=True):
        _goto(4); st.rerun()


def screen_whatif() -> None:
    preset = get_preset(st.session_state.preset_key)
    n = _episode_count()
    intensity = st.session_state.intensity
    st.subheader(C.t("s4_title"))
    st.caption(C.t("s4_subtitle"))

    st.markdown(f"**{C.t('whatif_recovery')}**")
    st.plotly_chart(recovery_figure(sim.simulate_recovery(preset, n, days=30)),
                    use_container_width=True, config=PLOTLY_CONFIG)
    st.caption(C.t("whatif_recovery_note"))

    st.markdown(f"**{C.t('whatif_delay')}**")
    st.plotly_chart(delay_figure(sim.compare_delay(preset, intensity, n)),
                    use_container_width=True, config=PLOTLY_CONFIG)
    st.caption(C.t("whatif_delay_note"))

    st.markdown(f"**{C.t('whatif_frequency')}**")
    st.plotly_chart(frequency_bar(sim.compare_frequency(preset, intensity, n)),
                    use_container_width=True, config=PLOTLY_CONFIG)
    st.caption(C.t("whatif_frequency_note"))

    c1, c2 = st.columns(2)
    if c1.button(C.t("cta_back"), use_container_width=True):
        _goto(3); st.rerun()
    if c2.button(C.t("cta_restart"), use_container_width=True):
        _goto(1); st.session_state.preset_key = None; st.rerun()


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

def main() -> None:
    _init_state()
    screen = st.session_state.screen
    if screen == 1 or st.session_state.preset_key is None:
        screen_pick()
    elif screen == 2:
        screen_customise()
    elif screen == 3:
        screen_narrated()
    elif screen == 4:
        screen_whatif()
    footer()


if __name__ == "__main__":
    main()
