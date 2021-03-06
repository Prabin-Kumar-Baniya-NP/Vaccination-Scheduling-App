import datetime
import io
from user.models import User
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from vaccination.models import Slot, Vaccination, Campaign
from django.urls import reverse_lazy, reverse
from vaccination.forms import CampaignCreateForm, CampaignUpdateForm, SlotCreateForm, SlotUpdateForm, VaccinationForm
from vaccine.models import Vaccine
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.http import FileResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.utils.decorators import method_decorator
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle


class CampaignCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Creates a new vaccination campaign
    """
    model = Campaign
    form_class = CampaignCreateForm
    permission_required = ("vaccination.add_campaign",)
    template_name = "vaccination/campaign/campaign-create.html"
    success_url = reverse_lazy("vaccination:campaign-list")
    success_message = "Campaign Created Successfully"


class CampaignUpdateForm(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Updates the vaccination campaign
    """
    model = Campaign
    form_class = CampaignUpdateForm
    permission_required = ("vaccination.change_campaign",)
    template_name = "vaccination/campaign/campaign-update.html"
    success_url = reverse_lazy("vaccination:campaign-list")
    success_message = "Campaign Updated Successfully"


@method_decorator(cache_page(60*15), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class CampaignListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Lists all the vaccination campaign
    """
    model = Campaign
    template_name = "vaccination/campaign/campaign-list.html"
    paginate_by = 10
    ordering = ["-id"]
    permission_required = ("vaccination.view_campaign",)


@method_decorator(cache_page(60*15), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class CampaignDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Returns the details of vaccination campaign
    """
    model = Campaign
    template_name = "vaccination/campaign/campaign-detail.html"
    permission_required = ("vaccination.view_campaign", )

    def get_queryset(self):
        return super().get_queryset().select_related("center", "vaccine")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["registration"] = Vaccination.objects.filter(
            campaign=self.kwargs["pk"]).count()
        return context


class CampaignDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Deletes the vaccination campaign
    """
    model = Campaign
    template_name = "vaccination/campaign/campaign-delete.html"
    permission_required = ("vaccination.delete_campaign", )
    success_url = reverse_lazy("vaccination:campaign-list")
    success_message = "Campaign Deleted Successfully"


class SlotCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Creates a new slot for given vaccination campaign
    """
    model = Slot
    form_class = SlotCreateForm
    template_name = "vaccination/slot/slot-create.html"
    permission_required = ("vaccination.add_slot", )
    success_url = reverse_lazy("vaccination:slot-list")
    success_message = "Slot Created Successfully"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["campaign_id"] = self.kwargs["campaign_id"]
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial["campaign"] = Campaign.objects.get(
            id=self.kwargs["campaign_id"])
        return initial

    def get_success_url(self) -> str:
        return reverse_lazy("vaccination:slot-list", kwargs={"campaign_id": self.kwargs["campaign_id"]})


class SlotUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Updates the slot
    """
    model = Slot
    form_class = SlotUpdateForm
    permission_required = ("vaccination.change_slot", )
    template_name = "vaccination/slot/slot-update.html"
    success_message = "Slot Updated Successfully"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["campaign_id"] = self.kwargs["campaign_id"]
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial["campaign"] = Campaign.objects.get(
            id=self.kwargs["campaign_id"])
        return initial

    def get_success_url(self):
        return reverse_lazy("vaccination:slot-list", kwargs={"campaign_id": self.kwargs["campaign_id"]})


@method_decorator(cache_page(60*15), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class SlotListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Lists all the slot for given vaccination campaign
    """
    model = Slot
    template_name = "vaccination/slot/slot-list.html"
    paginate_by = 10
    permission_required = ("vaccination.view_slot", )

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Slot.objects.filter(
            campaign=self.kwargs["campaign_id"]).order_by("id")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["campaign_id"] = self.kwargs["campaign_id"]
        return context


@method_decorator(cache_page(60*15), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class SlotDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Returns the details of given slot
    """
    model = Slot
    template_name = "vaccination/slot/slot-detail.html"
    permission_required = ("vaccination.view_slot", )

    def get_queryset(self):
        return super().get_queryset().select_related("campaign")


class SlotDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Deletes the slot 
    """
    model = Slot
    template_name = "vaccination/slot/slot-delete.html"
    permission_required = ("vaccination.delete_slot", )
    success_message = "Slot Deleted Successfully"

    def get_success_url(self) -> str:
        return reverse_lazy("vaccination:slot-list", kwargs={"campaign_id": self.get_object().campaign.id})


@method_decorator(cache_page(60*15), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class VaccinationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Lists all the vaccination registration for given vaccination campaign
    """
    model = Vaccination
    template_name = "vaccination/vaccination-list.html"
    paginate_by = 10
    permission_required = ("vaccination.view_campaign", )

    def get_queryset(self):
        return Vaccination.objects.filter(campaign=self.kwargs["campaign_id"]).order_by("-id")


@method_decorator(cache_page(60), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class VaccinationListViewForPatient(LoginRequiredMixin, ListView):
    """
    Lists all the vaccination registration done by the user
    """
    model = Vaccination
    template_name = "vaccination/vaccination-list-patient.html"
    paginate_by = 10

    def get_queryset(self):
        return Vaccination.objects.filter(patient=User.objects.get(id=self.request.user.id)).order_by("-id")


@method_decorator(cache_page(60*15), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class VaccinationDetailView(LoginRequiredMixin, DetailView):
    """
    Returns the details of vaccination registration
    """
    model = Vaccination
    template_name = "vaccination/vaccination-detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related("patient", "campaign", "slot")


@cache_page(60*15)
@login_required
def choose_vaccine(request):
    """
    Handles the vaccine choose part of vaccination registration
    """
    context = {
        "vaccine_list": Vaccine.objects.all().only("name", "number_of_doses", "interval"),
    }
    return render(request, "vaccination/choose-vaccine.html", context)


@login_required
def check_dose(request, vaccine_id):
    """
    View to check dose of vaccine for given patient
    """
    patient = User.objects.get(id=request.user.id)
    vaccine = Vaccine.objects.get(id=vaccine_id)
    dose_taken = Vaccination.get_dose_number(patient, vaccine)
    if dose_taken < vaccine.number_of_doses:
        return HttpResponseRedirect(reverse("vaccination:choose-campaign", kwargs={"vaccine_id": vaccine_id}))
    else:
        return render(request, "vaccination/dose-information.html", {"dose_taken": dose_taken, "dose_required": vaccine.number_of_doses})


@cache_page(60*15)
@login_required
def choose_campaign(request, vaccine_id):
    """
    Handles the choose vaccination campaign part of vaccination registration
    """
    context = {
        "campaign_list": Campaign.objects.filter(vaccine=vaccine_id).only("center", "start_date", "end_date").select_related("center")
    }
    return render(request, "vaccination/choose-campaign.html", context)


@cache_page(60*15)
@login_required
def choose_slot(request, campaign_id):
    """
    Lists all the slot for given vaccination campaign to choose for vaccination registration
    """
    context = {
        "slot_list": Slot.objects.filter(campaign=campaign_id, date__gte=datetime.date.today()).select_related("campaign")
    }
    return render(request, "vaccination/choose-slot.html", context)


@login_required
@transaction.atomic
def confirm_vaccination(request, campaign_id, slot_id):
    """
    Handles the final vaccination registration request
    """
    if request.method == "POST":
        form = VaccinationForm(request.POST)
        if form.is_valid():
            if Slot.reserve_vaccine(slot_id):
                form.save()
                messages.success(request, "Vaccination Scheduled Successfully")
                return render(request, "vaccination/schedule-success.html", {})
            else:
                messages.error(
                    request, "Unable to schedule your vaccination. Please try again.")
                return HttpResponse("Sorry! We are unable to reserve vaccine for you. Please Try Scheduling the vaccination again")
        else:
            return HttpResponse("Unable to process your request! Please enter correct data")
    else:
        campaign = Campaign.objects.select_related(
            "center", "vaccine").get(id=campaign_id)
        slot = Slot.objects.only("date", "start_time",
                                 "end_time").get(id=slot_id)
        form = VaccinationForm(
            initial={"patient": request.user, "campaign": campaign, "slot": slot})
        context = {
            "patient": request.user,
            "campaign": campaign,
            "slot": slot,
            "form": form
        }
        return render(request, "vaccination/confirm-vaccination.html", context)


@login_required
@transaction.atomic
def approve_vaccination(request, vaccination_id):
    """
    Approves the vaccination of patient
    """
    if request.user.has_perm("vaccination.change_vaccination"):
        vaccination = Vaccination.objects.only(
            "is_vaccinated", "updated_by").get(id=vaccination_id)
        vaccination.is_vaccinated = True
        vaccination.updated_by = User.objects.get(id=request.user.id)
        vaccination.save()
        messages.success(request, "Vaccination approved successfully")
        return HttpResponseRedirect(reverse("vaccination:vaccination-detail", kwargs={"pk": vaccination_id}))
    else:
        messages.error(
            request, "You don't have permission to approve vaccination")
        raise PermissionDenied()


@login_required
def vaccine_certificate(request, vaccination_id):
    vaccination = Vaccination.objects.select_related(
        "patient", "campaign", "slot").get(id=vaccination_id)
    dose_number = Vaccination.get_dose_number(
        request.user, vaccination.campaign.vaccine)
    context = {
        "pdf_title": f"{vaccination.patient.get_full_name() } | Vaccine Certificate",
        "date": str(datetime.datetime.now()),
        "title": "Vaccine Certificate",
        "subtitle": "To Whom It May Concern",
        "content": f"This is to certify that Mr/Ms/Mrs {vaccination.patient.get_full_name() } has successfuly completed dose {dose_number} of {vaccination.campaign.vaccine.name }. The vaccination was scheduled on { vaccination.slot.date }, { vaccination.slot.start_time } at { vaccination.campaign.center.name } and it was approved by { vaccination.updated_by.get_full_name() }.",
    }
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setTitle(context["pdf_title"])
    # Write the date
    p.drawString(40, 800, context["date"])
    # Draw a line
    p.line(20, 795, 570, 795)
    # Write the title
    p.setFont('Helvetica-Bold', 14)
    p.drawCentredString(300, 750, context["title"])
    # Write the subtitle
    p.setFont('Helvetica', 12)
    p.drawCentredString(300, 700, context["subtitle"])
    # Write the paragraph style
    para_style = ParagraphStyle(
        "paraStyle", fontSize=14, leading=20, firstLineIndent=25)
    # Write the paragraph
    para = Paragraph(context["content"], para_style)
    para.wrapOn(p, 500, 200)  # dimension of paragraph (width, height)
    para.drawOn(p, 40, 600)  # location of paragraph (x, y)
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=context["pdf_title"])
