from django.contrib import admin
from .models import Person, BotLog, Nustatymai, Grupes, Fermos # Import your new model

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # This shows columns in the list view
    list_display = ('full_name', 'email', 'company', 'is_active')
    
    # THIS IS YOUR SEARCH BUTTON LOGIC
    # It will search through these specific fields
    search_fields = ('full_name', 'email', 'company')
    
    # This adds a filter sidebar on the right
    list_filter = ('is_active', 'date_joined')



@admin.register(BotLog)
class BotLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'status', 'timestamp')
    search_fields = ('action',)


@admin.register(Nustatymai)
class NustatymaiAdmin(admin.ModelAdmin):
    list_display = ('action', 'status', 'timestamp')
    list_filter = ('status',)
    search_fields = ('action',)

@admin.register(Grupes)
class GrupesAdmin(admin.ModelAdmin):
    list_display = ('action', 'status', 'timestamp')
    list_filter = ('status',)
    search_fields = ('action',)

@admin.register(Fermos)
class FermosAdmin(admin.ModelAdmin):
    list_display = ('village_name', 'player_name', 'tribe', 'alliance', 'population')
    list_filter = ('tribe', 'alliance')
    search_fields = ('village_name', 'player_name')