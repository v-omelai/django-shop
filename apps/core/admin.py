from django.contrib import admin

from apps.core.models import *


admin.site.register(Item)
admin.site.register(Price)
admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(BuyerInventory)
admin.site.register(SellerInventory)
