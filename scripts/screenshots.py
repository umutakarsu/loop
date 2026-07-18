"""Drive the running Loop app with Playwright and capture screenshots.

Assumes Streamlit is serving at $LOOP_URL (default http://localhost:8531).
Captures screen 1 plus the narrated screen (screen 3) for every preset, so each
loop's signature visual can be eyeballed. Usage: python scripts/screenshots.py
"""
import os
import pathlib

from playwright.sync_api import sync_playwright

URL = os.environ.get("LOOP_URL", "http://localhost:8531")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
OUT = pathlib.Path(os.environ.get("SHOT_DIR", "docs/screenshots"))
OUT.mkdir(parents=True, exist_ok=True)

PRESETS = [
    ("Binge eating", "binge"),
    ("Porn", "porn"),
    ("Nicotine / vaping", "nicotine"),
    ("Doomscrolling", "doomscrolling"),
    ("Alcohol", "alcohol"),
    ("Caffeine", "caffeine"),
]


def settle(page, ms=1500):
    page.wait_for_timeout(ms)


def click_text(page, text):
    page.get_by_text(text, exact=False).first.click()
    settle(page)


def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])

        # Screen 1
        page = browser.new_page(viewport={"width": 900, "height": 1300})
        page.goto(URL, wait_until="networkidle")
        settle(page, 2500)
        page.screenshot(path=str(OUT / "01_pick.png"), full_page=True)
        page.close()

        for label, slug in PRESETS:
            page = browser.new_page(viewport={"width": 900, "height": 1500})
            page.goto(URL, wait_until="networkidle")
            settle(page, 2500)
            click_text(page, label)
            click_text(page, "Show me the curve")
            settle(page, 2000)
            page.screenshot(path=str(OUT / f"loop_{slug}.png"), full_page=True)
            page.close()

        browser.close()
        print("screenshots written to", OUT)


if __name__ == "__main__":
    run()
