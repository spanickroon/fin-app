from datetime import date

from pydantic import BaseModel


class DocumentDTO(BaseModel):
    birth_date: date
    country: str
    id_number: str
