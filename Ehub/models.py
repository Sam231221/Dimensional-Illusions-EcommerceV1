from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from decimal import Decimal
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator

# Create your models here.


class Profile(models.Model):
    Gender_Choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    username = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.SlugField(max_length=10, null=True)
    second_name = models.CharField(max_length=10, null=True)

    email = models.EmailField(max_length=140, null=True, blank=True)
    image = models.ImageField(upload_to="thumbnails/profile/%y", help_text="This will be uploaded as your profile picture. Only .png and .jpg are accepted",
                              validators=[FileExtensionValidator(['png', 'jpg'])], blank=True, null=True)
    gender = models.CharField(choices=Gender_Choices, null=True, max_length=50)
    esewa_id = models.PositiveIntegerField(null=True, help_text='This information will be used only for payment purpose.', blank=True, validators=[MinValueValidator(9000000000), MaxValueValidator(9999999999)]
                                           )
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    auth_token = models.CharField(max_length=100, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)

    def get_absolute_url(self):
        return reverse("profileinfo", kwargs={"pk": self.id})


class DiscountCoupon(models.Model):
    discountcode = models.CharField(
        null=True, help_text='For example:- sam3432', max_length=100)
    discount = models.PositiveIntegerField(null=True, verbose_name="Discount in %", help_text='You can set discount from 1 to 90 %. Set the disount wisely.Note,DI do not accept decimal value.', validators=[MinValueValidator(1), MaxValueValidator(90)]
                                           )
    made_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.discountcode)


class SetDiscount(models.Model):
    name = models.CharField(null=True, max_length=100)
    discount = models.PositiveIntegerField(null=True, verbose_name="Discount in %", help_text='You can set discount from 1 to 90 %. Set the disount wisely.Note,DI do not accept decimal value.', validators=[MinValueValidator(1), MaxValueValidator(90)]
                                           )

    def __str__(self):
        return str(self.name)


class Email(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length=100)
    title = models.TextField(null=True)
    content = models.TextField(null=True)
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "Message from " + self.name + ' - ' + self.email


class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    discountcoupon = models.ForeignKey(
        DiscountCoupon, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "Ordered by "+str(self.profile)

 # VFX TOTALS
    @property
    def get_vfxproduct_total(self):
        orderpaidvfxproduct = self.orderpaidvfxproduct_set.all()
        total = sum([item.get_total for item in orderpaidvfxproduct])
        return total

    @property
    def get_vfxproduct_items(self):
        orderpaidvfxproduct = self.orderpaidvfxproduct_set.all()
        total = sum([item.quantity for item in orderpaidvfxproduct])
        return total

 # SFX TOTALS
    @property
    def get_sfxproduct_total(self):
        orderpaidsfxproduct = self.orderpaidsfxproduct_set.all()
        total = sum([item.get_total for item in orderpaidsfxproduct])
        return total

    @property
    def get_sfxproduct_items(self):
        orderpaidsfxproduct = self.orderpaidsfxproduct_set.all()
        total = sum([item.quantity for item in orderpaidsfxproduct])
        return total

 # GRAPHICS TOTALS
    @property
    def get_graphicsproduct_total(self):
        ordergraphicsproduct = self.orderpaidgraphicsproduct_set.all()
        total = sum([item.get_total for item in ordergraphicsproduct])
        return total

    @property
    def get_graphicsproduct_items(self):
        ordergraphicsproduct = self.orderpaidgraphicsproduct_set.all()
        total = sum([item.quantity for item in ordergraphicsproduct])
        return total

# totaamountl of all products
    @property
    def grand_totalamount(self):
        if self.discountcoupon:
            stotal = float(self.get_sfxproduct_total) + \
                float(self.get_vfxproduct_total) + \
                float(self.get_graphicsproduct_total)
            total = stotal-self.discountcoupon.discount/100*stotal
        else:
            total = float(self.get_sfxproduct_total) + \
                float(self.get_vfxproduct_total) + \
                float(self.get_graphicsproduct_total)
        return total


# totalquantity of all products

    @property
    def grand_totalquantity(self):
        total = self.get_sfxproduct_items + \
            self.get_vfxproduct_items+self.get_graphicsproduct_items
        return total


class PurchasedProduct(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    date_purchased = models.DateTimeField(auto_now_add=True, null=True)
    # default is false which means unchecked box
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return "Purchased by " + str(self.profile)
