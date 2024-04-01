# signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Group
from students.models import Student

@receiver(post_save, sender=Student)
def add_student_to_group(sender, instance, created, **kwargs):
    if created:
        student_group = Group.objects.get(name='Students')
        instance.groups.add(student_group)

@receiver(post_delete, sender=Student)
def remove_student_from_group(sender, instance, **kwargs):
    student_group = Group.objects.get(name='Students')
    instance.groups.remove(student_group)
