# Generated by Django 4.1.7 on 2023-03-27 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stockCode', models.CharField(max_length=20)),
                ('companyName', models.CharField(max_length=40)),
            ],
        ),
    ]
