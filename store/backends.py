from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q

class EmailPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to fetch user by Username or Email first
            user = User.objects.filter(
                Q(username=username) | Q(email=username)
            ).first()

            # If not found, try searching by Phone (only if Profile exists)
            if not user:
                # We do this check to avoid the "Cannot resolve keyword profile" crash
                if hasattr(User, 'profile'): 
                    user = User.objects.filter(profile__phone_number=username).first()

        except Exception:
            # If anything goes wrong, just return None (don't crash)
            return None

        if user and user.check_password(password):
            return user
        return None