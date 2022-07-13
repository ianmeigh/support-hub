# Generated by Django 3.2.14 on 2022-07-13 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_alter_ticket_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('inprogress', 'In Progress'), ('onhold', 'On Hold'), ('closed', 'Closed')], default='open', max_length=10),
        ),
    ]
