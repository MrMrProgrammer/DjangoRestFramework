# DRF (Django Rest Framework)

Hello and welcome! 👋

This repository is your hands-on guide to mastering Django Rest Framework. Let’s dive in and code together!


### نکات:
---
1- در جنگو تا وقتی یک کوئریست تبدیل به لیست نشود و یا روی آن حلقه زده نشود، execute نمیشود. برای مثال :

`todos = list(Todo.objects.order_by('priority').all()`

یا

```
todo_list = []
for todo in todos:
  todo_list.append(
    {
      "title": todo.title,
      "is_done": todo.is_done
    }
  )   
```

---
2- اگر بخواهیم مقادیر خاصی از یک مدل را واکشی کنیم، میتوانیم از `values()` استفاده کنیم. برای مثال :

`todos = list(Todo.objects.order_by('priority').all().values('title', 'is_done')`

---

3- برای انتخاب Serializer ما 2 گزینه داریم :
  1) ModelSerializer
  2) Serializer

در حالت ModelSerializer روی یک مدل خاص اعمال میشود و نمونه های ما را تبدیل به Json و یا لیستی از Json ها میکند.

در حالت Serializer به صورت custom این فرآیند شکل میگیرد (مانند Schemas در Fastapi).

---

4- هنگام فرآیند Serializer ها باید دو فیلد زیر را به آنها پاس بدهیم.
  1) instance
  2) many: True/False

اگر `many=False` باشد، یک Json فرستاده می شود.
اگر `many=True` باشد لیستی از Json ها فرستاده می شود.

---

5- هنگامی که میخواهم فرآیند De-Serialize را انجام بدهیم، در متد `POST` باید `data` را به آن پاس بدهیم. در متد `PUT` باید `instance` و `data` را به آن بدهیم.

---
6- با استفاده از متد `is_valid()` میتوانیم ورودی api را اعتبارسنجی کنیم. برای مثال داریم:

```python
if request.method == 'POST':
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
```

---
7- در `decorator` به نام `api_view` لیست متد های قابل پردازش برای api را مشخص میکنیم. برای مثال داریم:

```python
@api_view(['GET', 'POST'])
def todos(request: Request):
    if request.method == 'GET':
      .
      .
      .
```

---
8- با استفاده از `fields` در `serializer` میتوانیم فیلد های ورودی api را مشخص کنیم. برای مثال داریم :
```python
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
```

یا

```python
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title']
```

---
9- برای واکشی یک Object از دیتابیس میتوانیم به روش های زیر عمل کنیم:

  1) `filter()`

  ```python
  todo: Todo = Todo.objects.filter(pk=1).first()
  ```

  2) `get_object_or_404()`:

  ```python
  from django.shortcuts import get_object_or_404

  todo: Todo = get_object_or_404(Todo, pk=todo_id)
  ```

  3) `get()`:

  ```python
  try:
    todo: Todo = Todo.objects.get(pk=todo_id)
  except Todo.DoesNotExist:
    return Response(None, status.HTTP_404_NOT_FOUND)
  ```

---
10- برای ایجاد API های بزرگ تر و پیچیده تر بهتر است از `CBV` ها استفاده کنم. برای مثال داریم :

```python
class TodosListApiView(APIView):
    def get(self, request: Request):
        todos = Todo.objects.order_by('priority').all()
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data, status.HTTP_200_OK)

    def post(self, request: Request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)
```

و یا مثالی دیگر:

```python
class TodosDetailApiView(APIView):

    def get_object(self, todo_id: int):
        try:
            todo: Todo = Todo.objects.get(pk=todo_id)
            return todo
        except Todo.DoesNotExist:
            raise NotFound()

    def get(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        serializer = TodoSerializer(todo, request.data)        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)
```

---
11- هنگامی که یک Object موجود نباشد، میتوانیم به صورت زیر این خطا را بازگردانیم:

```python
from rest_framework.exceptions import NotFound

try:
    todo: Todo = Todo.objects.get(pk=todo_id)
    return todo
except Todo.DoesNotExist:
    raise NotFound()
```

همچنین برای نمایش خطا میتوانیم جزئیات خطا را به صورت زیر بازگردانیم:

```python
return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
```

---

12- همانطور که میدانید در `urls.py` باید از `()as_view` برای `CBV` ها استفاده کنیم:

```python
path('cbv/', views.TodosListApiView.as_view())
```

---
13- با استفاده از قدرت Mixin ها در CBV و ارث بری چندگانه در پایتون میتوانیم از چندباره نویسی کدها جلوگیری کنیم. برای مثال داریم:

```python
from rest_framework import mixins, generics

class TodosListMixinApiView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer

    def get(self, request: Request):
        return self.list(request)
    
    def post(self, request: Request):
        return self.create(request)
```

و یا مثالی دیگر:

```python
class TodosDetailMixinApiView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer

    def get(self, request: Request, pk: int):
        return self.retrieve(request, pk)
    
    def put(self, request: Request, pk: int):
        return self.update(request, pk)
    
    def delete(self, request: Request, pk: int):
        return self.destroy(request, pk)
```

عملیات CRUD را به صورت زیر انجام میدهیم :

```
C ---> mixins.CreateModelMixin ---> self.create(request)
R ---> mixins.RetrieveModelMixin ---> self.retrieve(request, pk)
U ---> mixins.UpdateModelMixin ---> self.update(request, pk)
D ---> mixins.DestroyModelMixin ---> self.destroy(request, pk)
```

همچنین برای بازگرداندن لیستی از Object های مور نظر داریم:
```
mixins.ListModelMixin ---> self.list(request)
```

---
14- با استفاده از Generic ها عملا نیاز به کد زدن ندارید :)

تمامی عملیات C, R, U, D, List به صورت زیر پیاده سازی می شود:

```python
class TodosGenericApiView(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer

class TodosDetailGenericApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
```

----
15- کار با ViewSets :)

```python
class TodosViewSetApiView(viewsets.ModelViewSet):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
```

برای آدرس دهی در ViewSets ها باید در فایل urls.py به صورت زیر عمل کنیم:

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.TodosViewSetApiView)

urlpatterns = [
    path('viewsets/', include(router.urls)),
]
```
و تمام :)

---
