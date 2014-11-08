# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=30)),
                ('pic', models.FileField(upload_to=b'advs_images/')),
                ('upload_date', models.DateField(auto_now_add=True)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BeaconDevice',
            fields=[
                ('uuid', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('location', models.CharField(max_length=250)),
                ('postcode', models.CharField(max_length=10)),
                ('latitude', models.DecimalField(max_digits=10, decimal_places=8)),
                ('longitude', models.DecimalField(max_digits=11, decimal_places=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyDetail',
            fields=[
                ('company_name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('address', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=75)),
                ('mobile', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='beacon',
            field=models.ManyToManyField(to='publish.BeaconDevice'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advertisement',
            name='company',
            field=models.ForeignKey(to='publish.CompanyDetail'),
            preserve_default=True,
        ),
    ]
