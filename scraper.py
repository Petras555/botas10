from genericpath import exists
import os
import django
from playwright.sync_api import sync_playwright

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Import your model after django.setup()
from backoffice.models import Fermos 
# --------------------


def scrape_general(page, url):
            try:
                player_name = page.locator("css=#village_info > tbody > tr:nth-child(3) > td > a").inner_text().strip()
                village_name = page.locator("css=#tileDetails > h1").inner_text().strip().split("\u202d")[0].strip()
                tribe = page.locator("css=#village_info > tbody > tr.first > td").inner_text().strip()
                alliance = page.locator("css=#village_info > tbody > tr:nth-child(2) > td > a").inner_text().strip()
                population = page.locator("css=#village_info > tbody > tr:nth-child(4) > td").inner_text().strip()


                obj, created = Fermos.objects.update_or_create(
                    url=url,
                    defaults={
                        'village_name': village_name,
                        'tribe': tribe,
                        'alliance': alliance,
                        'population': int(population) if population.isdigit() else 0,
                        'url': url
                    }
                )

                exists = Fermos.objects.filter(player_name=player_name).exists()
                exists2 = Fermos.objects.filter(player_name=None).exists()
                if exists:
                    obj, created = Fermos.objects.update_or_create(
                        url=url,
                        defaults={
                            'player_name': player_name
                        }
                    )
                    print("⚠️ Player already exists in DB")

                elif exists2:
                    obj, created = Fermos.objects.create(
                        url=url,
                        player_name=player_name
                    )
                    print("🆕 New player")
                else:
                    obj, created = Fermos.objects.update_or_create(
                    url=url,
                    defaults={
                        'farm_status': False,
                        'farm_status_comment': "Village owner changed"
                    }
                )

                status = "Created" if created else "Updated"
                print(f"✅ {status} record for {player_name}")


            except Exception as e:

                print(f"Failed to scrape {url}: {e}")

def scrape_last_raid(page ,url):
            try:
                page.locator("css=#troop_info > tbody > tr:nth-child(1) > td > a:nth-child(2)").click()
                lumber = page.locator("css=#reportWrapper > div.body > div.role.attacker > table.additionalInformation > tbody > tr > td > div > div.res > div > div:nth-child(1) > span").inner_text().strip()
                clay = page.locator("css=#reportWrapper > div.body > div.role.attacker > table.additionalInformation > tbody > tr > td > div > div.res > div > div:nth-child(2) > span").inner_text().strip()
                iron = page.locator("css=#reportWrapper > div.body > div.role.attacker > table.additionalInformation > tbody > tr > td > div > div.res > div > div:nth-child(3) > span").inner_text().strip()
                crop = page.locator("css=#reportWrapper > div.body > div.role.attacker > table.additionalInformation > tbody > tr > td > div > div.res > div > div:nth-child(4) > span").inner_text().strip()
                resource_cap = page.locator("css=#reportWrapper > div.body > div.role.attacker > table.additionalInformation > tbody > tr > td > div > div.inlineIcon.carry > span").inner_text().strip()

                troop = {}

                for i in range(2, 12):
                    troop[i] = page.locator(f"#reportWrapper > div.body > div.role.attacker > table:nth-child(3) > tbody:nth-child(2) > tr > td:nth-child({i})").inner_text().strip()
                last_troop = page.locator("css=#reportWrapper > div.body > div.role.attacker > table:nth-child(3) > tbody:nth-child(2) > tr > td.unit.last").inner_text().strip()
                
                lost_troop = {}
                for i in range(2, 12):
                    lost_troop[i]= page.locator(f"css=#reportWrapper > div.body > div.role.attacker > table:nth-child(3) > tbody:nth-child(3) > tr > td:nth-child({i})").inner_text().strip()
                
                last_lost_troop = page.locator("css=#reportWrapper > div.body > div.role.attacker > table:nth-child(3) > tbody:nth-child(3) > tr > td.unit.last").inner_text().strip()


                obj, created = Fermos.objects.update_or_create(
                    url=url,
                    defaults={
                        'lumber': lumber,
                        'clay': clay,
                        'iron': iron,
                        'crop': crop,
                        'resource_cap': resource_cap,

                        'legionnaire': troop[2],
                        'praetorian': troop[3],
                        'imperian': troop[4],
                        'equites_legati': troop[5],
                        'equites_imperatoris': troop[6],
                        'equites_caesaris': troop[7],
                        'battering_ram': troop[8],
                        'fire_catapult': troop[9],
                        'senator': troop[10],
                        'settler': troop[11],
                        'hero': last_troop,

                        'lost legionnaire': lost_troop[2],
                        'lost praetorian': lost_troop[3],
                        'lost imperian': lost_troop[4],
                        'lost equites_legati': lost_troop[5],
                        'lost equites_imperatoris': lost_troop[6],
                        'lost equites_caesaris': lost_troop[7],
                        'lost battering_ram': lost_troop[8],
                        'lost fire_catapult': lost_troop[9],
                        'lost senator': lost_troop[10],
                        'lost settler': lost_troop[11],
                        'lost hero': last_lost_troop
                    }
                )
            except Exception as e:
                print(f"Failed to scrape {url}: {e}")

                for i in range(2, 12):
                     if int (troop[i]) > 5:
                        obj, created = Fermos.objects.update_or_create(
                            url=url,
                            defaults={
                                'farm_status': False,
                                'farm_status_comment': f"Too many lost {list(troop.keys())[i-2]} troops"
                            }
                        )
                        return  # Stop processing this farm if any troop count exceeds 5
                
                        # 'legionnaire'
                        # 'praetorian'
                        # 'imperian'
                        # 'equites_legati'
                        # 'equites_imperatoris'
                        # 'equites_caesaris'
                        # 'battering_ram'
                        # 'fire_catapult'
                        # 'senator'
                        # 'settler'
                        # 'hero'