from django.db import models

class Person(models.Model):
    # Basic Info
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Profile Data (Add your other 27 columns here)
    job_title = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name
    
class BotLog(models.Model):
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bot Log"          # This is the tab name
        verbose_name_plural = "Bot Logs"   # This is the plural tab name


            
class Nustatymai(models.Model):
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Nustatymai"          # This is the tab name
        verbose_name_plural = "Nustatymai"   # This is the plural tab name


class Grupes(models.Model):
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Grupes"          # This is the tab name
        verbose_name_plural = "Grupes"   # This is the plural tab name

class Fermos(models.Model):
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


    def __str__(self):
        return self.village_name
    
    # python manage.py makemigrations
    # python manage.py migrate