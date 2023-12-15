from unittest.mock import patch

from django.test import TestCase
from apps.authentication.models import User, UserProfile

from apps.payments.services import payment_service
from apps.payments.models import Category, Payment, PaymentHistory
from apps.logs.models import SystemLog

from parameterized import parameterized, param

from django.test.client import RequestFactory


class PaymentServiceTestCase(TestCase):

    def setUp(self):
        self._user = User.objects.create_user(username='test_user')
        self._test_user = UserProfile.objects.create(
            user=self._user,
        )
        self._payment_service = payment_service
        self._request = RequestFactory()
        self._request.user = self._user
        self._category = Category.objects.create(name='test_category')

    def test_execute_get_all_payment(self):
        codes = [Payment.objects.create(name=f"name_{i}", category=self._category).code for i in range(5)]
        result = self._payment_service.execute(self._request, self._payment_service.get_all_payments_action)

        self.assertListEqual(codes, [payment.code for payment in result])

    def test_execute_get_payment_by_category(self):
        new_category = Category.objects.create(name='test_category_1')
        codes = [Payment.objects.create(name=f"name_{i}", category=new_category).code for i in range(3)]
        result = self._payment_service.execute(self._request, self._payment_service.get_payment_action, None, new_category.id)

        self.assertEqual(len(result), 3)
        self.assertListEqual(codes, [payment.code for payment in result])

    def test_execute_get_payment_by_id(self):
        new_category = Category.objects.create(name='test_category_2')
        ids = [Payment.objects.create(name=f"name_{i}", category=new_category).id for i in range(3)]
        result = self._payment_service.execute(
            self._request, self._payment_service.get_payment_action, None, new_category.id, ids[1]
        )

        self.assertEqual(ids[1], result.id)

    def test_execute_get_history(self):
        payment = Payment.objects.create(
            category=self._category,
            name='test_payment',
        )
        payment_history = PaymentHistory.objects.create(
            userprofile=self._test_user,
            payment=payment,
            category=self._category,
            current_amount=100,
            prev_amount=100,
        )

        result = self._payment_service.execute(
            self._request, self._payment_service.get_history
        )

        self.assertEqual(payment_history, result[0])

    @parameterized.expand(
        [
            param(False, {}, None),
            param(True, {'prev_amount': 100, 'current_amount': 600}, 'test_code'),
        ]
    )
    @patch('apps.payments.services.PaymentForm')
    def test_execute_make_payment(self, is_valid, form_data, expected_result, mock_form):
        payment = Payment.objects.create(
            category=self._category,
            name='test_payment',
        )

        mock_form.is_valid.return_value = is_valid
        mock_form.cleaned_data = form_data

        result = self._payment_service.execute(
            self._request, self._payment_service.make_payment_action, mock_form, None, payment.id,
        )

        if not expected_result:
            self.assertIsNone(result)
        else:
            logs = SystemLog.objects.filter(userprofile=self._test_user)

            self.assertTrue(PaymentHistory.objects.filter(userprofile=self._test_user, payment=payment).exists())
            self.assertTrue('User make a payment test_payment' in logs[0].action)
