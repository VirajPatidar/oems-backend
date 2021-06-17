from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Student, Teacher


@receiver(post_save, sender=User)
def post_save_create_student_or_teacher(sender, instance, created, **kwargs):
    if instance.is_verified:
        if instance.user_type == "student":
            obj, is_created = Student.objects.get_or_create(user=instance)
            if not is_created:
                obj.save()
        else:
            obj, is_created = Teacher.objects.get_or_create(user=instance)
            if not is_created:
                obj.save()