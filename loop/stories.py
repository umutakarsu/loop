"""Per-loop story content — the "richer" half of "richer, but simpler UI".

Each loop gets its own plain-language story (headline, one-line, four phase
captions, a "what this means" reframe) plus its own signature-visual `kind` and
one plain chart label, and a `detail_note` with the real science for the
"Show the detail" expander.

Surface fields are deliberately jargon-free (a stressed non-expert should get
them in seconds); clinical terms live only in `detail_note`. Every string was
adversarially checked against the §6 tone rules and the preset pharmacology.
This is the single place to edit user-facing loop copy; it is kept separate from
copy.py (chrome strings) only for size. Both obey the §6 tone rules — enforced
by tests/test_copy_tone.py, which scans this module too.
"""

from __future__ import annotations

# signature-visual kinds map to renderers in loop/charts.py
LOOP_STORIES: dict[str, dict] = {
    "binge_eating": {
        "kind": "two_peaks",
        "dopamine_primary": True,
        "main_driver": "",
        "headline": "Your brain wants it more than it enjoys it.",
        "one_line": "The build-up feels huge, the actual eating feels smaller, and then you drop below where you started.",
        "trigger": "Something sets it off — a mood, a time of day, a place. Before you've eaten a single bite, the pull is already climbing. That rising feeling is the wanting, and it shows up first.",
        "peak": "You eat. The relief and the rush do arrive — but they land smaller and fade faster than the build-up promised. The moment you were chasing turns out to be quieter than the chase.",
        "crash": "About an hour later you dip below where you started — flatter, emptier, lower than before any of it began, and a wave of stress or self-criticism can roll in on top. This dip is the part that usually gets blamed on willpower.",
        "vulnerable": "For much of the next day your baseline sits low. That's exactly when the next trigger has the most power — not because something's wrong with you, but because the curve is at its lowest point and hasn't climbed back yet.",
        "what_this_means": "This loop has a predictable shape, and none of it means you're weak or broken. Seeing where you are on the curve — the big build-up, the smaller payoff, the dip afterward — is a completely different thing from being run by it.",
        "signature_label": "The build-up is taller than the payoff.",
        "detail_note": "Mechanistically this is a wanting-over-liking dissociation (Berridge's incentive-salience framing). Anticipatory mesolimbic dopamine spikes to ~1.6× baseline before consumption and exceeds the consummatory dopamine response (~1.3×) — the cue-driven \"wanting\" signal is larger than the reward actually delivers. At consumption, β-endorphin (opioid) release (~0.8) supplies the brief hedonic \"relief.\" Then Solomon & Corbit's opponent-process kicks in: the compensatory b-process drives dopamine into an undershoot (~0.55× baseline) around 60 min post-episode. A cortisol rebound (~0.75) — the post-episode stress/shame spike — follows, and elevated cortisol reduces prefrontal control, which is what raises the odds the next cue succeeds. Across repetitions, allostatic load (Koob & Le Moal) erodes the baseline downward (~0.03 per episode), so the whole curve gradually resets lower. Full recovery toward baseline takes ~18 hours.",
    },
    "porn": {
        "kind": "escalation",
        "dopamine_primary": True,
        "main_driver": "",
        "headline": "Each time, it takes more to feel the same.",
        "one_line": "A huge, fast spike — then a drop below where you started, and next time the bar sits higher.",
        "trigger": "Something grabs your attention and the pull kicks in. What drives this loop more than most is the chase for something new — and the wanting climbs before anything has actually happened.",
        "peak": "This is the biggest spike of any loop in here — and it's over fast. A lot shorter than it feels while it's happening.",
        "crash": "Almost right away it drops, and not back to normal — below where you started. Flat, foggy, a little empty. This is the part that usually gets blamed on you.",
        "vulnerable": "For a long stretch afterward — longer than most loops, up to about a day and a half — you're running below your normal. That flat, low feeling is exactly when a fresh cue has the most pull. That's the shape of the curve, not a flaw in you.",
        "what_this_means": "Needing something newer to get the same hit, and the flat feeling afterward, aren't signs of weakness — they're the predictable shape of this particular curve. Once you can see the low coming, it stops being a mystery or a verdict on you.",
        "signature_label": "Next time has to climb higher — and still lands lower.",
        "detail_note": "This loop is defined by two mechanisms rarely explained well. First, novelty escalation via the Coolidge effect: the dopaminergic response habituates to familiar stimuli, so each repetition recruits a higher novelty requirement to reach the same peak — modelled here as the fastest tolerance accumulation of the six presets (baseline erosion ~0.05 per episode). Second, a prolactin surge at orgasm drives an unusually fast (~20 min) and deep post-peak anhedonia plus refractory period; the dopamine undershoot (crash depth ~0.45 of baseline) is steeper than the other loops and recovery is longer (~36h). The theoretical frame is Solomon & Corbit's opponent-process theory — the opponent b-process, the below-baseline state, grows and lingers with repetition — layered with Koob & Le Moal's allostatic model, in which the hedonic set-point drifts downward across episodes. The very high anticipation spike (1.9× baseline) sitting just under an even higher consumption spike (2.2×) reflects a wanting-versus-liking dissociation that novelty keeps inflating.",
    },
    "nicotine": {
        "kind": "sinking_floor",
        "dopamine_primary": True,
        "main_driver": "",
        "headline": "Each hit fixes the craving the last one caused.",
        "one_line": "It doesn't lift you above normal — it lowers your normal, so each one just hauls you back up.",
        "trigger": "A few hours since the last one, and a low restlessness starts to build. Then a coffee, a step outside, a stressful minute — and the pull is already there before you've reached for anything.",
        "peak": "It lands in about seven seconds — faster than any other loop. But the spike is smaller than it feels. Most of what you notice isn't a high, it's the restlessness going quiet.",
        "crash": "Within the hour it clears and you settle a little below where you started. That dip is the next craving quietly being built. It's the part that gets blamed on willpower — it's really just the curve on its way back down.",
        "vulnerable": "Around three hours out, your normal is at its lowest and the pull is at its strongest. This is when the next one has the most power — not because something's wrong with you, but because this is the bottom of the dip.",
        "what_this_means": "Most of the pull isn't the pleasure of the next one — it's the discomfort the last one left behind. Once you can see that the \"reward\" is mostly just relief, the loop stops looking like a flaw and starts looking like a shape you can recognise.",
        "signature_label": "The high is just getting back to normal — and normal keeps sinking.",
        "detail_note": "Nicotine is the fastest-delivering loop here: an arterial bolus reaches the brain in 7-10 seconds, and that steep rate-of-rise is itself strongly reinforcing. But the defining mechanism isn't the peak — it's negative reinforcement. Chronic exposure upregulates nicotinic acetylcholine receptors (nAChR density climbs); when those extra receptors sit unoccupied between hits, they generate craving and dysphoria. This is textbook opponent-process theory (Solomon & Corbit, 1974): the b-process — the withdrawal counter-reaction — grows with repetition until it dominates the a-process (the reward). In allostatic terms (Koob & Le Moal, 2001), the reward set-point drifts downward, so the affective baseline itself resets lower. With a ~2h half-life, levels fall enough within 1-3 hours to open the withdrawal trough — the \"I need one\" point. The consequence, and the whole visual: the consumption spike (~1.9× the current baseline) increasingly just restores the eroded baseline rather than delivering net pleasure. Over a day of repeated hits the floor sinks and each hit only claws back toward where \"normal\" used to be — the loop is relieving the withdrawal it created.",
    },
    "doomscrolling": {
        "kind": "no_satiety",
        "dopamine_primary": True,
        "main_driver": "",
        "headline": "Your brain never gets the signal to stop.",
        "one_line": "Each swipe is a tiny maybe-reward and the feed never ends, so nothing ever tells you you're done.",
        "trigger": "A dull second, a notification, a queue to stand in, and your thumb has opened the app before you've decided anything.",
        "peak": "There's no single big hit here, just dozens of small ones. Each post lands a little smaller than you hoped, so you reach for the next. And the next.",
        "crash": "You finally put it down and feel flatter and more on-edge than before you picked it up, dropped below where you started rather than lifted.",
        "vulnerable": "For a while after, you sit at your lowest: restless, a bit wired, a bit tense. That's exactly the moment the next pull-to-refresh has the most power.",
        "what_this_means": "You didn't run out of willpower. The feed is built with no finish line and no \"you're full\" moment, so the off switch was never there to find. Seeing that the stop signal is missing by design, not broken in you, is what hands the decision back to you.",
        "signature_label": "Every other craving has a \"full\" line that says stop. Here it stays flat, so nothing ever does.",
        "detail_note": "Doomscrolling runs on a variable-ratio reinforcement schedule — the same intermittent-reward structure as a slot machine, and the most persistence-generating schedule known. The individual dopamine events are small (anticipation ~1.15×, consumption ~1.25× baseline) but arrive fast, ~4 per minute, and their unpredictable payoff is what sustains the behaviour. The defining feature is satiety_signal = 0.0: unlike eating (leptin, CCK, gastric distension) or sexual behaviour (post-orgasmic prolactin surge driving a refractory, anhedonic window), an infinite feed provides no homeostatic or consummatory termination signal, so the reward-seeking a-process is never switched off from within. Threat- and outrage-weighted content keeps the amygdala–HPA axis engaged, producing a sustained cortisol rebound (~0.8) rather than a clean return to rest. Per Solomon & Corbit's opponent-process theory, the compensatory b-process (the crash) grows with repeated activation; per Koob & Le Moal's allostatic model, the reward set-point drifts downward with each episode (tolerance ~0.015/episode). The net result modelled here is an undershoot to ~0.7 of baseline around 90 minutes, with recovery over roughly 8 hours — the sinking baseline under the spikes is that allostatic drift.",
    },
    "alcohol": {
        "kind": "overnight_rebound",
        "dopamine_primary": False,
        "main_driver": "GABA calm, then a glutamate rebound",
        "headline": "The calm tonight becomes the edge tomorrow morning.",
        "one_line": "It turns the volume down on your nerves tonight, so they come back up louder in the morning.",
        "trigger": "Something signals it's time — the end of a long day, a social thing, a knot of stress — and the pull to take the edge off shows up before the first sip.",
        "peak": "For a while, the volume drops. Your nerves go quiet, your shoulders come down, the day's sharp edges soften.",
        "crash": "As it wears off, the calm doesn't just fade back to normal — it overshoots, and you end up more wired than before you started.",
        "vulnerable": "Roughly eight hours on — usually the next morning — you're at your most on-edge. That low, jittery point is exactly when starting the loop again feels most reasonable.",
        "what_this_means": "The morning-after anxiety isn't proof that something's wrong with you — it's your brain swinging back the other way to even out last night's calm, and it moves in a shape you can see coming. Once you know the spike is part of the loop, it has a little less grip.",
        "signature_label": "This morning's edge is last night's calm, paid back on a delay.",
        "detail_note": "Ethanol acts as a positive allosteric modulator at GABA-A receptors (gaba_agonism ~0.85), boosting the brain's main inhibitory \"brake\" — that's the acute anxiolytic calm. The CNS compensates homeostatically: it downregulates GABA tone and upregulates excitatory glutamate/NMDA signalling. As blood alcohol clears (peak ~45 min, then near-zero-order elimination — the metabolising enzyme alcohol dehydrogenase saturates almost immediately, so ethanol is cleared at a roughly constant ~one-standard-drink-per-hour rate rather than in proportion to its concentration), the GABA boost vanishes but the compensatory glutamate excitation is left unopposed, producing an arousal rebound ABOVE baseline roughly 8 hours later — the \"hangxiety\" (glutamate_rebound ~0.9). This is a textbook opponent-process (Solomon & Corbit, 1974): the b-process rebound rises slower, decays slower, and grows with repetition. A cortisol rebound (~0.85) from HPA-axis activation and disrupted REM sleep layers on top, sharpening the morning anxiety. Across repeated episodes the allostatic model (Koob & Le Moal, 2001) predicts the resting set-point itself drifts downward (tolerance_per_episode ~0.025), so the same calm needs more, and each rebound starts from a lower, more anxious baseline. Full return to baseline takes ~48 hours.",
    },
    "caffeine": {
        "kind": "energy_loan",
        "dopamine_primary": False,
        "main_driver": "adenosine (blocked, not boosted)",
        "headline": "You're borrowing energy, not making it.",
        "one_line": "Caffeine doesn't add energy — it hides the tiredness you already have, then hands it back later.",
        "trigger": "The afternoon slump hits — or it's just the time you always have one — and you reach for the cup before you've really decided to.",
        "peak": "About 45 minutes in, you feel sharp and clear again. Nothing was actually added — the tiredness is just muffled for a while.",
        "crash": "Around five hours later the cup wears off, and all that muffled tiredness arrives at once — sometimes leaving you flatter than before you drank it.",
        "vulnerable": "This dip is exactly when another cup calls the loudest. And a late one is still working at bedtime — so tomorrow starts more tired, and the next cup has even more to cover.",
        "what_this_means": "The lift is real, but it's a loan against energy you already had — not a fresh supply. Seeing the afternoon dip as tiredness arriving on schedule, rather than you running low on willpower, is a different story about the same moment.",
        "signature_label": "You didn't make new energy — you moved it to later.",
        "detail_note": "Unlike most loops in this tool, caffeine is not primarily dopaminergic (mild anticipation/consumption bumps of ~1.1×/1.3× exist but are secondary). Its main action is adenosine-receptor antagonism. Adenosine accumulates across the waking day as a byproduct of ATP metabolism and binds A1/A2A receptors to build \"sleep pressure\" — the felt sense of tiredness. Caffeine competitively blocks those receptors, so the sleep-pressure signal is masked, not removed: adenosine keeps climbing behind the blockade (the adenosine debt). With a ~5.5-hour half-life, as caffeine clears the accumulated adenosine floods the now-unblocked receptors, producing the crash roughly five hours out (undershoot ~0.75 of baseline). In opponent-process terms (Solomon & Corbit, 1974), the alertness \"a-process\" is opposed by a growing fatigue \"b-process\" that outlasts it. Late-day dosing extends into sleep architecture — reduced slow-wave sleep — which raises the next day's starting adenosine load; across repetition, receptor upregulation drives tolerance and an allostatic downward shift in baseline (Koob & Le Moal, 2001). Hence \"borrowed, not created\": no energy is generated, fatigue is time-shifted and, with interest, compounded.",
    },
}


def get_story(loop_key: str) -> dict | None:
    """Return the story dict for a loop key, or None (e.g. the generic template)."""
    return LOOP_STORIES.get(loop_key)
