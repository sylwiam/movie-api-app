# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-07 19:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metadata_api', '0003_temp_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(default='', max_length=500)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.CharField(max_length=10, unique=True)),
                ('title', models.CharField(max_length=500)),
                ('year', models.CharField(max_length=6)),
                ('rating', models.FloatField()),
                ('votes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_pk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metadata_api.Genre')),
                ('movie_pk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metadata_api.Movie')),
            ],
        ),
        migrations.AlterField(
            model_name='temp',
            name='genre',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='temp',
            name='title',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='temp',
            name='year',
            field=models.CharField(max_length=6),
        ),
    ]
