import os 
import django
import re

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from backoffice.models import Fermos


def load_farms(filename="farms.txt"):
    farms = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            farms.append(line)
    return farms

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
    
farm_urls = load_farms("farms.txt")

for url in farm_urls:
    resource_cap = Fermos.objects.filter(url=url).values_list('resource_cap', flat=True).first()
    if resource_cap:
        try:
            percentage = percentage_from_string(resource_cap)
            print(f"URL: {url} - Resource Cap: {resource_cap} - Percentage: {percentage}%")
            print(type(percentage))
        except ValueError as e:
            print(f"Error processing URL {url}: {e}")
    else:
        print(f"URL: {url} - No resource cap found")



