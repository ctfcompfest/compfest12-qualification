from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('signup', views.signUp_view, name="signUp"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('create', views.createForum, name="createForum"),
    path('view/<int:forumid>', views.viewForum, name="viewForum"),
    path('write/<int:forumid>', views.writeForum, name="writeForum")
]
