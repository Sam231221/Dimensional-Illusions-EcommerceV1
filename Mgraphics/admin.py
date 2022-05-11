from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(FreeGraphicsProduct)
admin.site.register(PaidGraphicsProduct)
admin.site.register(OrderPaidGraphicsProduct)
admin.site.register(GraphicsCategory)