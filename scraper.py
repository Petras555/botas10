import os
import django
import random
import time
import json
from playwright.sync_api import sync_playwright

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
# --- DJANGO SETUP ---
# Replace 'your_project_name' with the actual folder name containing your settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Import your model after django.setup()
from backoffice.models import Fermos 
# --------------------

with open("config.json") as f:
    config = json.load(f)

def load_farms(filename="farms.txt"):
    if not os.path.exists(filename): return []
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def login(page):
    page.goto("https://www.travian.com/international")
    page.get_by_role("button", name="Login").click()
    time.sleep(2)
    page.get_by_role("textbox", name="Enter your email address or").fill(config["EMAIL"])
    page.get_by_role("textbox", name="Enter your password:").fill(config["PASSWORD"])
    page.locator("#loginLobby").get_by_role("button", name="Login").click()
    time.sleep(5)
    page.get_by_role("button", name="Play now").click()
    time.sleep(5)

def scrape():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context()
        page = context.new_page()

        login(page)
        farm_urls = load_farms("farms.txt")

        for url in farm_urls:
            print(f"Scraping {url} ...")
            try:
                page.goto(url, timeout=15000)
                time.sleep(2)

                # Scrape data
                player_name = page.locator("css=#village_info > tbody > tr:nth-child(3) > td > a").inner_text().strip()
                village_name = page.locator("css=#tileDetails > h1").inner_text().strip().split("\u202d")[0].strip()
                tribe = page.locator("css=#village_info > tbody > tr.first > td").inner_text().strip()
                alliance = page.locator("css=#village_info > tbody > tr:nth-child(2) > td > a").inner_text().strip()
                population = page.locator("css=#village_info > tbody > tr:nth-child(4) > td").inner_text().strip()


                # --- SAVE TO SQLITE VIA DJANGO ---
                # update_or_create prevents duplicate entries if the URL is the same
                obj, created = Fermos.objects.update_or_create(
                    url=url,
                    defaults={
                        'player_name': player_name,
                        'village_name': village_name,
                        'tribe': tribe,
                        'alliance': alliance,
                        'population': int(population) if population.isdigit() else 0,
                        'url': url
                    }
                )
                #troop_info > tbody > tr:nth-child(1) > td > a:nth-child(2)
                status = "Created" if created else "Updated"
                print(f"✅ {status} record for {player_name}")

                population = page.locator("css=#troop_info > tbody > tr:nth-child(1) > td > a:nth-child(2)").click()
                lumber = page.locator("css=#reportWrapper > div.body > div.role.attacker > table.additionalInformation > tbody > tr > td > div > div.res > div > div:nth-child(1) > span").inner_text().strip()
                clay = page.locator("css=#reportWrapper > div.body > div.role.attacker > table.additionalInformation > tbody > tr > td > div > div.res > div > div:nth-child(2) > span").inner_text().strip()
                iron = page.locator("css=#reportWrapper > div.body > div.role.attacker > table.additionalInformation > tbody > tr > td > div > div.res > div > div:nth-child(3) > span").inner_text().strip()
                crop = page.locator("css=#reportWrapper > div.body > div.role.attacker > table.additionalInformation > tbody > tr > td > div > div.res > div > div:nth-child(4) > span").inner_text().strip()
                resource_cap = page.locator("css=#reportWrapper > div.body > div.role.attacker > table.additionalInformation > tbody > tr > td > div > div.inlineIcon.carry > span").inner_text().strip()

                obj, created = Fermos.objects.update_or_create(
                    url=url,
                    defaults={
                        'lumber': lumber,
                        'clay': clay,
                        'iron': iron,
                        'crop': crop,
                        'resource_cap': resource_cap
                    }
                )
                
            except Exception as e:

                print(f"Failed to scrape {url}: {e}")

        context.close()
        browser.close()

if __name__ == "__main__":
    scrape()