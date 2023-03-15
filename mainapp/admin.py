from django.contrib import admin
from .models import *


class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'first', 'active')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at')


class ChangePasswordAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'ready')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'name', 'created_at')


class SupportAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at')


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'category',
        'title',
        'image',
        'price',
        'active',
        'mainView'
    )
    change_form_template = 'custom_admin/change_form.html'
    #exclude = ('features',)


admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(CommentModel, CommentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(ChangePassword, ChangePasswordAdmin)
admin.site.register(Support, SupportAdmin)
