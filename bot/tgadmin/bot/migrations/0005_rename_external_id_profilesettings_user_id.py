# Generated by Django 3.2.7 on 2021-10-02 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_alter_profilesettings_external_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profilesettings',
            old_name='external_id',
            new_name='user_id',
        ),
    ]
