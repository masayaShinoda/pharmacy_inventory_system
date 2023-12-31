# Generated by Django 4.2.4 on 2023-10-02 08:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("demo", "0009_userpreference_manager_alter_pharmacy_manager"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="manager",
            name="id",
        ),
        migrations.AlterField(
            model_name="manager",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                serialize=False,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="manager",
            name="user_preference",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="demo.userpreference",
            ),
        ),
    ]
