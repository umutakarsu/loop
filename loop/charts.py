"""Signature visualisations — one distinct picture per loop (§ "richer, simpler").

The complaint that drove this: every loop drew the same spike-and-dip. Each loop
now gets its OWN picture that makes its defining mechanism visible at a glance,
with plain on-chart labels and a de-cluttered y-axis (absolute dopamine numbers
mean nothing to a non-expert; the shape is the message). The detailed multi-
signal timeline still exists — it moves into the "Show the detail" expander via
`detail_timeline_figure`.

Every builder returns a plotly Figure. `signature_figure` dispatches on the
loop's story `kind`; loops without a story (the generic template) return None and
the app falls back to the detailed timeline as the main chart.
"""

from __future__ import annotations

import math

import numpy as np
import plotly.graph_objects as go

from loop import simulate as sim
from loop.stories import get_story

# --- palette --------------------------------------------------------------
BLUE = "#2E86DE"
PURPLE = "#8E44AD"
AMBER = "#E67E22"
GREY = "#8395A7"
RED = "#C0392B"
CALM_FILL = "rgba(52, 152, 219, 0.18)"
WARM_FILL = "rgba(230, 126, 34, 0.20)"
LOW_FILL = "rgba(192, 57, 43, 0.10)"
PURPLE_FILL = "rgba(142, 68, 173, 0.16)"
BLUE_FILL = "rgba(46, 134, 222, 0.16)"

_LN2 = math.log(2.0)


def _style(fig: go.Figure, xlabel: str, height: int = 380, show_y: bool = False) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=12, r=12, t=54, b=12),
        xaxis_title=xlabel,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        hovermode=False,
        font=dict(size=13),
    )
    fig.update_yaxes(showticklabels=show_y, showgrid=False, zeroline=False)
    fig.update_xaxes(showgrid=False, zeroline=False)
    return fig


def _title(fig: go.Figure, text: str) -> None:
    fig.add_annotation(
        x=0, y=1.14, xref="paper", yref="paper", showarrow=False,
        text=f"<b>{text}</b>", font=dict(size=15), align="left", xanchor="left",
    )


def _gauss(t, center, sigma):
    sigma = max(sigma, 1e-6)
    return np.exp(-((t - center) ** 2) / (2.0 * sigma ** 2))


# ---------------------------------------------------------------------------
# 1. binge — two peaks: wanting (anticipation) taller than liking (consumption)
# ---------------------------------------------------------------------------

def two_peaks_figure(preset, intensity, label) -> go.Figure:
    t = np.linspace(0, 2.4, 600)
    c = sim.episode_components(t, preset, intensity=intensity, baseline=1.0)
    pull = 1.0 + c["anticipation"]
    payoff = 1.0 + c["consumption"]
    i_pull = int(np.argmax(c["anticipation"]))
    i_pay = int(np.argmax(c["consumption"]))

    fig = go.Figure()
    fig.add_hline(y=1.0, line=dict(color=GREY, width=1.5, dash="dash"),
                  annotation_text="your normal", annotation_position="bottom left")
    fig.add_trace(go.Scatter(x=t, y=pull, line=dict(color=PURPLE, width=3),
                             fill="tonexty" if False else "tozeroy", fillcolor=PURPLE_FILL))
    fig.add_trace(go.Scatter(x=t, y=payoff, line=dict(color=BLUE, width=3),
                             fill="tozeroy", fillcolor=BLUE_FILL))
    # relabel the fills to baseline by clipping view
    fig.update_yaxes(range=[0.9, max(pull.max(), payoff.max()) * 1.08])

    fig.add_annotation(x=t[i_pull], y=pull[i_pull], text="<b>the pull</b><br>(wanting)",
                       showarrow=True, arrowhead=0, ax=0, ay=-34, font=dict(color=PURPLE))
    fig.add_annotation(x=t[i_pay], y=payoff[i_pay], text="<b>the payoff</b><br>(liking)",
                       showarrow=True, arrowhead=0, ax=36, ay=-24, font=dict(color=BLUE))
    # gap bracket
    xg = t[i_pull]
    fig.add_shape(type="line", x0=xg, x1=xg, y0=payoff[i_pay], y1=pull[i_pull],
                  line=dict(color=RED, width=2))
    fig.add_annotation(x=xg, y=(pull[i_pull] + payoff[i_pay]) / 2,
                       text="wanting&gt;liking", showarrow=False, xanchor="right",
                       font=dict(color=RED, size=12), xshift=-6)
    _title(fig, label)
    return _style(fig, "Time around the episode")


# ---------------------------------------------------------------------------
# 2. porn — escalation: next time starts lower and lands lower
# ---------------------------------------------------------------------------

def escalation_figure(preset, intensity, n_episodes, label) -> go.Figure:
    # Zoom on the peak region: porn peaks at ~20 min, so a 40h axis collapses both
    # spikes into one line. The escalation message is about peak HEIGHT, so show
    # the first ~1.5h where the two peaks are visible and comparable.
    t = np.linspace(0, 1.6, 700)
    this = sim.episode_curve(t, preset, intensity=intensity, baseline=1.0)
    next_base = 0.78
    nxt = sim.episode_curve(t, preset, intensity=intensity, baseline=next_base)
    this_peak = float(this.max()); next_peak = float(nxt.max())
    xp = float(t[int(np.argmax(this))])

    fig = go.Figure()
    fig.add_hline(y=1.0, line=dict(color=GREY, width=1.5, dash="dash"),
                  annotation_text="your normal", annotation_position="bottom left")
    fig.add_hline(y=this_peak, line=dict(color=PURPLE, width=1, dash="dot"),
                  annotation_text="as high as last time", annotation_position="top right")
    fig.add_trace(go.Scatter(x=t, y=this, line=dict(color=BLUE, width=3),
                             fill="tozeroy", fillcolor=BLUE_FILL, name="this time"))
    fig.add_trace(go.Scatter(x=t, y=nxt, line=dict(color=PURPLE, width=2.5, dash="dot"),
                             opacity=0.8, name="next time"))
    fig.add_annotation(x=xp, y=this_peak, text="<b>this time</b>", showarrow=True,
                       arrowhead=0, ax=46, ay=-14, font=dict(color=BLUE))
    fig.add_annotation(x=xp, y=next_peak, text="<b>next time</b>", showarrow=True,
                       arrowhead=0, ax=60, ay=6, font=dict(color=PURPLE))
    # shortfall bracket a little to the right of the peaks
    xb = xp + 0.28
    fig.add_shape(type="line", x0=xb, x1=xb, y0=next_peak, y1=this_peak,
                  line=dict(color=RED, width=2))
    fig.add_annotation(x=xb, y=(this_peak + next_peak) / 2, text="falls short",
                       showarrow=False, xanchor="left", xshift=6, font=dict(color=RED, size=12))
    fig.update_yaxes(range=[min(this.min(), nxt.min()) - 0.05, this_peak * 1.16])
    _title(fig, label)
    return _style(fig, "Hours since the cue (zoomed on the peak)")


# ---------------------------------------------------------------------------
# 3. nicotine — the sinking floor: hits chase a normal that keeps dropping
# ---------------------------------------------------------------------------

def sinking_floor_figure(preset, intensity, label) -> go.Figure:
    n_hits = 12
    interval = 2.0
    t = np.linspace(0, n_hits * interval, 2400)
    scale = sim.intensity_scale(intensity)

    floor = np.clip(1.0 - 0.035 * (t / interval), 0.55, 1.0)
    dop = floor.copy()
    relief = 0.45 * scale
    tau = 0.8  # visual clearance (h)
    for i in range(n_hits):
        ti = i * interval
        dop = dop + np.where(t >= ti, relief * np.exp(-np.maximum(t - ti, 0) * _LN2 / tau), 0.0)

    fig = go.Figure()
    fig.add_hline(y=1.0, line=dict(color=GREY, width=1.5, dash="dash"),
                  annotation_text="normal at the start of the day", annotation_position="top right")
    # widening gap between original and sinking floor
    fig.add_trace(go.Scatter(x=t, y=np.full_like(t, 1.0), line=dict(width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=t, y=floor, line=dict(color=GREY, width=2),
                             fill="tonexty", fillcolor=LOW_FILL))
    fig.add_trace(go.Scatter(x=t, y=dop, line=dict(color=BLUE, width=2.5)))
    fig.add_annotation(x=0.0, y=float(dop[np.argmin(np.abs(t - 0.0))]),
                       text="this one felt like something", showarrow=True, arrowhead=0,
                       ax=70, ay=-26, font=dict(color=BLUE, size=11))
    late = (n_hits - 2) * interval
    fig.add_annotation(x=late, y=1.0, text="this one just gets you level", showarrow=True,
                       arrowhead=0, ax=-4, ay=-34, font=dict(color=BLUE, size=11))
    fig.add_annotation(x=t[-1], y=float(floor[-1]), text="normal keeps sinking",
                       showarrow=False, xanchor="right", yshift=-14, font=dict(color=GREY, size=12))
    fig.update_yaxes(range=[0.4, 1.6])
    _title(fig, label)
    return _style(fig, "Hours across a day of hits")


# ---------------------------------------------------------------------------
# 4. doomscrolling — the missing "full" line
# ---------------------------------------------------------------------------

def no_satiety_figure(preset, intensity, label) -> go.Figure:
    t = np.linspace(0, 90, 3000)  # minutes
    rng = np.random.default_rng(7)
    n = 4 * 90
    centers = np.sort(rng.uniform(0, 90, n))
    heights = rng.uniform(0.10, 0.30, n) * sim.intensity_scale(intensity)
    sag = 1.0 - 0.0016 * t
    # vectorised sum of narrow gaussians
    spikes = (heights[:, None] * np.exp(-((t[None, :] - centers[:, None]) ** 2) / (2 * 0.18 ** 2))).sum(axis=0)
    dop = sag + spikes

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=dop, line=dict(color=BLUE, width=1)))
    fig.add_trace(go.Scatter(x=t, y=sag, line=dict(color=GREY, width=1.5, dash="dash")))
    fig.add_annotation(x=90, y=1.0, text="the \"full\" signal never rises →", showarrow=False,
                       xanchor="right", yshift=-16, font=dict(color=RED, size=12))
    fig.add_annotation(x=90, y=float(dop.max()), text="…no natural end", showarrow=False,
                       xanchor="right", font=dict(color=GREY, size=11))
    fig.update_yaxes(range=[0.8, dop.max() * 1.08])
    _title(fig, label)
    return _style(fig, "Minutes of scrolling")


# ---------------------------------------------------------------------------
# 5. alcohol — the overnight rebound: calm now, edge ~8h later
# ---------------------------------------------------------------------------

def overnight_rebound_figure(preset, intensity, label) -> go.Figure:
    t = np.linspace(0, 24, 800)
    scale = sim.intensity_scale(intensity)
    calm = -preset.get("gaba_agonism", 0.85) * scale * _gauss(t, 2.5, 1.9)
    rebound = preset.get("glutamate_rebound", 0.9) * scale * _gauss(t, 11.0, 3.0)
    arousal = calm + rebound

    calm_part = np.minimum(arousal, 0.0)
    edge_part = np.maximum(arousal, 0.0)

    fig = go.Figure()
    fig.add_hline(y=0.0, line=dict(color=GREY, width=1.5, dash="dash"),
                  annotation_text="your normal", annotation_position="top left")
    fig.add_trace(go.Scatter(x=t, y=calm_part, line=dict(width=0),
                             fill="tozeroy", fillcolor=CALM_FILL))
    fig.add_trace(go.Scatter(x=t, y=edge_part, line=dict(width=0),
                             fill="tozeroy", fillcolor=WARM_FILL))
    fig.add_trace(go.Scatter(x=t, y=arousal, line=dict(color=BLUE, width=3)))
    fig.add_annotation(x=2.5, y=float(arousal.min()), text="tonight: nerves quiet",
                       showarrow=True, arrowhead=0, ax=0, ay=28, font=dict(color=BLUE, size=12))
    fig.add_annotation(x=11.0, y=float(arousal.max()), text="next morning: on edge",
                       showarrow=True, arrowhead=0, ax=0, ay=-26, font=dict(color=AMBER, size=12))
    _title(fig, label)
    return _style(fig, "Hours (0 = first drink · ~8h = next morning)")


# ---------------------------------------------------------------------------
# 6. caffeine — the energy loan: borrowed now, paid back later
# ---------------------------------------------------------------------------

def energy_loan_figure(preset, intensity, label) -> go.Figure:
    t = np.linspace(0, 12, 600)
    scale = sim.intensity_scale(intensity)
    boost = 0.42 * scale * _gauss(t, 1.0, 1.1)
    peak = 6.5
    gamma = np.where(t > 0, (t / peak) * np.exp(1 - t / peak), 0.0)
    debt = -0.48 * scale * gamma
    awake = boost + debt

    borrowed = np.maximum(awake, 0.0)
    paid = np.minimum(awake, 0.0)

    fig = go.Figure()
    fig.add_hline(y=0.0, line=dict(color=GREY, width=1.5, dash="dash"),
                  annotation_text="your normal energy", annotation_position="top right")
    fig.add_trace(go.Scatter(x=t, y=borrowed, line=dict(width=0),
                             fill="tozeroy", fillcolor=WARM_FILL))
    fig.add_trace(go.Scatter(x=t, y=paid, line=dict(width=0),
                             fill="tozeroy", fillcolor=CALM_FILL))
    fig.add_trace(go.Scatter(x=t, y=awake, line=dict(color=BLUE, width=3)))
    fig.add_annotation(x=1.0, y=float(awake.max()), text="energy borrowed now",
                       showarrow=False, yshift=14, font=dict(color=AMBER, size=12))
    fig.add_annotation(x=peak, y=float(awake.min()), text="the same energy, paid back later",
                       showarrow=False, yshift=-14, font=dict(color=BLUE, size=12))
    _title(fig, label)
    return _style(fig, "Hours since the cup")


_DISPATCH = {
    "two_peaks": lambda p, i, n, l: two_peaks_figure(p, i, l),
    "escalation": lambda p, i, n, l: escalation_figure(p, i, n, l),
    "sinking_floor": lambda p, i, n, l: sinking_floor_figure(p, i, l),
    "no_satiety": lambda p, i, n, l: no_satiety_figure(p, i, l),
    "overnight_rebound": lambda p, i, n, l: overnight_rebound_figure(p, i, l),
    "energy_loan": lambda p, i, n, l: energy_loan_figure(p, i, l),
}


def signature_figure(loop_key, preset, intensity=5.0, n_episodes=0.0):
    """Return this loop's signature figure, or None if it has no story (generic)."""
    story = get_story(loop_key)
    if not story:
        return None
    builder = _DISPATCH.get(story["kind"])
    if builder is None:
        return None
    return builder(preset, intensity, n_episodes, story["signature_label"])


# ---------------------------------------------------------------------------
# Detailed timeline (moves into the "Show the detail" expander)
# ---------------------------------------------------------------------------

PHASE_COLORS = {"trigger": PURPLE, "peak": BLUE, "crash": RED, "vulnerable": AMBER}


def detail_timeline_figure(timeline: dict, phases: list) -> go.Figure:
    t = timeline["t"]
    fig = go.Figure()
    vuln = next((p for p in phases if p.key == "vulnerable"), None)
    if vuln is not None:
        fig.add_vrect(x0=vuln.t_start, x1=vuln.t_end, fillcolor=LOW_FILL,
                      line_width=0, layer="below")
    fig.add_trace(go.Scatter(x=t, y=timeline["baseline"], name="your baseline",
                             line=dict(color=GREY, width=1.5, dash="dash")))
    fig.add_trace(go.Scatter(x=t, y=timeline["dopamine"], name="dopamine",
                             line=dict(color=BLUE, width=3)))
    fig.add_trace(go.Scatter(x=t, y=timeline["cortisol"], name="cortisol (stress)",
                             line=dict(color=AMBER, width=2, dash="dot")))
    heights = [1.10, 1.02, 1.10, 1.02]
    for i, p in enumerate(phases):
        fig.add_annotation(x=p.t_marker, y=heights[i % len(heights)], yref="paper",
                           showarrow=False, text=f"<b>{p.label}</b>",
                           font=dict(color=PHASE_COLORS[p.key], size=12))
        fig.add_vline(x=p.t_marker, line=dict(color=PHASE_COLORS[p.key], width=1, dash="dot"),
                      opacity=0.4)
    fig.update_layout(
        height=420, margin=dict(l=10, r=10, t=52, b=10),
        xaxis_title="Hours since the cue", yaxis_title="Level (relative to baseline)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.28, x=0), hovermode="x unified",
    )
    return fig
