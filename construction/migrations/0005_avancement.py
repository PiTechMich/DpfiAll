# Generated by Django 5.1.4 on 2025-01-02 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0004_marche'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avancement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etat', models.CharField(choices=[('Achevée', 'Achevée'), ('En arrêt', 'En arrêt'), ('En cours', 'En cours'), ('Non commencée', 'Non commencée')], max_length=25)),
                ('avancement', models.CharField(max_length=100)),
                ('Observation', models.TextField(null=True)),
                ('AnneeAchevement', models.CharField(max_length=10, null=True)),
                ('inaugurable', models.CharField(choices=[('DEJA', 'DEJA'), ('OUI', 'OUI'), ('NON', 'NON')], max_length=10, null=True)),
                ('Niveau', models.TextField(null=True)),
                ('TravauxRestant', models.TextField(null=True)),
                ('create_on', models.DateTimeField(auto_now_add=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='construction.site')),
            ],
        ),
    ]
