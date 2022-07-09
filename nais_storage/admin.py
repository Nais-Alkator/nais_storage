from django.contrib import admin
from .models import Storage, Box, Order
from .models import BoxOrder, SeasonItem, SeasonOrder


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'address',
        'contact_phone',
    ]

    list_display = [
        'name',
        'address'
    ]


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]

    list_display = [
        'name',
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = [
        'storage',
        'date_from',
        'date_to',
        'client'
    ]

    list_display = [
        'client',
    ]


@admin.register(BoxOrder)
class BoxOrderAdmin(admin.ModelAdmin):
    search_fields = [  
        'box_size', 
        'date_from',
        'date_to',
        'client'
    ]


@admin.register(SeasonItem)
class SeasonItemAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'category',
    ]

    list_display = [
        'name',
        'category'
    ]


@admin.register(SeasonOrder)
class SeasonOrderAdmin(admin.ModelAdmin):
    search_fields = [  
        'item', 
        'date_from',
        'date_to',
        'client'
    ]
    
    list_display = [
        'client',
        'item'
    ]
