from django.contrib import admin
from models import *


# Register your models here.

class GoodsInventoryAdmin(admin.ModelAdmin):
    search_fields = ['barcode']


admin.site.register(FuelOrder)
admin.site.register(FuelTank)
admin.site.register(Site)
admin.site.register(GoodsOrder)
admin.site.register(InventoryRecord)
admin.site.register(Classification)
admin.site.register(SecondClassification)
admin.site.register(ThirdClassification)
admin.site.register(Supplier)
admin.site.register(Receiver)
admin.site.register(DeliveryRecord)
admin.site.register(FuelPlan)
admin.site.register(CardRecord)
admin.site.register(AbnormalRecord)
admin.site.register(GoodsInventory, GoodsInventoryAdmin)
