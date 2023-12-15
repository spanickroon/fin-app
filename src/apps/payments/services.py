import base64
import json
from io import BytesIO
from typing import Any, Optional

import qrcode
import requests
from django.conf import settings
from django.http import HttpResponse

from apps.logs.services import logger_service
from apps.payments.dao import PaymentDAO
from apps.payments.forms import PaymentForm


class PaymentService:
    get_all_payments_action = "get_all_payments"
    get_payment_action = "get_payment"
    make_payment_action = "make_payment"
    get_history = "get_history"

    def __init__(self, payment_dao: PaymentDAO):
        self._payment_dao = payment_dao

    def execute(
        self,
        request,
        action: str,
        payment_data: Optional[PaymentForm] = None,
        category_id: Optional[int] = None,
        payment_id: Optional[int] = None,
    ) -> str | None:
        if action == self.get_all_payments_action:
            return self._get_all_payments()
        if action == self.get_payment_action:
            return self._get_payment(category_id, payment_id)
        if action == self.make_payment_action:
            return self._make_payment(request, payment_data, payment_id)
        if action == self.get_history:
            return self._get_history(request)

    def _get_all_payments(self) -> Any:
        return self._payment_dao.get_all_payments()

    def _get_payment(self, category_id: int, payment_id: Optional[int] = None) -> Any:
        if category_id and not payment_id:
            return self._payment_dao.get_payments_by_category(category_id)

        return self._payment_dao.get_payment_by_id(payment_id)

    def _make_payment(
        self, request: HttpResponse, payment_data, payment_id: int
    ) -> str | None:
        payment = self._payment_dao.get_payment_by_id(payment_id)
        profile = request.user.profile

        if not payment_data.is_valid():
            logger_service.execute(
                profile, action="payment_data is not valid", use_db=False
            )
            return None

        prev_amount = payment_data.cleaned_data["prev_amount"]
        current_amount = payment_data.cleaned_data["current_amount"]
        rate = payment.rate
        price_amount = (current_amount - (prev_amount if prev_amount else 0)) * rate

        history = self._payment_dao.add_payment_to_history(
            profile=profile,
            payment=payment,
            prev_amount=0 if prev_amount is None else prev_amount,
            current_amount=current_amount,
            price_amount=price_amount,
        )
        result_paypal = self._paypal_payment(price_amount, payment.name)
        result_paypal_url = (
            result_paypal[2]
            if result_paypal[0]
            else "https://www.paypal.com/by/webapps/mpp/home"
        )

        logger_service.execute(
            profile,
            action=f"User make a payment {payment.name} - {payment.code}, history id: {history.id}",
        )
        logger_service.execute(None, result_paypal, use_db=False)

        stream = BytesIO()
        qrcode.make(result_paypal_url).save(stream)
        stream.seek(0)
        qr_code = base64.b64encode(stream.getvalue()).decode()

        return qr_code

    def _get_history(self, request: HttpResponse) -> Any:
        return self._payment_dao.get_payments_history_by_userprofile(
            request.user.profile
        )

    def _paypal_payment(self, amount: int, payment_name: str) -> Any:
        client_id = settings.PAYPAL_CLIENT_ID
        secret = settings.PAYPAL_SECRET_KEY
        url = settings.PAYPAL_DEFAULT_URL

        base_url = url
        token_url = base_url + "/v1/oauth2/token"
        payment_url = base_url + "/v1/payments/payment"

        token_payload = {"grant_type": "client_credentials"}
        token_headers = {"Accept": "application/json", "Accept-Language": "en_US"}
        token_response = requests.post(
            token_url,
            auth=(client_id, secret),
            data=token_payload,
            headers=token_headers,
        )

        if token_response.status_code != 200:
            return False, "Failed to authenticate with PayPal API", None

        access_token = token_response.json()["access_token"]

        payment_payload = {
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [
                {
                    "amount": {"total": str(amount), "currency": "RUB"},
                    "description": f"TOFI FIN APP PAYMENT {payment_name}",
                }
            ],
            "redirect_urls": {
                "return_url": "https://www.paypal.com/by/webapps/mpp/home",
                "cancel_url": "https://www.paypal.com/by/webapps/mpp/home",
            },
        }

        payment_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        payment_response = requests.post(
            payment_url, data=json.dumps(payment_payload), headers=payment_headers
        )

        logger_service.execute(None, payment_response.text, use_db=False)

        if payment_response.status_code != 201:
            return False, "Failed to create PayPal payment.", None

        payment_id = payment_response.json()["id"]
        approval_url = next(
            link["href"]
            for link in payment_response.json()["links"]
            if link["rel"] == "approval_url"
        )

        return True, payment_id, approval_url


payment_service = PaymentService(PaymentDAO())
