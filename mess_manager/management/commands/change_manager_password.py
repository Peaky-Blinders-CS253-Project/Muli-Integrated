
# change_manager_password.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Change manager password'

    def handle(self, *args, **options):
        # Fetch the manager user from the database
        manager = User.objects.get(username='manager')

        # Prompt the user to enter the new password
        new_password = input('Enter the new password for the manager: ')

        # Update the manager's password
        manager.is_student = False
        manager.set_password(new_password)
        manager.save()

        self.stdout.write(self.style.SUCCESS('Manager password changed successfully.'))