# Generated by Django 3.2.4 on 2021-07-10 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('quiz', '0002_rename_status_submissionstatus'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Response',
            new_name='QuizResponse',
        ),
    ]