from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import *


urlpatterns = [
# API

    path('admin/', admin.site.urls),
    path("api/slider/", Slider.as_view()),
    path("api/country/", CountryView.as_view()),
    path("api/email/", EmailView.as_view()),
    path("api/category/", CategoryView.as_view()),
    path("api/image/", ImageView.as_view()),
    path("api/latestproduct/", latest_products),
    path("api/filterbyprice/",filter_by_price),
    path("api/contactus/",contactus),
    path("api/productdetail/<int:pk>/",ProductDetail.as_view()),
    path("api/reviewget/", RewievGEt.as_view()),
    path("api/reviewpost/", RewievPost.as_view()),
    path("api/card/", CardView.as_view()),
    path("api/cart-total/", total_card),
    path("api/check-out/", CheckOut),
    path("api/wishlist/", WishlistView.as_view()),
    path("api/blog/", BlogView.as_view()),
    path("api/blog-text/", BlogtextView.as_view()),
    path("api/about/", AboutView.as_view()),
    path("api/about-text/", AbouttextView.as_view()),
    path("api/replay/", ReplaySend.as_view()),
    path("api/comment/", CommentSend.as_view()),
    path("api/login/",Login),

# Templates

    path('', Index, name='home'),
    path('product/', Productt, name='product'),
    path('add-product/', AddProductt, name='add-product'),
    path('edit-product/<int:pk>/', EditProductt, name='edit-product'),
    path('blog/', Blogg, name='blog'),
    path('add-blog/', Add_blog, name='add-blog'),
    path('add-about/', Add_about, name='add-about'),
    path('about/', Aboutt, name='about'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

