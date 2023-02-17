from django.contrib import admin

from admin_auto_filters.filters import AutocompleteFilter

from .models import Client, Executor, Order, Rate


class ClientFilter(AutocompleteFilter):
    title = 'Клиент'
    field_name = 'client'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'subscription_end')
    search_fields = ['username',]


@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    ...


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('client_tg_id',
                       'executor',
                       'executor_tg_id',
                       'rate',
                       'is_taken',
                       'is_complete',
                       'estimate',
                       'complete_date',
                       'text')
    list_filter = [ClientFilter]
     

@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    ...