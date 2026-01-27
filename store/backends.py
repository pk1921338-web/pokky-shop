from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q

class EmailPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Ye check karega: Username OR Email OR Phone Number
            user = User.objects.get(
                Q(username=username) | 
                Q(email=username) | 
                Q(profile__phone_number=username)
            )
        except User.DoesNotExist:
            return None

        # Agar user mil gaya, to password check karo
        if user.check_password(password):
            return user
        return None