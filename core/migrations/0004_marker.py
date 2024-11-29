# Generated by Django 4.2 on 2024-11-29 07:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_alter_membership_group"),
    ]

    operations = [
        migrations.CreateModel(
            name="Marker",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("event_id", models.CharField(max_length=50)),
                ("member_id", models.CharField(max_length=50)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("place_name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
