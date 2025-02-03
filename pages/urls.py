from django.urls import path
from .views import home, join_us, join_us_success, get_ranks

urlpatterns = [
    path("", home, name="home"),
    path("join-us/", join_us, name="join_us"),
    path("join-us/success/", join_us_success, name="join_us_success"),
    path("get-ranks/", get_ranks, name="get_ranks"),
]
