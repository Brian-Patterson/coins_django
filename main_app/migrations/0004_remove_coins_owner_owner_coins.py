# Generated by Django 4.1.1 on 2022-10-05 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_owner_alter_coins_year_coins_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coins',
            name='owner',
        ),
        migrations.AddField(
            model_name='owner',
            name='coins',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owners', to='main_app.coins'),
        ),
    ]
