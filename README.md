# Todo - DRF (Django Rest Framework)

Hello and welcome! 👋

This repository is your hands-on guide to mastering Django Rest Framework through the creation of a Todo app. Let’s dive in and code together!


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

هنگام استفاده از Serializer ها باید دو فیلد را به آنها پاس بدهیم.
  1) instance
  2) many: True/False

اگر `many=False` باشد، یک Json فرستاده می شود.
اگر `many=True` باشد لیستی از Json ها فرستاده می شود.

---
