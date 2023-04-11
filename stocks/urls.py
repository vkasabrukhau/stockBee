from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('add', views.add, name="add"),
    path("<int:stock_id>", views.stock, name="stock"),
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('profile', views.profile, name="profile")
]