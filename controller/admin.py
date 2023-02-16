from django.contrib import admin

from .models import Client, Executor, Order, Rate

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'subscription_end')


@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    ...


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('executor',
                       'is_booked',
                       'rate',
                       'is_taken',
                       'is_complete',
                       'estimate',
                       'complete_date',)

@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    ...