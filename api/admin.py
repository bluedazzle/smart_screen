from django.contrib import admin
from api.models import *


# Register your models here.

class GoodsInventoryAdmin(admin.ModelAdmin):
    search_fields = ['barcode']


class GoodsAdmin(admin.ModelAdmin):
    search_fields = ['belong__id']


admin.site.register(FuelOrder, GoodsAdmin)
admin.site.register(FuelTank)
admin.site.register(Site)
admin.site.register(GoodsOrder, GoodsAdmin)
admin.site.register(InventoryRecord)
admin.site.register(Classification)
admin.site.register(SecondClassification)
admin.site.register(ThirdClassification)
admin.site.register(Supplier)
admin.site.register(Receiver)
admin.site.register(DeliveryRecord)
admin.site.register(FuelPlan)
admin.site.register(CardRecord, GoodsAdmin)
admin.site.register(AbnormalRecord, GoodsAdmin)
admin.site.register(GoodsInventory, GoodsInventoryAdmin)
