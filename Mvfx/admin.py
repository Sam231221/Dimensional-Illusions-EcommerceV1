from Mvfx.models import FreeVfxProduct
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(FreeVfxProduct)
admin.site.register(PaidVfxProduct)
admin.site.register(OrderPaidVfxProduct)
admin.site.register(VfxCategory)