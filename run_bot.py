from scraper import scrape_general, scrape_last_raid  
from backoffice.models import Fermos
from utilities import random_delay, config
import re

browser = None


def percentage_from_string(resource_cap):
    clean_resource_cap = re.sub(r'[^\d/]', '', resource_cap)
    try:
        value_str, limit_str = clean_resource_cap.split("/")
        value = int(value_str.strip())
        limit = int(limit_str.strip())

        if limit == 0:
            return 0

        return round((value / limit) * 100, 2)
    except Exception as e:
        raise ValueError(f"Invalid format: {resource_cap}") from e

def close_overlays(page):
    """Close any popups or overlays that block clicks"""
    try:
        page.locator(".dialogOverlay .closeButton").first.click(timeout=1000)
        print("Overlay closed")
        random_delay(300, 800)
    except:
        pass  # no overlay found

def farm_from_url(page, url, config):
    print(f"Farming: {url}")
    farm_status = Fermos.objects.filter(url=url).values_list('farm_status', flat=True).first()
    if farm_status is False:
        print(f"Skipping farm {url} (farm status is False)")
        return
    page.goto(url)
    random_delay()
    scrape_general(page, url)

    close_overlays(page)
    scrape_last_raid(page, url)
    random_delay()

    resource_cap = Fermos.objects.filter(url=url).values_list('resource_cap', flat=True).first()

    if resource_cap:
        try:
            percentage = percentage_from_string(resource_cap)
            print(f"URL: {url} - Resource Cap: {resource_cap} - Percentage: {percentage}%")
        except ValueError as e:
            print(f"Error processing URL {url}: {e}")
    else:
        print(f"URL: {url} - No resource cap found")

    page.goto(url)

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
        
        if percentage > 90:
            print("Sending 50% more troops due to high resource cap percentage")            
            # reik padirbet, reikia profilyje tureti multiplyeri troopsu siuntimui!!!!!!!!!!!

            # padauginimas, neleidzia INT irasyti browseryje
            amount = str(config["TROOP_AMOUNT"] * 1.5)

            page.locator(f'input[name="troop[{config["TROOP_ID"]}]"]').fill(amount)
            random_delay()
        else:
            print("Sending normal amount of troops")   
            page.locator(f'input[name="troop[{config["TROOP_ID"]}]"]').fill(str(config["TROOP_AMOUNT"]))
            random_delay()


        page.get_by_role("button", name="Send").click()
        random_delay()

        page.get_by_role("button", name="Confirm").click()
        random_delay()

        print("Attack sent")
    except Exception as e:
        print(f"Failed to send troops on {url} | {e}")




        