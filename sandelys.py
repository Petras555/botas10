from playwright.sync_api import sync_playwright, TimeoutError
import time
from datetime import datetime
import re
from utilities import config


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def clean_number(text):
    return int(re.sub(r"[^\d]", "", text))


def get_resources(page):
    try:
        page.locator("#l1").wait_for(state="visible", timeout=10000)
        page.locator("#l2").wait_for(state="visible", timeout=10000)
        page.locator("#l3").wait_for(state="visible", timeout=10000)

        wood = clean_number(page.locator("#l1").inner_text())
        clay = clean_number(page.locator("#l2").inner_text())
        iron = clean_number(page.locator("#l3").inner_text())
        return wood, clay, iron
    except TimeoutError:
        print(f"[{now()}] Error reading resources")
        return 0, 0, 0

def warehouse_almost_full(page):
    wood, clay, iron = get_resources(page)
    limit = config["WAREHOUSE_CAPACITY"] * config["RESOURCE_TRIGGER"]
    return wood >= limit or clay >= limit or iron >= limit

def train_equites_imperatoris(page):
    wood, clay, iron = get_resources(page)
    print(f"[{now()}] Warehouse high → attempting to train EI")
    print(f"[{now()}] Resources before training: W:{wood} C:{clay} I:{iron}")

    page.goto(config["STABLE_URL"])
    try:
        input_box = page.locator(f'input[name*="{config["TROOP_NAME"]}"]')
        input_box.wait_for(state="visible", timeout=10000)
        input_box.fill(str(config["EI_TRAIN_AMOUNT"]))

        train_button = page.locator('button:has-text("Train")')
        if train_button.is_enabled():
            train_button.click()
            print(f"[{now()}] Successfully queued {config['EI_TRAIN_AMOUNT']} Equites Imperatoris\n")
        else:
            print(f"[{now()}] Train button not enabled. Possibly insufficient resources.\n")
    except TimeoutError:
        print(f"[{now()}] Could not find input or train button\n")
    except Exception as e:
        print(f"[{now()}] Training failed: {e}\n")

def warehouse_monitor_loop(page):
    if warehouse_almost_full(page):
        train_equites_imperatoris(page)
    else:
        wood, clay, iron = get_resources(page)
        print(f"[{now()}] Warehouse OK, no training needed → W:{wood} C:{clay} I:{iron}\n")

