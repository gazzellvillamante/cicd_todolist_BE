from django.urls import path

from .views import RegisterView, LoginView, LogoutView, TodoCreateView, TodoListView, TodoDetailView, TodoUpdateView, TodoDeleteView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

# Todo URLs
    path('todos/', TodoListView.as_view(), name='todo-list'),  # View all todos
    path('todos/create/', TodoCreateView.as_view(), name='todo-create'),  # Create todo
    path('todos/<int:pk>/', TodoDetailView.as_view(), name='todo-detail'),  # View single todo
    path('todos/<int:pk>/update/', TodoUpdateView.as_view(), name='todo-update'),  # Update todo
    path('todos/<int:pk>/delete/', TodoDeleteView.as_view(), name='todo-delete'),  # Delete todo
]