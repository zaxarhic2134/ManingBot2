# Generated by Django 3.2.7 on 2021-10-02 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0014_auto_20211002_1152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profilesettings',
            old_name='external_id',
            new_name='external',
        ),
    ]
