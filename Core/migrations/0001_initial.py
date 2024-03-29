# Generated by Django 4.1.7 on 2023-03-27 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exploit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('os', models.CharField(max_length=200)),
                ('module', models.CharField(max_length=200)),
                ('payload', models.CharField(max_length=200)),
                ('uri', models.CharField(default=None, max_length=200)),
                ('rhost', models.CharField(max_length=200)),
                ('rport', models.IntegerField()),
                ('lhost', models.CharField(default=None, max_length=200)),
                ('lport', models.IntegerField(default=None)),
            ],
        ),
    ]
