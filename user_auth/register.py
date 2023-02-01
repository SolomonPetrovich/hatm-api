from django.contrib.auth import authenticate
from .models import CustomUser as User
from rest_framework.exceptions import AuthenticationFailed
from .backends import PasswordlessAuthBackend


def register_social_user(provider, email):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:
            return filtered_user_by_email[0].tokens()

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'email': email,
        }
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        
        new_user = User.objects.get(email=email)
        return new_user.tokens()        