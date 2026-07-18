"""Every non-generic preset has a complete story with a renderable signature."""

import numpy as np
import pytest

from loop.presets import PRESET_ORDER, get_preset
from loop.stories import LOOP_STORIES, get_story
from loop import charts

REQUIRED = [
    "kind", "headline", "one_line", "trigger", "peak", "crash", "vulnerable",
    "what_this_means", "signature_label", "detail_note",
]


@pytest.mark.parametrize("key", PRESET_ORDER)
def test_every_preset_has_a_story(key):
    story = get_story(key)
    assert story is not None, f"{key} has no story"
    for field in REQUIRED:
        assert story.get(field), f"{key} story missing {field}"


@pytest.mark.parametrize("key", PRESET_ORDER)
def test_signature_figure_builds(key):
    fig = charts.signature_figure(key, get_preset(key), intensity=6, n_episodes=100)
    assert fig is not None, f"{key} produced no signature figure"
    assert fig.data, f"{key} signature figure has no traces"


@pytest.mark.parametrize("key", PRESET_ORDER)
def test_signature_kind_is_dispatchable(key):
    assert LOOP_STORIES[key]["kind"] in charts._DISPATCH


def test_generic_has_no_signature():
    from loop.presets import GENERIC_KEY
    assert charts.signature_figure(GENERIC_KEY, get_preset(GENERIC_KEY)) is None


def test_headline_lengths_reasonable():
    for key, story in LOOP_STORIES.items():
        assert len(story["headline"]) <= 60, f"{key} headline too long"
