from django.http import HttpResponse

from apps.authentication.models import UserProfile
from apps.credits.models import CreditRequest


class CreditDAO:
    def make_credit(
        self, userprofile: UserProfile, request_amount: float, document
    ) -> HttpResponse:
        return CreditRequest.objects.create(
            userprofile=userprofile,
            request_amount=request_amount,
            document=document,
        )
