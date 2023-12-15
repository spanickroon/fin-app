from typing import Any

from django import forms


class DocumentForm(forms.Form):
    document_photo = forms.ImageField()

    def clean_document_photo(self) -> Any:
        document_photo = self.cleaned_data.get("document_photo")

        if not document_photo:
            raise forms.ValidationError("Необходимо загрузить документ.")

        return document_photo
