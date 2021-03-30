### django-graphene
Technologies
1. Django
2. graphene-django
3. Postgres
4. Heroku

To install the project
```
$ git clone https://github.com/wekesa931/django-graphene.git
$ cd django-graphene
$ pip install requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

Heroku url: `https://django-graphene.herokuapp.com/graphql/`

## To post data

**Query**
```
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
```
**payload**

```
{
  "title": "My Todo",
  "body": "This is my todo",
  "completed": false
}
```

## To get data

```
query {
  todos {
    id
    title
    body
    completed
  }
}
```

## To get data single data

```
  todo(id: 1) {
    id
    title
    body
    completed
  }

```

## To update data
```
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
```

**payload**
```
{
    "id": "1",
    "title": "Changed Titile",
    "body": "CHanged Body",
    "completed": false
}
```

## To delete data
```
    mutation DeleteTodo (
        $id: ID!
    ){
    deleteTodo(
        id: $id
    ){
        id
    }
    
    }
```

**payload**
{
	"id": "1"
}