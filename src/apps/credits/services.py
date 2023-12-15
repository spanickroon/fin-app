from http import HTTPStatus

from apps.credits.dao import CreditDAO
from apps.credits.forms import CreditForm
from apps.documents.dao import DocumentDAO
from apps.logs.services import logger_service


class CreditService:
    def __init__(self, credit_dao: CreditDAO, document_dao: DocumentDAO):
        self._credit_dao = credit_dao
        self._document_dao = document_dao

    def execute(self, request, credit_form_data: CreditForm) -> HTTPStatus:
        if not credit_form_data.is_valid():
            return HTTPStatus.BAD_REQUEST

        profile = request.user.profile
        documents = self._document_dao.get_userprofile_documents(userprofile=profile)

        if not documents:
            return HTTPStatus.BAD_REQUEST

        request_amount = credit_form_data.cleaned_data["request_amount"]
        self._credit_dao.make_credit(
            userprofile=profile, request_amount=request_amount, document=documents[0]
        )

        logger_service.execute(profile, f"User make a credit with {request_amount}")

        return HTTPStatus.CREATED


credit_service = CreditService(CreditDAO(), DocumentDAO())
