import logging
from typing import Optional

from apps.authentication.models import UserProfile
from apps.logs.dao import LoggerDAO


class LoggerService:
    def __init__(self, logger_dao: LoggerDAO):
        self._logger_dao = logger_dao

    def execute(
        self,
        userprofile: Optional[UserProfile] = None,
        action: str = "",
        use_db: bool = True,
    ) -> None:
        if userprofile and use_db:
            self._logger_dao.write_log(userprofile, action)

        logging.info(action)


logger_service = LoggerService(logger_dao=LoggerDAO())
