# Generated by Django 5.1.4 on 2025-04-01 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercices', '0008_alter_solution_fichier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='note',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4, null=True),
        ),
    ]
