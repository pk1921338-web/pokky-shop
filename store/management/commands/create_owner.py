from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create Custom Admin for Owner'

    def handle(self, *args, **options):
        # Yahan apni Secret Details dalein
        USERNAME = 'pokky_admin' 
        PASSWORD = 'pokky7788' 
        EMAIL = 'gs7860011@gmail.com'

        if not User.objects.filter(username=USERNAME).exists():
            User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
            print(f"✅ OWNER ACCOUNT CREATED: User={USERNAME}, Pass={PASSWORD}")
        else:
            print("⚠️ Owner account already exists.")