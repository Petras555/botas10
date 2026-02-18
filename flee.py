import time
from utilities import random_delay

def time_to_seconds(t: str) -> int:
    h, m, s = map(int, t.split(":"))
    return h * 3600 + m * 60 + s

limit = "0:00:50"

def avoid_attack(page):
    page.goto("https://nys.x5.international.travian.com/dorf1.php")
    print("prasided avoid")
    try:
        time_until_attack = page.locator("css=#movements > tbody > tr:nth-child(2) > td:nth-child(2) > div.dur_r > span").inner_text()
        print(f"Time until attack: {time_until_attack}")

        if time_to_seconds(time_until_attack) < time_to_seconds(limit):
            print("⚠️ Attack incoming, skipping farm and sending troops to defend")
            # human like reik kad graziai nukeliaut
            page.goto("https://nys.x5.international.travian.com/build.php?gid=16&tt=2&eventType=5&targetMapId=34971")
            page.locator("css=#troops > tbody > tr:nth-child(1) > td.line-first.column-first.large > span").click()
            page.locator("css=#troops > tbody > tr:nth-child(2) > td.column-first.large > a").click()
            page.locator("css=#troops > tbody > tr:nth-child(3) > td.line-last.column-first.large > a").click()
            page.locator("css=#troops > tbody > tr:nth-child(1) > td:nth-child(2) > a").click()
            page.locator("css=#troops > tbody > tr:nth-child(2) > td:nth-child(2) > a").click()
            page.locator("css=#troops > tbody > tr:nth-child(3) > td:nth-child(2) > span").click()
            page.locator("css=#troops > tbody > tr:nth-child(1) > td.line-first.regular > span").click()
            page.locator("css=#troops > tbody > tr:nth-child(2) > td.regular > span").click()
            page.locator("css=#troops > tbody > tr:nth-child(1) > td.line-first.column-last.small > span").click()
            page.locator("css=#troops > tbody > tr:nth-child(2) > td.column-last.small > span").click()
            page.locator("css=#troops > tbody > tr:nth-child(3) > td.line-last.column-last.small > a").click()
            page.locator("css=#troops > tbody > tr:nth-child(2) > td.column-last.small > span").click()
            page.get_by_role("button", name="Send").click()
            page.get_by_role("button", name="Confirm").click()


            time.sleep(40)
            page.locator("css=#build > div.data.rallyPointOverviewContainer > table.troop_details.outRaid > tbody.infos > tr > td > div.abort > button").click()
    
        else:
            time.sleep(10)
            print("No attack incoming, continuing with farming")

    except Exception as e:
        print(f"Error in avoid_attack: {e}")

        #build > div.data.rallyPointOverviewContainer > table.troop_details.outRaid > tbody.infos > tr > td > div.abort > button
    
    
    # if page.locator("css=#movements > tbody > tr:nth-child(2) > td:nth-child(2) > div.dur_r > span").strip.inner_text()
    #     print("Attack incoming, skipping farm")
    #     return True

    #troops > tbody > tr:nth-child(3) > td.line-last.column-first.large > a

def avoid_attack_loop(page, sleep_minutes, interval_seconds=30): 
    print("starting sleep loop +avoid attack")
    start_time = time.time()
    sleep_seconds = sleep_minutes * 60

    while True:
        avoid_attack(page)
        time.sleep(interval_seconds)

        # Check if total elapsed time exceeds duration
        if time.time() - start_time >= sleep_seconds:
            time_left = time.time() - start_time
            print(time_left)
            print(f"⏱️ Stopped after {sleep_minutes} minutes")
            break