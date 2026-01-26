from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect
from .models import Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'price', 'quantity')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'full_name', 'status_badge', 'action_buttons')
    list_filter = ('status',)
    search_fields = ('order_id', 'phone')
    inlines = [OrderItemInline]
    readonly_fields = ('order_id', 'user')

    # STATUS BADGE (Colors)
    def status_badge(self, obj):
        colors = {'Pending': '#ffc107', 'Accepted': '#0d6efd', 'Shipped': '#6f42c1', 'Delivered': '#198754', 'Cancelled': '#dc3545'}
        return format_html('<span style="color:white; background:{}; padding:5px 10px; border-radius:10px;">{}</span>', colors.get(obj.status, 'grey'), obj.status)
    status_badge.short_description = 'Status'

    # ACTION BUTTONS (Accept | Reject | Print)
    def action_buttons(self, obj):
        buttons = ""
        if obj.status == 'Pending':
            # Accept Button Logic (Hum URL hack use karenge ya actions)
            # Simple rakhne ke liye hum Django Actions use karenge jo upar dropdown me hoti hain
            return format_html('<span style="color:orange;">⚠ Waiting Action</span>')
        
        if obj.status in ['Accepted', 'Shipped']:
            url = reverse('admin_print_label', args=[obj.id])
            buttons += f'<a href="{url}" target="_blank" style="background:#333; color:white; padding:3px 8px; border-radius:4px; text-decoration:none;">🖨️ Label</a>'
        
        return format_html(buttons)
    action_buttons.short_description = 'Actions'

    # BULK ACTIONS (Select karke Accept/Reject karna)
    actions = ['mark_accepted', 'mark_rejected', 'mark_shipped']

    def mark_accepted(self, request, queryset):
        queryset.update(status='Accepted')
    mark_accepted.short_description = "✅ Accept Selected Orders"

    def mark_rejected(self, request, queryset):
        queryset.update(status='Cancelled')
    mark_rejected.short_description = "❌ Reject/Cancel Selected Orders"

    def mark_shipped(self, request, queryset):
        queryset.update(status='Shipped')
    mark_shipped.short_description = "🚚 Mark as Shipped"

admin.site.register(Product)
admin.site.register(Order, OrderAdmin)