from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from apps.core.models import *


class PriceAdmin(admin.ModelAdmin):
    def get_deleted_objects(self, objs, request):
        deleted_objects, model_count, perms_needed, protected = super().get_deleted_objects(objs, request)
        items = 0
        for obj in objs:
            if obj.item:
                link = reverse(
                    f'admin:{obj.item._meta.app_label}_{obj.item._meta.model_name}_change',  # noqa
                    args=[obj.item.pk]
                )
                html = mark_safe(f'Item: <a href="{link}">{obj.item}</a>')
                items += 1
                deleted_objects.append(html)
        model_count['items'] = items
        return deleted_objects, model_count, perms_needed, protected


class SellerAdmin(admin.ModelAdmin):
    def get_deleted_objects(self, objs, request):
        deleted_objects, model_count, perms_needed, protected = super().get_deleted_objects(objs, request)
        buyers = 0
        buyer_inventories = 0
        for obj in objs:
            if obj.buyer:
                link = reverse(
                    f'admin:{obj.buyer._meta.app_label}_{obj.buyer._meta.model_name}_change',  # noqa
                    args=[obj.buyer.pk]
                )
                html = mark_safe(f'Buyer: <a href="{link}">{obj.buyer}</a>')
                buyers += 1
                if obj.buyer.inventory:
                    buyer_inventories += obj.buyer.inventory.count()
                deleted_objects.append(html)
        model_count['buyers'] = buyers
        model_count['buyer inventories'] = buyer_inventories
        return deleted_objects, model_count, perms_needed, protected


admin.site.register(Item)
admin.site.register(Price, PriceAdmin)
admin.site.register(Buyer)
admin.site.register(Seller, SellerAdmin)
admin.site.register(BuyerInventory)
admin.site.register(SellerInventory)
admin.site.register(Goal)
