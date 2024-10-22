from django.urls import path
from . import views

urlpatterns = [
    path('', views.todoapp_view, name='todoapp_view'),
    path('update/<str:id>/', views.update_todo, name='update_todo'),
    path('delete-item/<int:id>', views.todo_delete, name='todo_delete'),
    path('<int:id>', views.todoapp_view, name='todoapp_view')
]
