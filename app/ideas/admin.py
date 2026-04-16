from django.contrib import admin
from .models import Category, Idea, Comment, Vote

# Register your models here.

admin.site.register(Category)
admin.site.register(Idea)
admin.site.register(Comment)
admin.site.register(Vote)
