# Generated by Django 5.1.4 on 2025-03-30 02:37

import corrections.models
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corrections', '0001_initial'),
        ('exercices', '0008_alter_solution_fichier'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='correction',
            options={'ordering': ['-created_at'], 'verbose_name': 'Correction', 'verbose_name_plural': 'Corrections'},
        ),
        migrations.RemoveField(
            model_name='correction',
            name='feedback',
        ),
        migrations.AddField(
            model_name='correction',
            name='annotated_document',
            field=models.FileField(blank=True, null=True, storage=corrections.models.CorrectionFileStorage(), upload_to='annotated/%Y/%m/%d', verbose_name='Document annoté'),
        ),
        migrations.AddField(
            model_name='correction',
            name='corrected_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='corrections_realisees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='correction',
            name='exercice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='corrections', to='exercices.exercice', verbose_name='Exercice source'),
        ),
        migrations.AddField(
            model_name='correction',
            name='is_validated',
            field=models.BooleanField(default=False, verbose_name='Validée par un enseignant'),
        ),
        migrations.AddField(
            model_name='correction',
            name='structured_feedback',
            field=models.JSONField(default=dict, help_text="{'points_forts': [str], 'points_faibles': [str], 'corrections': [str],'references': [str]}", verbose_name='Feedback structuré'),
        ),
        migrations.AddField(
            model_name='correction',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='correction',
            name='provider',
            field=models.CharField(choices=[('DSK', 'DeepSeek'), ('OLL', 'Ollama'), ('MAN', 'Manuelle')], default='OLL', max_length=3),
        ),
        migrations.AlterField(
            model_name='correction',
            name='raw_response',
            field=models.JSONField(verbose_name="Réponse brute de l'API"),
        ),
        migrations.AlterField(
            model_name='correction',
            name='score',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)]),
        ),
        migrations.AlterField(
            model_name='correction',
            name='solution',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='correction', to='exercices.solution', verbose_name='Solution étudiante'),
        ),
        migrations.AddIndex(
            model_name='correction',
            index=models.Index(fields=['exercice', 'solution'], name='corrections_exercic_d124f8_idx'),
        ),
        migrations.AddIndex(
            model_name='correction',
            index=models.Index(fields=['score'], name='corrections_score_071616_idx'),
        ),
    ]
