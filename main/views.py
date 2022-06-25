from rest_framework.authtoken.models import Token
from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import status
from django.http import Http404
from main.models import *
from main.serializer import *
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from random import *
from .models import User as Users
import random 
import datetime

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

    # def retrieve(self, request, pk):
    #     products = Product.objects.all()
    #     all = []
    #     for product in products:
    #         data = {
    #             "Product Info": product
    #         }
    #     dat = {
    #         data,
    #         "Similar Products":
            
    #     }

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


def Index(request):
    
    return render(request, 'index.html')


def Productt(request):

    return render(request, 'product.html')


def AddProductt(request):

    return render(request, 'add-products.html')