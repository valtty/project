from django.contrib import admin
from .models import User, Application, Review

admin.site.register(User)
admin.site.register(Application)
admin.site.register(Review)