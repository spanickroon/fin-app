from typing import Any

from apps.authentication.models import UserProfile
from apps.documents.dto import DocumentDTO
from apps.documents.models import Document


class DocumentDAO:
    def add_document(
        self, userprofile: UserProfile, document_photo, document: DocumentDTO
    ) -> Any:
        document = Document.objects.create(
            userprofile=userprofile, document_photo=document_photo, **dict(document)
        )
        return document.save()

    def get_userprofile_documents(self, userprofile: UserProfile) -> Any:
        return Document.objects.filter(userprofile=userprofile)
