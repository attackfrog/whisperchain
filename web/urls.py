from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("chain/<str:code>", views.chain, name="chain"),
    path("chain", views.post_chain, name="post_chain"),
    path("create", views.create, name="create"),
    path("join", views.join, name="join"),
    path("chain/<str:chain_code>/submit", views.submit, name="submit"),
    path("credits", views.credits, name="credits"),
]
