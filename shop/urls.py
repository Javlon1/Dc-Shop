from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import *


urlpatterns = [
# API

    path('admin/', admin.site.urls),
    path("slider/", Slider.as_view()),
    path("latest-product/", latest_products),
    path("filter-by-price/",filter_by_price),
    path("product-detail/<int:pk>/",ProductDetail.as_view()),
    path("review-get/", RewievGEt.as_view()),
    path("review-post/", RewievPost.as_view()),
    path("contactus/", contactus),
    path("checkout/",CheckOut),
    path("card/",CardView.as_view()),

# Templates

    path('', Index, name='home'),
    path('product/', Productt, name='product'),
    path('add-product/', AddProductt, name='add-product'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

