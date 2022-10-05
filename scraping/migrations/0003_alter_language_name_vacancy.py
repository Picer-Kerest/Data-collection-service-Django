# Generated by Django 4.1.2 on 2022-10-05 22:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_language_alter_city_options_alter_city_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=60, unique=True, verbose_name='Programming language'),
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
                ('title', models.CharField(max_length=250, verbose_name='Job title')),
                ('company', models.CharField(max_length=250, verbose_name='Company')),
                ('description', models.TextField(verbose_name='Job description')),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='scraping.city', verbose_name='City')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.language', verbose_name='Programming language')),
            ],
            options={
                'verbose_name': 'vacancy',
                'verbose_name_plural': 'vacancy',
                'ordering': ['-timestamp'],
            },
        ),
    ]
