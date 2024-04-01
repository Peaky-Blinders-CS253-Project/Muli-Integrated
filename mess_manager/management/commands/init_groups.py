from django.contrib.auth.models import Group
from students.models import Student
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Initializes groups for students'

    def handle(self, *args, **options):
        put_students_in_group()# Your logic to initialize groups for students goes here
        self.stdout.write(self.style.SUCCESS('Groups initialized successfully'))
def put_students_in_group():
    # Step 1: Retrieve all student objects
    students = Student.objects.all()

    # Step 2: Retrieve or create the group
    group_name = 'Students'
    group, created = Group.objects.get_or_create(name=group_name)

    # Step 3: Add student objects to the group
    for student in students:
        group.student_groups.add(student)  # Use the correct related name

    # Step 4: Save changes
    group.save()