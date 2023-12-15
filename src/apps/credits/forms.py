from django import forms


class CreditForm(forms.Form):
    request_amount = forms.IntegerField()

    def clean_request_amount(self) -> int:
        request_amount = self.cleaned_data.get("request_amount")

        if request_amount is not None and request_amount <= 0:
            raise forms.ValidationError(
                "Сумма запроса должна быть положительным числом."
            )

        return request_amount

