# Generated by Django 3.2.14 on 2022-07-19 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_note'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ('-updated_on',)},
        ),
    ]