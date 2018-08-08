from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("profile", views.profile, name="profile"),
    path("chain/<str:code>", views.chain, name="chain"),
    path("chain", views.post_chain, name="post_chain"),
    path("create", views.create, name="create")
]
