from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Set up manager password'

    def add_arguments(self, parser):
        parser.add_argument('password', nargs='?', type=str, help='Manager password')

    def handle(self, *args, **options):
        password = options['password']
        if not password:
            self.stdout.write(self.style.ERROR('Please provide a password for the manager.'))
            return

        manager_exists = User.objects.filter(username='manager').exists()
        if not manager_exists:
            user = User.objects.create_user(username='manager', password=password,rollno=1,is_student=False)
            
            
            self.stdout.write(self.style.SUCCESS(f'Manager password set: {password}'))
            user.save()
        else:
            self.stdout.write(self.style.WARNING('Manager password already set.'))