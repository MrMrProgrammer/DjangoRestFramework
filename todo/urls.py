from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.todos),
    path('<int:todo_id>', views.todo_detail_view),
]