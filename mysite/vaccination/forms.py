from django.forms import ModelForm
from vaccination.models import Vaccination_Campaign, Slot, Vaccination


class CampaignCreateForm(ModelForm):
    class Meta:
        model = Vaccination_Campaign
        fields = "__all__"


class CampaignUpdateForm(ModelForm):
    class Meta:
        model = Vaccination_Campaign
        fields = "__all__"


class SlotCreateForm(ModelForm):
    class Meta:
        model = Slot
        fields = "__all__"


class SlotUpdateForm(ModelForm):
    class Meta:
        model = Slot
        fields = "__all__"

class VaccinationForm(ModelForm):
    class Meta:
        model = Vaccination
        fields = ["patient", "campaign", "slot"]