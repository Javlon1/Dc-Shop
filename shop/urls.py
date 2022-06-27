from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import *


urlpatterns = [
# API

    path('admin/', admin.site.urls),
    path("slider/", Slider.as_view()),
    path("latestproduct/", latest_products),
    path("filterbyprice/",filter_by_price),
    path("productdetail/<int:pk>/",ProductDetail.as_view()),
    path("reviewget/", RewievGEt.as_view()),
    path("reviewpost/", RewievPost.as_view()),
    path("card/", CardView.as_view()),
    path("cart-total/", total_card),
    path("check-out/", CheckOut),
    path("wishlist/", WishlistView.as_view()),
    path("blog/", BlogView.as_view()),
    path("blog-text/", BlogtextView.as_view()),
    path("about/", AboutView.as_view()),
    path("about-text/", AbouttextView.as_view()),
    path("replay/", ReplaySend.as_view()),
    path("comment/", CommentSend.as_view()),
    path("login/",Login),

# Templates

    path('', Index, name='home'),
    path('product/', Productt, name='product'),
    path('add-product/', AddProductt, name='add-product'),
    path('edit-product/', EditProductt, name='edit-product'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

