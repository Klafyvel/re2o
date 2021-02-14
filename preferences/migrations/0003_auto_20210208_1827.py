# Generated by Django 2.2.18 on 2021-02-08 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0002_foreign_keys'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assooption',
            options={'verbose_name': 'organisation preferences'},
        ),
        migrations.AlterModelOptions(
            name='generaloption',
            options={'verbose_name': 'general preferences'},
        ),
        migrations.AlterModelOptions(
            name='homeoption',
            options={'verbose_name': 'homepage preferences'},
        ),
        migrations.AlterModelOptions(
            name='mailcontact',
            options={'verbose_name': 'contact email address', 'verbose_name_plural': 'contact email addresses'},
        ),
        migrations.AlterModelOptions(
            name='mailmessageoption',
            options={'verbose_name': 'email message preferences'},
        ),
        migrations.AlterModelOptions(
            name='mandate',
            options={'verbose_name': 'mandate', 'verbose_name_plural': 'mandates'},
        ),
        migrations.AlterModelOptions(
            name='optionalmachine',
            options={'verbose_name': 'machine preferences'},
        ),
        migrations.AlterModelOptions(
            name='optionaltopologie',
            options={'verbose_name': 'topology preferences'},
        ),
        migrations.AlterModelOptions(
            name='optionaluser',
            options={'verbose_name': 'user preferences'},
        ),
        migrations.AlterModelOptions(
            name='radiuskey',
            options={'verbose_name': 'RADIUS key', 'verbose_name_plural': 'RADIUS keys'},
        ),
        migrations.AlterModelOptions(
            name='reminder',
            options={'verbose_name': 'reminder', 'verbose_name_plural': 'reminders'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'service', 'verbose_name_plural': 'services'},
        ),
        migrations.AlterModelOptions(
            name='switchmanagementcred',
            options={'verbose_name': 'switch management credentials'},
        ),
    ]