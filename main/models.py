from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator,  MinValueValidator
from phone_field import PhoneField


class Country(models.Model):
    name = models.CharField(max_length=255)


class User(AbstractUser):
    type = models.IntegerField(choices=(
        (1, 'Manager'),
        (2, 'User'),
    ), default=3)
    phone = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username
    
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class User_address(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    company_name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    street_address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    phone = PhoneField(blank=True, help_text='phone number')
    email = models.EmailField()


class Info(models.Model):
    logo = models.ImageField(upload_to='Info/')
    in_link = models.URLField()
    tw_link = models.URLField()
    fa_link = models.URLField()
    insta_link = models.URLField()


class Email(models.Model):
    email = models.EmailField()


class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='img/')


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ManyToManyField(Image, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date =  models.DateField(auto_now_add=True)
    text = models.TextField()
    discount = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ], default=0
    )
    rating = models.FloatField(default=0)
    reviews = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    SKU = models.IntegerField(default=1)
    description = models.TextField()
    weight = models.FloatField()
    dimentions = models.CharField(max_length=100)
    colours = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    rating = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date =  models.DateField(auto_now_add=True)


class ContactUs(models.Model):
    first_name = models.CharField(max_length=199)
    last_name = models.CharField(max_length=199)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class Card(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name


class Blog(models.Model):
    img = models.ImageField(upload_to='blog/')
    title = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    blogtext = models.ManyToManyField('Blogtext', blank=True)


class Reply(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    website = models.URLField(max_length=500)
    coment = models.TextField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    data = models.DateField(auto_now_add=True)


class Comment(models.Model):
    replay_comment = models.ForeignKey(Reply, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.TextField()
    data = models.DateField(auto_now_add=True)


class Blogtext(models.Model):
    text = models.CharField(max_length=100)

    

class About(models.Model):
    img = models.ImageField(upload_to='About/')
    title = models.CharField(max_length=255)
    mintext = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    abouttext = models.ManyToManyField('Abouttext', blank=True)


class Abouttext(models.Model):
    text = models.CharField(max_length=100)


class Delivery_Options(models.Model):
    delivery = models.CharField(max_length=255)
    def __str__(self):
        return self.delivery

class Order(models.Model):
    order_number = models.CharField(max_length=255)
    email = models.EmailField()
    status = models.IntegerField(choices=(
        (1, 'Delivered'),
        (2, 'Processing')
    ), default=2)
    order_data = models.DateField()
    delivery_options = models.ForeignKey(Delivery_Options, on_delete=models.PROTECT, blank=True, null=True)
    delivery_address = models.ForeignKey(User_address, on_delete=models.PROTECT)
    contact = PhoneField(blank=True, help_text='phone number')