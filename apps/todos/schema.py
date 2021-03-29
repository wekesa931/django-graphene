import graphene
from graphene_django import DjangoObjectType
from django.core import serializers

from .models import Todo

class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
    
class Query(graphene.ObjectType):
    todos = graphene.List(TodoType)
    
    todo = graphene.Field(
        TodoType,
        id=graphene.Int(),
    )
    
    def resolve_todos(self, info, **kwargs):
        return Todo.objects.all().order_by('-created_on')
    
    def resolve_todo(self, info, id):
        if id is not None:
            return Todo.objects.get(pk=id)
        return None
    
class UpdateTodo(graphene.Mutation):
    class Arguments:
        id = graphene.NonNull(graphene.ID)
        title = graphene.String()
        body = graphene.String()
        completed = graphene.Boolean()
    
    todo = graphene.Field(TodoType)
    
    @staticmethod
    def mutate(root, info, id, title=None,body=None,completed=None):
        # id = args.pop('id')
        todo = Todo.objects.get(pk=id)
        todo.title = title if title is not None else todo.title
        todo.body = body if body is not None else todo.body
        todo.completed = completed if completed is not None else todo.completed
        # todo.set_properties(**args)
        todo.save()

        return UpdateTodo(todo)
    
class DeleteTodo(graphene.Mutation):
    class Arguments:
        id = graphene.NonNull(graphene.ID)
    
    id = graphene.ID()

    @staticmethod
    def mutate(root, info, **args):
        id = args.pop('id')
        todo = Todo.objects.get(pk=id)
        todo.delete()

        return DeleteTodo(id)


class CreateTodo(graphene.Mutation):
    class Arguments:
        title = graphene.NonNull(graphene.String)
        body = graphene.NonNull(graphene.String)
        completed = graphene.NonNull(graphene.Boolean)
        

    todo = graphene.Field(TodoType)

    @staticmethod
    def mutate(root, info, **args):
        todo = Todo(**args)
        todo.save()
        return CreateTodo(todo)

class TodoMutations(graphene.ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()    
# schema = graphene.Schema(query=Query)