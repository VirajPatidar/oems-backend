# Generated by Django 3.2.4 on 2021-07-25 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0003_grade_assignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment_response',
            name='idGraded',
            field=models.BooleanField(default=False),
        ),
    ]
