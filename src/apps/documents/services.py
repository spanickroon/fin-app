from datetime import datetime
from http import HTTPStatus

from django.conf import settings
from django.core.files.base import ContentFile
from django.http.response import HttpResponse
from mindee import PredictResponse, product

from apps.documents.dao import DocumentDAO
from apps.documents.dto import DocumentDTO
from apps.documents.forms import DocumentForm
from apps.logs.services import logger_service


class DocumentService:
    def __init__(self, document_dao: DocumentDAO):
        self._document_dao = document_dao

    def execute(
        self, request: HttpResponse, document_form_data: DocumentForm
    ) -> HTTPStatus:
        if not document_form_data.is_valid():
            return HTTPStatus.BAD_REQUEST

        document_photo = document_form_data.cleaned_data["document_photo"]
        document_photo_copy = ContentFile(
            document_photo.read(), name=document_photo.name
        )
        input_doc = settings.MINDEE_CLIENT.source_from_file(document_photo)

        result: PredictResponse = settings.MINDEE_CLIENT.parse(
            product.PassportV1, input_doc
        )

        logger_service.execute(request.user.profile, result, use_db=False)

        prediction = result.document.inference.prediction
        if not prediction.id_number.value:
            return HTTPStatus.BAD_REQUEST

        document = DocumentDTO(
            birth_date=datetime.strptime(
                prediction.birth_date.value, "%Y-%m-%d"
            ).date(),
            country=prediction.country.value,
            id_number=prediction.id_number.value,
        )

        logger_service.execute(request.user.profile, document)

        self._document_dao.add_document(
            userprofile=request.user.profile,
            document_photo=document_photo_copy,
            document=document,
        )

        return HTTPStatus.CREATED


document_service = DocumentService(DocumentDAO())
