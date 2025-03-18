from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from .serializers import Todoserializer
from .models import Todo

# ------------------------------------------------------------------------------------------------

# Without Serializer
# @api_view(['GET'])
# def todos(request: Request):
#     todos: list[Todo] = Todo.objects.order_by('priority').all().values('title', 'is_done')
#     return Response({"todos": todos}, status.HTTP_200_OK)

# With Serializer
@api_view(['GET', 'POST'])
def todos(request: Request):
    if request.method == 'GET':
        todos = Todo.objects.order_by('priority').all()
        todo_serializer = Todoserializer(todos, many=True)
        return Response(todo_serializer.data, status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = Todoserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
    
    else:
        Response(None, status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------------
