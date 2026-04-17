from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, CommentForm, IdeaForm
from .models import Category, Idea, Vote


def idea_list_view(request):
    ideas = Idea.objects.all()
    context = {"title": "Список ідей", "ideas": ideas}
    return render(request, "ideas/idea_list.html", context=context)


def idea_detail_view(request, idea_id: int):
    idea = get_object_or_404(Idea, id=idea_id)
    comments = idea.comments.all().order_by("-created_at")

    if request.method == "POST" and "submit_comment" in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.idea = idea

            from django.contrib.auth import get_user_model

            new_comment.author = get_user_model().objects.first()

            new_comment.save()
            return redirect("idea_detail", idea_id=idea.id)
    else:
        comment_form = CommentForm()

    upvotes = idea.votes.filter(value=Vote.Value.UPVOTE).count()
    downvotes = idea.votes.filter(value=Vote.Value.DOWNVOTE).count()

    context = {
        "title": idea.title,
        "idea": idea,
        "comments": comments,
        "comment_form": comment_form,
        "upvotes": upvotes,
        "downvotes": downvotes,
    }
    return render(request, "ideas/idea_detail.html", context=context)


def idea_vote_view(request, idea_id: int):
    if request.method == "POST":
        idea = get_object_or_404(Idea, id=idea_id)
        vote_value = int(request.POST.get("vote_value", 0))

        from django.contrib.auth import get_user_model

        user = get_user_model().objects.first()

        if vote_value in dict(Vote.Value.choices):
            Vote.objects.update_or_create(
                idea=idea, user=user, defaults={"value": vote_value}
            )

    return redirect("idea_detail", idea_id=idea_id)


def idea_create_view(request):
    if request.method == "POST":
        form = IdeaForm(request.POST)
        if form.is_valid():
            new_idea = form.save(commit=False)
            from django.contrib.auth import get_user_model

            new_idea.author = get_user_model().objects.first()
            new_idea.save()
            return redirect("idea_list")
    else:
        form = IdeaForm()

    context = {"title": "Створення ідеї", "form": form}
    return render(request, "ideas/idea_form.html", context=context)


def idea_update_view(request, idea_id: int):
    idea = get_object_or_404(Idea, id=idea_id)

    if request.method == "POST":
        form = IdeaForm(request.POST, instance=idea)
        if form.is_valid():
            form.save()
            return redirect("idea_detail", idea_id=idea.id)
    else:
        form = IdeaForm(instance=idea)

    context = {"title": "Редагування ідеї", "form": form, "idea": idea}
    return render(request, "ideas/idea_form.html", context=context)


def idea_delete_view(request, idea_id: int):
    idea = get_object_or_404(Idea, id=idea_id)

    if request.method == "POST":
        idea.delete()
        return redirect("idea_list")

    context = {"title": "Видалення ідеї", "idea": idea}
    return render(request, "ideas/idea_confirm_delete.html", context=context)


def category_list_view(request):
    categories = Category.objects.all()
    context = {"title": "Категорії", "categories": categories}
    return render(request, "ideas/category_list.html", context=context)


def category_detail_view(request, category_id: int):
    category = get_object_or_404(Category, id=category_id)
    context = {
        "title": category.name,
        "category": category,
        "ideas": category.ideas.all(),
    }
    return render(request, "ideas/category_detail.html", context=context)


def category_create_view(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form = CategoryForm()

    context = {"title": "Створення категорії", "form": form}
    return render(request, "ideas/category_form.html", context=context)


def category_update_view(request, category_id: int):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("category_detail", category_id=category.id)
    else:
        form = CategoryForm(instance=category)

    context = {"title": "Редагування категорії", "form": form, "category": category}
    return render(request, "ideas/category_form.html", context=context)


def category_delete_view(request, category_id: int):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        category.delete()
        return redirect("category_list")

    context = {"title": "Видалення категорії", "category": category}
    return render(request, "ideas/category_confirm_delete.html", context=context)
