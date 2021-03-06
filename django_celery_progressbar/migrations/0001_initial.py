# Generated by Django 3.0.7 on 2020-06-26 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=255, unique=True, verbose_name='task_id')),
                ('total', models.IntegerField(default=100)),
                ('progress', models.IntegerField(default=0)),
                ('step', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
    ]
