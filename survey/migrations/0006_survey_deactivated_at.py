# Generated by Django 4.2.8 on 2023-12-12 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_alter_answer_id_alter_option_id_alter_question_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='deactivated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
