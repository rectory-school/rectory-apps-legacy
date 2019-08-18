# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IconFolderIcon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=1, editable=False, db_index=True)),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageIcon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('icon_height', models.IntegerField(null=True, blank=True)),
                ('icon_width', models.IntegerField(null=True, blank=True)),
                ('display_icon', models.ImageField(height_field=b'icon_height', width_field=b'icon_width', upload_to=b'')),
                ('title', models.CharField(max_length=255)),
                ('classAttr', models.CharField(max_length=255)),
                ('href', models.CharField(max_length=4096)),
                ('internal_description', models.CharField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IconLink',
            fields=[
                ('pageicon_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='paw.PageIcon', on_delete=models.CASCADE)),
                ('url', models.URLField()),
            ],
            options={
            },
            bases=('paw.pageicon',),
        ),
        migrations.CreateModel(
            name='IconFolder',
            fields=[
                ('pageicon_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='paw.PageIcon', on_delete=models.CASCADE)),
                ('uuid', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=('paw.pageicon',),
        ),
        migrations.CreateModel(
            name='PageIconDisplay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=1, editable=False, db_index=True)),
                ('icon', adminsortable.fields.SortableForeignKey(to='paw.PageIcon', on_delete=models.CASCADE)),
                ('page', models.ForeignKey(to='paw.Page', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageTextLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=1, editable=False, db_index=True)),
                ('position', models.CharField(max_length=5, choices=[(b'LEFT', b'Left'), (b'RIGHT', b'Right')])),
                ('page', models.ForeignKey(to='paw.Page', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pagetextlink',
            name='text_link',
            field=adminsortable.fields.SortableForeignKey(to='paw.TextLink', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='iconfoldericon',
            name='icon',
            field=adminsortable.fields.SortableForeignKey(to='paw.IconLink', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='iconfoldericon',
            name='iconFolder',
            field=models.ForeignKey(to='paw.IconFolder', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
