import graphene
import apps.todos.schema

class Query(apps.todos.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=apps.todos.schema.TodoMutations)