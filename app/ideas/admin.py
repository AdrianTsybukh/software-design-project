from django.contrib import admin

from .models import Category, Comment, Idea, IdeaParticipant, Vote


class IdeaParticipantInline(admin.TabularInline):
    model = IdeaParticipant
    extra = 1


class IdeaAdmin(admin.ModelAdmin):
    inlines = [IdeaParticipantInline]
    list_display = ("title", "category", "author", "created_at")
    list_filter = ("category", "created_at")


admin.site.register(Category)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(Comment)
admin.site.register(Vote)
