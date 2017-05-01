# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-01 19:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('images', '0008_auto_20170302_2108'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentBlockLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ContentFollowLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ContentLogoLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FollowLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('usage', models.CharField(blank=True, default='', max_length=255)),
                ('link', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='LogoBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('usage', models.CharField(blank=True, default='', max_length=255)),
                ('link', models.CharField(blank=True, max_length=2048, null=True)),
                ('logo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='images.AttributedImage')),
            ],
        ),
        migrations.CreateModel(
            name='TextBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('usage', models.CharField(blank=True, default='', max_length=255)),
                ('heading', models.TextField(blank=True, default='')),
                ('content', wagtail.wagtailcore.fields.RichTextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('folder', models.CharField(default='themes/default', max_length=1024)),
                ('is_default', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ThemeContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('contact_email', models.EmailField(blank=True, help_text='Only provide if this should be different from the site default email contact address.', max_length=254, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='theme',
            name='content',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='themes.ThemeContent'),
        ),
        migrations.AddField(
            model_name='contentlogolink',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_links', to='themes.LogoBlock'),
        ),
        migrations.AddField(
            model_name='contentlogolink',
            name='theme_content',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='logo_links', to='themes.ThemeContent'),
        ),
        migrations.AddField(
            model_name='contentfollowlink',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_links', to='themes.FollowLink'),
        ),
        migrations.AddField(
            model_name='contentfollowlink',
            name='theme_content',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_links', to='themes.ThemeContent'),
        ),
        migrations.AddField(
            model_name='contentblocklink',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_links', to='themes.TextBlock'),
        ),
        migrations.AddField(
            model_name='contentblocklink',
            name='theme_content',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='block_links', to='themes.ThemeContent'),
        ),
    ]
