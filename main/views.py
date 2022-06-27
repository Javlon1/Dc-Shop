from itertools import product
from multiprocessing import context
from rest_framework.authtoken.models import Token
from django.shortcuts import render,redirect
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import status
from django.http import Http404
from main.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes,authentication_classes
from main.serializer import *
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from random import *
from .models import User as Users
import random 
import datetime


class CountryView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class EmailView(CreateAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer


class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ImageView(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class Slider(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request):
        slider = Product.objects.all().order_by('-rating')[:5]
        ser = ProductSerializer(slider, many=True)
        return Response(ser.data)


@api_view(['GET'])
def latest_products(request):
    product = Product.objects.all().order_by("-id")[:6]
    prod = ProductSerializer(product, many=True)
    return Response(prod.data)


@api_view(['GET'])
def filter_by_price(request):
    st_price = request.GET.get('st_price')
    end_price = request.GET.get('end_price')
    pr = Product.objects.filter(price__gte=st_price, price__lte=end_price)
    p = ProductSerializer(pr, many=True)
    return Response(p.data)


class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, pk):
        pr = Product.objects.get(id=pk)
        products = Product.objects.filter(category=pr.category)
        DATA = {
            "Product":ProductSerializer(pr).data,
            "Similar Products":ProductSerializer(products,many=True).data,            
        }
        return Response(DATA)


class RewievGEt(APIView):
    def get(self, request):
        Data = {}
        all_products = Product.objects.all()
        for i in all_products:
            a = Review.objects.filter(product_id=i.id)
            for d in a:
                i.rating += d.rating
                Data[i.name] = i.rating/len(a)                
        return Response(Data)


class RewievPost(APIView):
    def post(self, request):
        try:
            rating = request.POST['rating']
            text = request.POST['text']
            product = request.POST['product']
            name = request.POST.get("name")
            email = request.POST.get("email")
            aaa = Review.objects.create(
                rating=rating,
                text=text,
                product_id=product,
                name=name,
                email=email,
            )
            aaa.save()
            all_products = Product.objects.all()
            for i in all_products:
                a = Review.objects.filter(product_id=i.id)
                if len(a) != 0:
                    i.rating = 0
                    for d in a:
                        i.rating += d.rating
                    i.rating = i.rating/len(a)
                    i.save()

            ab = ReviewSerializer(aaa)
            return Response(ab.data)
        except Exception as arr:
            data = {
                'error':f"{arr}"
            }
            return Response(data)


@api_view(['POST'])
def contactus(request):
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    email = request.data['email']
    subject = request.data['subject']
    message = request.data['message']
    ContactUs.objects.create(
        first_name = first_name,
        last_name = last_name,
        email = email,
        subject = subject,
        message = message,
    )
    return Response(status=200)


# def Login(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     if request.method == "POST":
#         username =request.POST.get("username")
#         password = request.POST.get ('password')
#         employe = User.objects.filter(username=username)
#         if employe.count() > 0:
#             if employe[0].check_password(password):
#                 login(request,employe[0])


class CardView(APIView):
    def post(self, request):
        product = request.data['product']
        user = request.data['user']
        quantity = request.data['quantity']
        Card.objects.create(
            product_id=product,
            user_id=user,
            quantity=quantity,
        )
        return Response(status=200)
    
    def get(self, request):
        user = request.GET.get("user")
        uss = Card.objects.filter(user_id=user)
        us = CardSerializer(uss, many=True)
        return Response(us.data)
    

@api_view(['post'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def CheckOut(request):
    user = request.user
    carts = Card.objects.filter(user=user)
    address = User_address.objects.filter(user=user).last()
    DATA = {
        "order":[],
        "bot_message":f"Имя: {user.first_name}\nФамилия: {user.last_name}\nemail: {user.email}\nНомер: {user.phone}\nАдрес: {address.country}, {address.street_address}\n",
    }
    total_price = 0
    for i in carts:
        data = Order.objects.create(
        email=user.email,
        delivery_address=User_address.objects.filter(user=user).last(),
        contact = user.phone,
        product=i.product,
        quantity=i.quantity,
        )
        DATA['order'].append(OrderSerizlizer(data).data)
        DATA['bot_message'] += f"{i.product.name} dan {i.quantity} ta\n"
        total_price += i.product.price * i.quantity

        i.delete()
    DATA['bot_message'] += f"общий сумма: {total_price}"
    token = "5453955664:AAHmbCQcK4NKVevk5wWH1mE0FMG1ad8Dv8E"
    admin = "727134704"
    params = {
       "chat_id": admin,
       "text": DATA['bot_message'],
    }
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resp = requests.post(url, data=params)
    return Response(DATA['order'])


@api_view(['GET'])
def total_card(request):
    user = request.GET.get("user")
    card = Card.objects.filter(user_id=user)
    DATA = {
        "products":[],
        "total_price":0,
    }
    for i in card:
        DATA['total_price'] += i.product.price * i.quantity 
        ser = ProductSerializer(i.product)
        DATA['products'].append(ser.data) 
    
    return Response(DATA)


class WishlistView(APIView):
    def post(self, request):
        product = request.data['product']
        user = request.data['user']
        Wishlist.objects.create(
            product_id=product,
            user_id=user,
        )
        return Response(status=200)
    
    def get(self, request):
        user = request.GET.get("user")
        uss = Wishlist.objects.filter(user_id=user)
        us = WishlistSerializer(uss, many=True)
        return Response(us.data)


@api_view(['post'])
def Login(request):
    username =request.POST.get("username")
    password = request.POST.get ('password')
    try:
        user = Users.objects.get(username=username)
        if user.check_password(password):
            DATA = {
                "token":str(Token.objects.get(user=user))
            }
            return Response(DATA)
        else:
            return Response(status=401)
    except:
        return Response(status=401)


class BlogView(APIView):
    def get(self, request):
        blog = Blog.objects.all().order_by("-id")
        bl = BlogSerizlizer(blog, many=True)
        return Response(bl.data)


class BlogtextView(APIView):
    def post(self, request):
        text = BlogtextSerizlizer(data=request.data)
        if text.is_valid():
            text.save()
            return Response(text.data, status=status.HTTP_201_CREATED)
        return Response(text.errors, status=status.HTTP_400_BAD_REQUEST)


class AboutView(APIView):
    def get(self, request):
        about = About.objects.all().order_by("-id")
        bl = AboutSerizlizer(about, many=True)
        return Response(bl.data)


class AbouttextView(APIView):
    def post(self, request):
        text = AbouttextSerizlizer(data=request.data)
        if text.is_valid():
            text.save()
            return Response(text.data, status=status.HTTP_201_CREATED)
        return Response(text.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplaySend(APIView):
    def post(self, request):
        replay = ReplySerizlizer(data=request.data)
        if replay.is_valid():
            replay.save()
            return Response(replay.data, status=status.HTTP_201_CREATED)
        return Response(replay.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentSend(APIView):
    def post(self, request):
        comment = CommentSerizlizer(data=request.data)
        if comment.is_valid():
            comment.save()
            return Response(comment.data, status=status.HTTP_201_CREATED)
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderSend(APIView):
    def post(self, request):
        order = OrderSerizlizer(data=request.data)
        if order.is_valid():
            order.save()
            return Response(order.data, status=status.HTTP_201_CREATED)
        return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)


def Index(request):
    
    return render(request, 'index.html')


def Productt(request):
    context = {
        'product': Product.objects.all().order_by('-id')
    }
    return render(request, 'product.html', context)


def AddProductt(request):

    return render(request, 'add-products.html')


def EditProductt(request):

    return render(request, 'edit.html')