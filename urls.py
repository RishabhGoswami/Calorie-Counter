from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('/',views.index,name='index'),
    path('/profile',views.profile,name='profile'),
    path('/firstprofile/<int:pd>',views.firstprofile,name='firstprofile'),
    path('/loginfinal',views.loginfinal,name='loginfinal'),
    path('/plans',views.plans,name='plans')
]
