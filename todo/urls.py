from django.urls import path
from . import views

urlpatterns = [
    path('', views.todos),
    path('<int:todo_id>', views.todo_detail_view),

    path('cbv/', views.TodosListApiView.as_view()),
    path('cbv/<int:todo_id>', views.TodosDetailApiView.as_view()),
]