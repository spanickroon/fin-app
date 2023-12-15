from django import forms


class PaymentForm(forms.Form):
    prev_amount = forms.IntegerField(required=False)
    current_amount = forms.IntegerField(required=True)

    def clean_current_amount(self) -> float:
        current_amount = self.cleaned_data.get("current_amount")

        if current_amount is None or current_amount <= 0:
            raise forms.ValidationError(
                "Текущая сумма должна быть предоставлена и быть положительным числом."
            )

        return current_amount
