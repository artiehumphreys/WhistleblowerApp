# Generated by Django 4.2.10 on 2024-04-15 22:11

from django.db import migrations, models
import uuid

def generate_uuids(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    if 'postgresql' in db_alias:
        schema_editor.execute('ALTER TABLE whistleblower_app_submission ADD COLUMN new_id UUID DEFAULT uuid_generate_v4();')
        schema_editor.execute('UPDATE whistleblower_app_submission SET new_id = uuid_generate_v4();')
        schema_editor.execute('ALTER TABLE whistleblower_app_submission DROP COLUMN id;')
        schema_editor.execute('ALTER TABLE whistleblower_app_submission RENAME COLUMN new_id TO id;')
        schema_editor.execute('ALTER TABLE whistleblower_app_submission ADD PRIMARY KEY (id);')

class Migration(migrations.Migration):
    dependencies = [
        ('whistleblower_app', '0004_submission_uploadedfile_submission'),
    ]

    operations = [
        migrations.RunPython(generate_uuids, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='uploadedfile',
            name='description',
            field=models.TextField(default=''),
        ),
    ]