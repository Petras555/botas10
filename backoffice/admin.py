from django.contrib import admin
from .models import BotLog, Fermos # Import your new model



@admin.register(BotLog)
class BotLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'status', 'timestamp')
    search_fields = ('action',)


@admin.register(Fermos)
class FermosAdmin(admin.ModelAdmin):
    # This organizes the layout
    fieldsets = (
        ('Farm Status', {
            'fields': ('farm_status', 'farm_status_comment')
        }),
        ('General Info', {
            'fields': ('village_name', 'player_name', 'tribe','alliance', 'population', 'url')
        }),
        ('Last Attack Raided Resources', {
            # Putting these in a single inner tuple forces them onto one line
            'fields': (('lumber', 'clay', 'iron', 'crop'), 'resource_cap'),
        }),
        ('Last Attack – Troops Overview', {
        'fields': (
            ('legionnaire', 'lost_legionnaire'),
            ('praetorian', 'lost_praetorian'),
            ('imperian', 'lost_imperian'),
            ('equites_legati', 'lost_equites_legati'),
            ('equites_imperatoris', 'lost_equites_imperatoris'),
            ('equites_caesaris', 'lost_equites_caesaris'),
            ('battering_ram', 'lost_battering_ram'),
            ('fire_catapult', 'lost_fire_catapult'),
            ('senator', 'lost_senator'),
            ('settler', 'lost_settler'),
            ('hero', 'lost_hero'),
        )
}),
    )