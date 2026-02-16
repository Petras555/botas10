from run_bot import farm_from_url
from sandelys import warehouse_monitor_loop
from utilities import random_delay, config, load_farms, check_warehouse_capacity
from playwright.sync_api import sync_playwright
import random, time




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

    check_warehouse_capacity(page)

    

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

        while True: 
            random.shuffle(farm_urls)
            for url in farm_urls:
                try:
                    farm_from_url(page, url, config)
                    time.sleep(random.randint(3, 6))
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    browser_instance = None

            warehouse_monitor_loop(page)

            sleep_minutes = random.randint(20, 25)
            print(f"Cycle finished. Sleeping {sleep_minutes} minutes...")
            time.sleep(sleep_minutes * 60)



