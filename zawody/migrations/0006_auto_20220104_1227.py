# Generated by Django 3.2.9 on 2022-01-04 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zawody', '0005_auto_20211121_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turniej',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='zawody',
            name='turniej',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='zawody.turniej'),
        ),
    ]