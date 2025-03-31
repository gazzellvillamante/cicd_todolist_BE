from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from todolist_app.models import Todo

class TodoViewsTestCase(TestCase):
    def setUp(self):
        """Set up the test user and token"""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_register(self):
        """Test the registration endpoint"""
        url = reverse('register')  # Make sure the URL name is correct
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_todo_create(self):
        """Test creating a new Todo item"""
        url = reverse('todo-create')  # Make sure the URL name is correct
        data = {
            'title': 'Test Todo',
            'description': 'This is a test todo',
            'completed': False,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_todo_list(self):
        """Test listing Todo items"""
        url = reverse('todo-list')  # Make sure the URL name is correct
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_todo_update(self):
        """Test updating a Todo item"""
        todo = Todo.objects.create(
            user=self.user, title="Old Title", description="Old description", completed=False
        )
        url = reverse('todo-update', args=[todo.id])  # Ensure the URL name is correct
        data = {
            'title': 'Updated Title',
            'description': 'Updated description',
            'completed': True,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo.refresh_from_db()
        self.assertEqual(todo.title, 'Updated Title')
        self.assertEqual(todo.description, 'Updated description')

    def test_todo_delete(self):
        """Test deleting a Todo item"""
        todo = Todo.objects.create(
            user=self.user, title="Test Title", description="Test description", completed=False
        )
        url = reverse('todo-delete', args=[todo.id])  # Ensure the URL name is correct
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)
