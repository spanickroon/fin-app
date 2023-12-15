from typing import Any

from apps.authentication.models import UserProfile
from apps.payments.models import Payment, PaymentHistory, PaymentTemplate


class PaymentDAO:
    def get_all_payments(self) -> Any:
        return Payment.objects.all()

    def get_payments_by_category(self, category_id: int) -> Any:
        return Payment.objects.filter(category_id=category_id)

    def get_payment_by_id(self, payment_id: int) -> Any:
        try:
            return Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return None

    def add_payment_to_history(
        self,
        profile: UserProfile,
        payment: Payment,
        prev_amount: int,
        current_amount: float,
        price_amount: float,
    ) -> Any:
        return PaymentHistory.objects.create(
            userprofile=profile,
            payment=payment,
            category=payment.category,
            prev_amount=prev_amount,
            current_amount=current_amount,
            price_amount=price_amount,
        )

    def get_payments_history_by_userprofile(self, profile: UserProfile) -> Any:
        return PaymentHistory.objects.filter(userprofile=profile)

    def get_payment_template_by_userprofile(self, profile: UserProfile) -> Any:
        return PaymentHistory.objects.filter(userprofile=profile)

    def add_payment_from_history_to_template(
        self, payment: Payment, template: PaymentTemplate
    ) -> Any:
        payment = PaymentHistory.objects.get(paymenthistory_id=payment)
        payment.payment_template = template
        payment.save()
