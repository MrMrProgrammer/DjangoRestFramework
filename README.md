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

5- هنگامی که میخواهم فرآیند De-Serialize را انجام بدهیم، در متد `POST` باید مقدار `data` را به آن پاس بدهیم. در متد `PUT` باید مقدار `instance` و `data` را به آن بدهیم.

---
6- با استفاده از متد `is_valid()` میتوانیم ورودی api را اعتبارسنجی کنیم. برای مثال داریم:

```python
if request.method == 'POST':
    serializer = Todoserializer(data=request.data)
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
class Todoserializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
```

یا

```python
class Todoserializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title']
```

```