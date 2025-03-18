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
