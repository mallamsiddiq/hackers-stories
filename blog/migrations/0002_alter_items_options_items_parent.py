# Generated by Django 4.0.1 on 2022-02-09 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='items',
            options={'ordering': ['-time']},
        ),
        migrations.AddField(
            model_name='items',
            name='parent',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
