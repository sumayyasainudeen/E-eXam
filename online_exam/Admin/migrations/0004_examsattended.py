# Generated by Django 5.0.3 on 2024-04-01 03:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0003_alter_exams_duration'),
        ('register_login', '0002_studentdetails_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamsAttended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=255, null=True)),
                ('answer_status', models.CharField(blank=True, max_length=100, null=True)),
                ('exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Admin.exams')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Admin.questions')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='register_login.studentdetails')),
            ],
        ),
    ]
