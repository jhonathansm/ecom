from django.urls import path

from .views import AboutPageView, HomePageView

from products.views import ProductListView

app_name = "pages"

urlpatterns = [
    path("about/", AboutPageView.as_view(), name="about"),
    path("", ProductListView.as_view(), name="home"),
]