# Generated by Django 2.1.7 on 2019-03-02 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_auto_20190302_1106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='smartword',
            old_name='word',
            new_name='word_one',
        ),
    ]
