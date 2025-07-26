from django.urls import path
from .views import *
from . import views
from .views import export_readers_to_s3

urlpatterns = [
    path("", home),
    path("home", home),
    path("readers", readers_tab),
    path("save", save_student),
    path("readers/add", save_reader),
    path("readers/edit/<int:reader_id>/", views.edit_reader, name="edit_reader"),
    path("readers/delete/<int:reader_id>/", views.delete_reader, name="delete_reader"),
    path("readers/export/", views.export_readers_to_s3, name="export_readers"),
]
