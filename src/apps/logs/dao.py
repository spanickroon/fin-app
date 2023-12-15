from apps.authentication.models import UserProfile
from apps.logs.models import SystemLog


class LoggerDAO:
    def write_log(self, userprofile: UserProfile, action: str) -> SystemLog:
        return SystemLog.objects.create(userprofile=userprofile, action=action)
