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
    path("reviewget/", RewievGEt.as_view()),
    path("reviewpost/", RewievPost.as_view()),

    path('', Index, name='home'),
    path('product/', Productt, name='product'),
    path('add-product/', AddProductt, name='add-product'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

