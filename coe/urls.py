from django.urls import path,include
from coe import views

urlpatterns = [
    #path("", views.home, name="home"),
    #path("docs/", views.schema_view),
    path("/", views.help, name="help"),
    path("hello/<name>", views.hello_there, name="hello_there"),
    path("help", views.help, name="help"),
    path("predict", views.predict, name="predict"),
    path("status", views.status, name="status"),
    path('', include('snippets.urls')),
    #path("predict/?<manufacturer>&<description>", views.predict, name="predict"),
]