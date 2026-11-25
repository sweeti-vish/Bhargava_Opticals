from urllib.parse import quote

from django.contrib import admin
from django.utils.html import format_html

from .models import Brand, Frame, Customer, Order, Review

admin.site.register(Brand)
admin.site.register(Frame)
admin.site.register(Customer)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'frame', 'shop', 'status', 'advance_paid',
                    'created', 'ready_by', 'whatsapp')
    list_editable = ('status', 'advance_paid')
    list_filter = ('status', 'advance_paid', 'shop')

    @admin.display(description='WhatsApp')
    def whatsapp(self, obj):
        c = obj.customer
        name = c.user.first_name
        if obj.status == 'PU':
            label = 'Send thank-you'
            msg = (f"Hello {name}, thank you for visiting Bhargava Opticians! "
                   f"We hope you love your {obj.frame.name}. "
                   f"We would be happy to see you again.")
        elif obj.status == 'RD':
            label = 'Send ready message'
            msg = (f"Hello {name}, your {obj.frame.name} is ready for pickup at "
                   f"{obj.get_shop_display()}, Sironj. "
                   f"- Bhargava Opticians")
        else:
            return '-'
        url = f"https://wa.me/91{c.phone}?text={quote(msg)}"
        return format_html('<a href="{}" target="_blank" rel="noopener">{}</a>', url, label)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'rating', 'approved', 'created')
    list_editable = ('approved',)
    list_filter = ('approved', 'rating')