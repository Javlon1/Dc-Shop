from urllib import request
from django.shortcuts import render
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .serializer import *
from rest_framework import viewsets
from . import models


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
        cate = Category.objects.get()
        category = Product.objects.filter(cate_id=id)
        cat = ProductSerializer(category, many=True)
        return Response(cat.data)