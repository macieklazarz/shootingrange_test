# Generated by Django 3.2.9 on 2022-01-06 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wyniki', '0010_wyniki_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wyniki',
            name='result',
            field=models.TextField(default='0', max_length=60, null=True),
        ),
    ]