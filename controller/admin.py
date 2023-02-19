from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models.functions import TruncMonth
from django.db.models import Sum

from admin_auto_filters.filters import AutocompleteFilter

from .models import Client, Executor, Order, Rate

class MonthFilter(SimpleListFilter):
    title = 'Месяц'
    parameter_name = 'month'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        return (
            (f'{x["month"]}', x["month"].strftime('%B %Y'))
            for x in qs.annotate(month=TruncMonth('creation_date')).values('month').distinct()
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.annotate(month=TruncMonth('creation_date')).filter(month=self.value())
        else:
            return queryset


class ExecutorFilter(AutocompleteFilter):
    title = 'Подрядчик'
    field_name = 'executor'

class ClientFilter(AutocompleteFilter):
    title = 'Клиент'
    field_name = 'client'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'subscription_end')
    search_fields = ['username',]


@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ['username',]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('client',
                       'client_tg_id',
                       'creation_date',
                       'executor',
                       'executor_tg_id',
                       'rate',
                       'is_taken',
                       'is_complete',
                       'estimate',
                       'complete_date',
                       'text',
                       'questions',
                       'answers')
    list_filter = [ClientFilter, ExecutorFilter, MonthFilter, 'is_complete']
    list_display = ('__str__', 'rate', 'executor', 'is_taken', 'is_complete')
    exclude = ['credentials']

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        queryset = response.context_data['cl'].queryset
        total_rate = queryset.aggregate(total_rate=Sum('rate__rate'))['total_rate']
        response.context_data['total_rate'] = total_rate
        return response
     

@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('rate', 'when_set')
