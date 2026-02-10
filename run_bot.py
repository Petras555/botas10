import random
import time
import os
from playwright.sync_api import sync_playwright, Playwright
import json

browser = None

with open("config.json") as f:
    config = json.load(f)

def random_delay(min_ms=500, max_ms=1500):
    time.sleep(random.uniform(min_ms, max_ms) / 1000)

def load_farms(filename="farms.txt"):
    farms = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            farms.append(line)
    return farms

def close_overlays(page):
    """Close any popups or overlays that block clicks"""
    try:
        page.locator(".dialogOverlay .closeButton").first.click(timeout=1000)
        print("Overlay closed")
        random_delay(300, 800)
    except:
        pass  # no overlay found

def farm_from_url(page, url):
    print(f"Farming: {url}")
    page.goto(url)
    random_delay()

    # CLOSE ANY OVERLAYS
    close_overlays(page)

    # Wait for the village element and click it (force=True bypasses blockers)
    try:
        village = page.locator("#mapContainer > div > div:nth-child(2)").first
        village.wait_for(state="visible", timeout=5000)
        village.click(force=True)
        random_delay()
    except:
        print("Village click failed, skipping farm")
        return

    try:
        page.get_by_role("link", name="Send troops", exact=True).click()
        random_delay()

        page.locator(f'input[name="troop[{config["TROOP_ID"]}]"]').fill(str(config["TROOP_AMOUNT"]))
        random_delay()

        page.get_by_role("button", name="Send").click()
        random_delay()

        page.get_by_role("button", name="Confirm").click()
        random_delay()

        print("Attack sent")
    except Exception as e:
        print(f"Failed to send troops on {url} | {e}")

def login(page):
    page.goto("https://www.travian.com/international")
    page.get_by_role("button", name="Login").click()

    random_delay()
    page.get_by_role("textbox", name="Enter your email address or").fill(config["EMAIL"])
    random_delay()
    page.get_by_role("textbox", name="Enter your password:").fill(config["PASSWORD"])
    random_delay()

    page.locator("#loginLobby").get_by_role("button", name="Login").click()
    random_delay(2000, 3000)

    page.get_by_role("button", name="Play now").click()
    random_delay(3000, 5000)

def kill_browser():
    global browser
    browser.close()
    print("Playwright browser closed via stop button.")


def start_the_loop():
    global browser
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context()
        page = context.new_page()

        login(page)
        farm_urls = load_farms("farms.txt")

        while True:  # <--- YOUR LOOP
            random.shuffle(farm_urls)
            for url in farm_urls:
                try:
                    farm_from_url(page, url)
                    time.sleep(random.randint(3, 6))
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    browser_instance = None

            sleep_minutes = random.randint(20, 25)
            print(f"Cycle finished. Sleeping {sleep_minutes} minutes...")
            time.sleep(sleep_minutes * 60)
 