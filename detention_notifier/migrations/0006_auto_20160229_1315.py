# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def delete_detention(apps, schema_editor):
    Detention = apps.get_model("detention_notifier", "Detention")
    Detention.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('detention_notifier', '0005_auto_20160229_1234'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(unique=True, max_length=255)),
                ('process', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='detention',
            name='code',
        ),
        
        migrations.RunPython(delete_detention, migrations.RunPython.noop),
        
        migrations.AddField(
            model_name='detention',
            name='code',
            field=models.ForeignKey(default=None, to='detention_notifier.Code', on_delete=models.CASCADE),
            preserve_default=False,
        ),
    ]
