# Generated by Django 3.2.4 on 2021-06-22 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20210621_0032'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatmessage',
            options={'ordering': ['-created_at']},
        ),
    ]
