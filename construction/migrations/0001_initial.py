# Generated by Django 5.1.4 on 2025-01-02 07:55

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('create_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('create_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construction.province')),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('create_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construction.region')),
            ],
        ),
    ]
