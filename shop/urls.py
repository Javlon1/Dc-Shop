from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path("slider/", Slider.as_view()),
    path("latestproduct/", latest_products),
    path("filterbyprice/",filter_by_price),
    path("productdetail/<int:pk>/",ProductDetail.as_view()),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

