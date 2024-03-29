from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import Permission
from user.tests.factory import UserFactory
from vaccination.tests.factory import VaccinationFactory


class TestPermissionsOnVaccinationView(TestCase):
    def setUp(self):
        self.c = Client()
        self.vaccination = VaccinationFactory()
        self.user = UserFactory()
        self.c.login(email=self.user.email, password="abcde@12345")
        return super().setUp()

    def test_unauthorized_access_on_registration_list_view(self):
        response = self.c.get(
            reverse(
                "vaccination:registration-list",
                kwargs={"campaign_id": self.vaccination.campaign.id},
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_registration_list_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="view_vaccination")
        )
        response = self.c.get(
            reverse(
                "vaccination:registration-list",
                kwargs={"campaign_id": self.vaccination.campaign.id},
            )
        )
        self.assertEqual(response.status_code, 200)
