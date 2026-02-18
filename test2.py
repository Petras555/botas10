# from flee import avoid_attack
# import run_bot, scraper
# from run_bot import farm_from_url
# from sandelys import warehouse_monitor_loop
# from utilities import random_delay, config, load_farms
# from playwright.sync_api import sync_playwright, Playwright
import random, time, re



# def login(page):
#     page.goto("https://www.travian.com/international")
#     page.get_by_role("button", name="Login").click()

#     random_delay()
#     page.get_by_role("textbox", name="Enter your email address or").fill(config["EMAIL"])
#     random_delay()
#     page.get_by_role("textbox", name="Enter your password:").fill(config["PASSWORD"])
#     random_delay()

#     page.locator("#loginLobby").get_by_role("button", name="Login").click()
#     random_delay(2000, 3000)

#     page.get_by_role("button", name="Play now").click()
#     random_delay(3000, 5000)


# def check_warehouse_capacity(page):
#     raw_text = page.locator("css=#stockBar > div.warehouse > div > div").inner_text()
#     clean_text = re.sub(r'[^\d,.\s]', '', raw_text).strip()
#     print(f"Warehouse capacity: {clean_text}")

# def start_the_loop():
#     global browser
#     with sync_playwright() as playwright:
#         browser = playwright.chromium.launch(headless=False, slow_mo=300)
#         context = browser.new_context()
#         page = context.new_page()

#         login(page)

#         random_delay()

#         # check_warehouse_capacity(page)
#         avoid_attack(page)

# if __name__ == "__main__":
#     start_the_loop()

start_time = time.time()
print(start_time)
