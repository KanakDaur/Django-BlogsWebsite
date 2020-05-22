"""project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf.urls import include
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage_view.as_view(),name = 'home'),
    path('accounts/',include('django.contrib.auth.urls'),{'template_name': 'login.html'}, name='login'),
    path('signup/',views.signupform_view.as_view(model=User,success_url="/accounts/login")),
    path('allblogs/',views.allblogs_view),
    path('myblogs/',views.myblogs_view,name = 'allblogs'),
    path('postblogs/',views.postblogs_view.as_view()),
    path('<int:id>',views.allblogs_detailview,name = 'detail'),
    path('updateblog/<int:pk>',views.update_blogs.as_view()),
    path('deleteblog/<int:pk>',views.delete_blogs.as_view()),
    path('sports_cat/',views.sports_category_view),
    path('travel_cat/',views.travel_category_view),
    path('fashion_cat/',views.fashion_category_view),
    path('food_cat/',views.food_category_view),
    path('educational_cat/',views.educational_category_view),
    path('parenting_cat/',views.parenting_category_view),
    path('movie_music_cat/',views.movie_category_view),
    path('personal_cat/',views.personal_category_view),
    path('other_cat/',views.other_category_view),
    path('draft/',views.draft_view),
    path('edit_profile/',views.edit_profile,name = "edit_profile"),
    path('cmntdelete/<int:pk>',views.comment_delete.as_view()),
    #path('publishblog/<id>',views.draft_publish),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
