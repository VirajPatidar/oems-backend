# Generated by Django 3.2.4 on 2021-07-24 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0002_assignment_response_submissionstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade_Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks_scored', models.IntegerField()),
                ('remark', models.TextField(blank=True)),
                ('response_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_assignment_response_id', to='assignment.assignment_response')),
            ],
        ),
    ]
