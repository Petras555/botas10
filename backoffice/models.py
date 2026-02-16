from django.db import models

class BotLog(models.Model):
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bot Log"          # This is the tab name
        verbose_name_plural = "Bot Logs"   # This is the plural tab name



class Fermos(models.Model):

    farm_status = models.BooleanField(default=True)  # Example field to track if the farm is active or not
    farm_status_comment = models.CharField(max_length=255, blank=True)  # Optional comment about the farm status

    village_name = models.CharField(max_length=255, blank=True)
    player_name = models.CharField(max_length=255, blank=True)
    tribe = models.CharField(max_length=30, blank=True)
    
    # Profile Data (Add your other 27 columns here)
    alliance = models.CharField(max_length=255, blank=True)
    population = models.CharField(max_length=20, blank=True)
    url = models.CharField(max_length=255, blank=True)

    lumber = models.IntegerField(default=0, blank=True)
    clay = models.IntegerField(default=0, blank=True)
    iron = models.IntegerField(default=0, blank=True)
    crop = models.IntegerField(default=0, blank=True)
    resource_cap = models.CharField(max_length=255, blank=True)

    legionnaire = models.IntegerField(default=0, blank=True)
    praetorian = models.IntegerField(default=0, blank=True)
    imperian = models.IntegerField(default=0, blank=True)
    equites_legati = models.IntegerField(default=0, blank=True)
    equites_imperatoris = models.IntegerField(default=0, blank=True)
    equites_caesaris = models.IntegerField(default=0, blank=True)
    battering_ram = models.IntegerField(default=0, blank=True)
    fire_catapult = models.IntegerField(default=0, blank=True)
    senator = models.IntegerField(default=0, blank=True)
    settler = models.IntegerField(default=0, blank=True)
    hero = models.IntegerField(default=0, blank=True)

    lost_legionnaire = models.IntegerField(default=0, blank=True)
    lost_praetorian = models.IntegerField(default=0, blank=True)
    lost_imperian = models.IntegerField(default=0, blank=True)
    lost_equites_legati = models.IntegerField(default=0, blank=True)
    lost_equites_imperatoris = models.IntegerField(default=0, blank=True)
    lost_equites_caesaris = models.IntegerField(default=0, blank=True)
    lost_battering_ram = models.IntegerField(default=0, blank=True)
    lost_fire_catapult = models.IntegerField(default=0, blank=True)
    lost_senator = models.IntegerField(default=0, blank=True)
    lost_settler = models.IntegerField(default=0, blank=True)
    lost_hero = models.IntegerField(default=0, blank=True)



    def __str__(self):
        return self.village_name
    

    
    # python manage.py makemigrations
    # python manage.py migrate