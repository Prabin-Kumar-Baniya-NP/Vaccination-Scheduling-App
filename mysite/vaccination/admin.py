from django.contrib import admin
from vaccination.models import Slot, Campaign, Vaccination


class SlotInline(admin.TabularInline):
    model = Slot
    exclude = ["reserved"]


class CustomCampaignAdmin(admin.ModelAdmin):
    list_display = ["vaccine", "center", "start_date", "end_date"]
    ordering = ["start_date"]
    search_fields = ["vaccine", "center", "start_date", "end_date"]
    inlines = [SlotInline]


class CustomVaccinationAdmin(admin.ModelAdmin):
    list_display = ["patient", "campaign", "slot", "is_vaccinated"]
    search_fields = ["patient", "campaign", "slot"]
    list_filter = ["is_vaccinated"]


admin.site.register(Campaign, CustomCampaignAdmin)
admin.site.register(Vaccination, CustomVaccinationAdmin)
