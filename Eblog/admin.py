from django.contrib import admin
from . import models
from mptt.admin import MPTTModelAdmin
# Register your models here.

@admin.register(models.Post)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'slug', 'author')

    #when we input characters on title attribute slug attribute also get inputted(prepopulated)
    prepopulated_fields = {
        'slug': ('title',),
         }


admin.site.register(models.Category)



admin.site.register(models.Comment, MPTTModelAdmin)

admin.site.register(models.IpModel)