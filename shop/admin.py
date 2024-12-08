from django import forms
from django.contrib import admin
from .models import Orders, Product, Contact, Category,Review

class OrdersAdminForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = '__all__'
        widgets = {
            'products': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        }
class OrdersAdmin(admin.ModelAdmin):
    form = OrdersAdminForm
    list_display = ('fname', 'products', 'price', 'state', 'success_full')  # Use lowercase 'success_full'
    list_filter = ('success_full', 'state')  # Use lowercase 'success_full'
    search_fields = ('fname', 'email', 'phone')

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Contact)
admin.site.register(Orders, OrdersAdmin)
