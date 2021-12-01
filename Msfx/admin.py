from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(FreeSfxProduct)
admin.site.register(PaidSfxProduct)
admin.site.register(OrderPaidSfxProduct)
admin.site.register(SfxCategory)