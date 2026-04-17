from django import forms

from .models import Category, Comment, Idea


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ["title", "description", "category"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": "Ваш коментар"}
        widgets = {"text": forms.Textarea(attrs={"rows": 3})}
