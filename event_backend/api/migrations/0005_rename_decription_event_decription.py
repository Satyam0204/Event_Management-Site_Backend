# Generated by Django 4.1.5 on 2023-01-06 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("api", "0004_alter_event_decription")]

    operations = [
        migrations.RenameField(
            model_name="event", old_name="Decription", new_name="decription"
        )
    ]
