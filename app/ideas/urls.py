from django.urls import path

from . import views

urlpatterns = [
    path("", views.idea_list_view, name="idea_list"),
    path("create/", views.idea_create_view, name="idea_create"),
    path("<int:idea_id>/", views.idea_detail_view, name="idea_detail"),
    path("<int:idea_id>/update/", views.idea_update_view, name="idea_update"),
    path("<int:idea_id>/delete/", views.idea_delete_view, name="idea_delete"),
    path("categories/", views.category_list_view, name="category_list"),
    path("categories/create/", views.category_create_view, name="category_create"),
    path(
        "categories/<int:category_id>/",
        views.category_detail_view,
        name="category_detail",
    ),
    path(
        "categories/<int:category_id>/update/",
        views.category_update_view,
        name="category_update",
    ),
    path(
        "categories/<int:category_id>/delete/",
        views.category_delete_view,
        name="category_delete",
    ),
    path("<int:idea_id>/vote/", views.idea_vote_view, name="idea_vote"),
]
