# Generated by Django 5.1.4 on 2025-03-29 20:23

import storages.backends.s3
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercices', '0007_alter_exercice_fichier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='fichier',
            field=models.FileField(storage=storages.backends.s3.S3Storage(), upload_to='solutions/', verbose_name='Fichier S3'),
        ),
    ]
