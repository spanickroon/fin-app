from django.contrib.auth.models import User

from apps.authentication.dto import UserDTO
from apps.authentication.models import UserProfile


class UserDAO:
    def create_user(self, user: UserDTO) -> UserProfile:
        return UserProfile.objects.create(
            user_id=User.objects.create_user(**dict(user)).id
        )


class UserProfileDAO:
    def is_user_exists(self, username: str) -> bool:
        return UserProfile.objects.filter(user__username=username).exists()
