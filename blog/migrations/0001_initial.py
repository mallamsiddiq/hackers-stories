# Generated by Django 4.0.1 on 2022-02-08 13:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('deleted', models.BooleanField(blank=True, default=False)),
                ('type', models.CharField(max_length=200)),
                ('by', models.CharField(blank=True, max_length=200, null=True)),
                ('time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('dead', models.BooleanField(blank=True, default=False)),
                ('kids', models.CharField(blank=True, max_length=200, null=True)),
                ('parts', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('descendants', models.IntegerField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, default=0)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
