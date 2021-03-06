# Generated by Django 3.0.3 on 2020-04-13 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookcomment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.IntegerField()),
                ('num', models.TextField()),
                ('name', models.TextField()),
                ('like_num', models.TextField()),
                ('time', models.TextField()),
                ('snow_nlp', models.TextField()),
            ],
            options={
                'db_table': 'book_comment',
            },
        ),
        migrations.CreateModel(
            name='Bookinfo',
            fields=[
                ('sid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('star', models.TextField()),
                ('tag', models.TextField()),
                ('score', models.TextField()),
                ('info', models.TextField()),
                ('tfidf', models.TextField()),
            ],
            options={
                'db_table': 'book_info',
            },
        ),
    ]
