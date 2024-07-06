from django.urls import path, include
from .views import CreateDjangoUser, GetDjangoUser, CreateGroup, GetGroup, UpdateNotionPageView

urlpatterns = [

    path('create-django-user/', CreateDjangoUser.as_view(), name='create-cliente'),
    path('get-django-user/', GetDjangoUser.as_view(), name='get-cliente'),
    path('create-django-group/', CreateGroup.as_view(), name='create-group'),
    path('get-django-group/', GetGroup.as_view(), name='get-group'),
    path('update-notion/', UpdateNotionPageView.as_view(), name='get-group'),
]

