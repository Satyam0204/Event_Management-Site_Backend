# Generated by Django 4.1.5 on 2023-01-06 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("api", "0002_event")]

    operations = [
        migrations.AddField(
            model_name="event",
            name="prizes",
            field=models.CharField(blank=True, max_length=500, null=True),
        )
    ]
