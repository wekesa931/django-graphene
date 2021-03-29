import pytest
from django.test import TestCase
from mixer.backend.django import mixer
from graphene.test import Client

from .models import Todo
from config.schema import schema

todo_list_query = """
    query {
        todos {
            title
            body
            completed
        }
    }   
"""

single_todo_query = """
    query {
        todo(id: 1) {
            id
            title
            body
            completed
        }
    }   
"""

create_todo_mutation = """
        mutation CreateTodo (
        $title: String!,
        $body: String!,
        $completed: Boolean!
            ){
            createTodo(
                title: $title,
                body: $body,
                completed: $completed
            ){
                todo {
                    body
                    title
                    completed
                }
            }
        
    }
"""

update_todo_mutation = """
    mutation UpdateTodo (
        $id: ID!,
        $title: String!,
        $body: String!,
        $completed: Boolean!
    ){
    updateTodo(
        id: $id
        title: $title,
        body: $body,
        completed: $completed
    ){
        todo {
        id
        body
        title
        completed
        }
    }
    
    }
"""
@pytest.mark.django_db
class TestSingleTodoSchema(TestCase):
 
    def setUp(self):
        self.client = Client(schema)
        self.todo = mixer.blend(Todo)
     
    def test_single_todo_query(self):
        response = self.client.execute(single_todo_query, variables={ "id": "1" })
        response_todo = response.get("data").get("todo")
        assert response_todo["id"] == str(self.todo.id)
        
        
@pytest.mark.django_db
class TestTodoSchema(TestCase):
 
    def setUp(self):
        self.client = Client(schema)
        self.todo = mixer.blend(Todo)
        
        
    def test_todo_list_query(self):
        mixer.blend(Todo)
        mixer.blend(Todo)
 
        response = self.client.execute(todo_list_query)
        todos = response.get("data").get("todos")
        ok = response.get("data").get("ok")
         
        assert len(todos)

 
        
    def test_update_todo(self):
        payload = {
            "id": self.todo.id,
            "title": "Changed Titile",
            "body": "Changed Body",
            "completed": False
        }
 
        response = self.client.execute(update_todo_mutation, variables={**payload})
        response_todo = response.get("data").get("updateTodo").get('todo')
        title = response_todo.get("title")
        assert title == payload["title"]
        assert title != self.todo.title 
        
    def test_create_todo(self):
        payload = {
            "title": "My forth Todo",
            "body": "This is my forth todo",
            "completed": False
        }
 
        response = self.client.execute(create_todo_mutation, variables={**payload})
        response_todo = response.get("data").get("createTodo").get("todo")
        # print(response_todo)
        title = response_todo.get("title")
        assert title == payload["title"]