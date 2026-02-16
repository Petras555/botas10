import re
import time, random
import json
import os

from backoffice.models import Fermos 


# Load config once when this module is imported
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

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

def check_warehouse_capacity(page):
    raw_text = page.locator("css=#stockBar > div.warehouse > div > div").inner_text()
    clean_text = re.sub(r'[^\d]', '', raw_text) 
    
    if not clean_text:
        print("Could not find capacity value.")
        return

    capacity_int = int(clean_text)
    print(f"Detected Warehouse capacity: {capacity_int}")

    with open('config.json', 'r') as f:
        config = json.load(f)

    config['WAREHOUSE_CAPACITY'] = capacity_int

    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
        
    print("Successfully updated config.json")


