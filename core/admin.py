from django.contrib import admin

from .models import Platform, Post, Project

admin.site.register([Platform, Project, Post])
