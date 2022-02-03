from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


# Create your models here.
class Setting(models.Model):
    c_name = models.CharField(max_length=255, unique=True)
    c_email = models.CharField(max_length=255, unique=True)
    c_email_1 = models.CharField(max_length=255, unique=True, null=True, blank=True)
    c_email_2 = models.CharField(max_length=255, unique=True, null=True, blank=True)
    c_phone = models.CharField(max_length=30)
    c_phone1 = models.CharField(max_length=30, null=True, blank=True)
    c_phone2 = models.CharField(max_length=30, null=True, blank=True)
    c_address = models.CharField(max_length=30)
    c_logo = models.ImageField(upload_to='logo', null=True, blank=True)
    c_meta_title = models.TextField()
    c_meta_description = models.TextField()

    def __str__(self):
        return self.c_name

    def get_company_name(self):
        c_name = str(self.c_name)
        return c_name.title()


class Attribute(models.Model):
    attribute_name = models.CharField(max_length=255)

    def __str__(self):
        return self.attribute_name


class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=255, unique=True)
    attribute_id = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    def __str__(self):
        return self.attribute_value


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_slug = models.SlugField(max_length=255, unique=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    m_price = models.IntegerField(default=0)
    s_price = models.IntegerField(default=0)
    d_price = models.IntegerField(default=0)
    product_image = models.ImageField(upload_to='products')
    summary = models.TextField(blank=True)
    description = RichTextField(blank=True)

    def __str__(self):
        return self.product_name


class ProductImage(models.Model):
    product_image_name = models.ImageField(upload_to='products/images')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductAttribute(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute_value_id = models.ManyToManyField(AttributeValue)


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class UniqueCart(models.Model):
    buyer_id = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Unique Cart: " + str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(UniqueCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    sub_total = models.PositiveIntegerField(default=0)


class Order(models.Model):
    cart = models.OneToOneField(UniqueCart, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    rate = models.PositiveIntegerField(default=0)
    sub_total = models.PositiveIntegerField(default=0)
