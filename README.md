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
16- میخواهیم هنگامی که لیست کاربران را نشان میدهیم، لیست Todo های هر کاربر را نیز نمایش بدهیم.
برای این کار باید از مفهوم `Nested Serializers` استفاده کنیم. برای این کار داریم:

```python
# Add user

class Todo(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    priority = models.IntegerField(default=1)
    is_done = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
```

```python
# Create User Serializer

class UserSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
```

finally

```python
class UserGenericApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

### Important point !
```python
# Add related_name
user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
```

---
17- برای ایجاد Pagination به صورت Global برای CBVها میتوانیم در فایل `settings.py` تنظیمات زیر را اعمال کنیم:

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": "10"
}
```
در DRF دو نوع Pagination وجود دارد:
```
1- PageNumberPagination
2- LimitOffsetPagination
```
در `PageNumberPagination` با شماره صفحه جدا میشود و در هر صفحه به اندازه `PAGE_SIZE` نمایش داده خواهد شد.

در `LimitOffsetPagination` با دو فیلد `limit` و `offset` محتوای هر صفحه واکشی میشود. `limit` تعداد آیتم های نمایش داده شده در هر صفحه است و `offset` تعداد آیتم هایی است که skeep شده است.

آین تنظیمات به صورت Global بر روی تمام CBV ها اعمال میشود. همچنین میتوانیم یک CBV دلخواه را به صورت دستی با تنظیمات Pagination متفاوتی تنظیم کنیم. برای مثال داریم :

```python
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class TodosGenericApiViewPagination(PageNumberPagination):
    page_size = 10

class TodosGenericApiView(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = TodosGenericApiViewPagination
```
و همچنین:
```python
class TodosViewSetApiView(viewsets.ModelViewSet):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = LimitOffsetPaginationV
```

---
18- برای پیاده سازی سیستم `Authentication` در DRF روش های متفاوتی وجود دارد.

یکی از این روش های `Basic Authentication` است. برای پیاده سازی این روش به صورت Global روی تمام CBV ها میتوانیم به صورت زیر عمل کنیم:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.BasicAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"]
}
```
همچنین روش اعمال آن بر روی یک CBV خاص به صورت زیر است:
```python
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class TodosGenericApiView(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
```

---
19- برای پیاده سازی `Token Authentication` باید چند مرحله زیر را دنبال کنیم:

1- اضافه کردن `rest_framework.authtoken` به `INSTALLED_APPS`
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
]
```

2- استفاده از `TokenAuthentication` به عنوان `DEFAULT_AUTHENTICATION_CLASSES`
```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.TokenAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"]
}
```

3- انجام `migrate` برای ایجاد جدول جهت نگهداری توکن در دیتابیس

4- ایجاد view برای دریافت توکن. برای اینکار میتوانیم از view آماده DRF استفاده کنیم. این view نام کاربری و رمز عبور را دریافت میکند و توکن ایجاد میکند.

```python
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    ...
    path('auth-token/', obtain_auth_token, name='generate_auth_token')
]
```
به این ترتیب میتوانیم نام کاربری و رمز عبور را به ویو مربوط به `auth-token` ارسال کنیم و یک توکن دریافت کنیم. سپس در هدر درخواست در کلید `Authorization` مقداری مانند `Token c06b08fab2e37e659d2a70d9c9d348f11b363e20` قرار میدهیم.

---
20- برای پیاده سازی فرآیند احرازهویت با استفاده از JWT میتوانیم از کتابخانه‌ی `djangorestframework-simplejwt` استفاده کنیم. برای این کار کافیست مراحل زیر را انجام بدهیم.

1- نصب کتابخانه‌ی `djangorestframework-simplejwt`:
```bash
pip install djangorestframework-simplejwt
```

2- استفاده از JWT به عنوان روش احرازهویت:
```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': [
        ...
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
    ...
}
```

3- اضافه کردن URL های مربوط به دریافت توکن و رفرش توکن:
```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    ...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ...
]
```

با این تغییرات اگر `username` و `password` را به سمت `api/token/` ارسال کنیم، یک `access` و یک `refresh` دریافت خواهیم کرد.

با استفاده از `access` در هدر درخواست به صورت زیر میتوانیم به دیتای مورد نظر دسترسی داشته باشیم:
```
"Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5c..."
```

---
21- اگر به فیلدهای `model` مقدار `null` بدهیم، باید `migration` انجام بدهیم ولی اگر `blank` بدهیم، نیازی به `migration` ندارد و تنها رشته خالی ذخیره میکند.

---
22- اگر بخواهیم روی فیلدهای `serializer` فرآیند `validation` انجام بدهیم به یکی از دو روش زیر میتوانیم این کار را انجام بدهیم:

1- استفاده از توابع `validate_[attr_name]`:

میتوانیم در `serializer` توابعی با نام فیلد موردنظر ایجاد کنیم فرآیند اعتبارسنجی را درون آن پیاده سازی کنیم. 
```python
def validate_priority(self, priority):
    if 10 < priority < 20:
        return priority
    raise serializers.ValidationError('priority is not OK!')
```

2- استفاده از تابع `validate`:

میتوانیم تابع `validate` را ایجاد کنیم و روی فیلدهای دلخواه اعتبار سنجی انجام بدهیم. در این تابع لیست تمامی فیلدها وجود دارد.

```python
def validate(self, attrs):
    if 10 < attrs['priority'] < 20:
        return super().validate(attrs)
    raise serializers.ValidationError('priority is not OK!')
```

---
23- برای ایجاد داکیومنت swagger میتوانیم از کتابخانه‌ی `drf-spectacular` استفاده کنیم. برای این کار باید مراحل زیر را انجام بدهیم:

1- نصب کتابخانه‌ی `drf-spectacular`:
```bash
pip install drf-spectacular
```

2- اضافه کردن کتابخانه به `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    'drf_spectacular',
]
```

3- تغییر `DEFAULT_SCHEMA`:
```python
REST_FRAMEWORK = {
    # YOUR SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

4- تنظیمات `SPECTACULAR`:
```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}
```

5- اضافه کردن URLها:
```python
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

---
24- هنگامی که از FBV یا CBVها به صورت پیش فرض استفاده میکنم، این کتابخانه نمیتواند مقادیر ورودی و خروجی API را تشخیص بدهد. برای تنظیم این مقادیر یا اضافه کردن توضیحات باید به صورت زیر عمل کنیم:
```python
class TodosListApiView(APIView):

    def get(self, request: Request):
        todos = Todo.objects.order_by('priority').all()
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data, status.HTTP_200_OK)

    @extend_schema(
        request=TodoSerializer,
        ...
    )
    def post(self, request: Request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)
```

---