# Generated by Django 4.1.7 on 2023-03-09 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('short_name', models.CharField(max_length=1024)),
                ('description', models.CharField(max_length=1024)),
            ],
        ),
    ]
