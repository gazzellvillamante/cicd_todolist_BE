from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from todolist_app.models import Todo
from rest_framework.test import APIClient

from todolist_app.serializer import TodoSerializer


class TodoViewsTestCase(TestCase):
    def setUp(self):
        # Create a user and an API token for authentication
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)

        # Use the APIClient from DRF, which has the force_authenticate method
        self.client = APIClient()
        self.client.force_authenticate(user=self.user, token=self.token)


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
        # Test creating a new Todo item
        url = reverse('todo-create')  # Use the correct endpoint
        data = {'user': self.user.id ,'title': 'New Todo', 'description': 'Test Description', 'completed': 'false'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Expect 201 Created

    def test_todo_update(self):
        # First create a Todo item to update
        todo = Todo.objects.create(user=self.user, title='Initial Title', description='Initial Description', completed = False)
        url = reverse('todo-update', kwargs={'pk': todo.id})
        data = {'user': self.user.id ,'title': 'Updated Title', 'description': 'Updated Description', 'completed': 'true'}
        response = self.client.put(url, data, format='json')  # Use PUT for updates
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Expect 200 OK


    def test_todo_list(self):
        """Test listing Todo items"""
        url = reverse('todo-list')  # Make sure the URL name is correct
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_todo_delete(self):
        """Test deleting a Todo item"""
        todo = Todo.objects.create(
            user=self.user, title="Test Title", description="Test description", completed=False
        )
        url = reverse('todo-delete', args=[todo.id])  # Ensure the URL name is correct
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)
