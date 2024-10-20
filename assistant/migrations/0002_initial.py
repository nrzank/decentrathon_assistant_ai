# Generated by Django 4.2.16 on 2024-10-19 06:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assistant', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='searchhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='classified_subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assistant.subject'),
        ),
        migrations.AddField(
            model_name='question',
            name='classified_topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assistant.topic'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.question'),
        ),
        migrations.AddField(
            model_name='agentlog',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.question'),
        ),
    ]
