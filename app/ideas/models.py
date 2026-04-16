from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Idea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='ideas')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_ideas')
    participants = models.ManyToManyField(User, related_name='joined_ideas', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


class Comment(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Comment by {self.author.username} on {self.idea.title}"


class Vote(models.Model):
    VOTE_CHOICES = (
        (1, 'За'),
        (-1, 'Проти'),
    )
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['idea', 'user'], name='unique_user_vote_per_idea')
        ]

    def __str__(self):
        return f"{self.user.username} voted {self.value} on {self.idea.title}"
