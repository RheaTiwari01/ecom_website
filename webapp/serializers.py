from rest_framework import serializers
from .models import Order, OrderItem, Inventory, Store, Product,Category
from django.db import transaction
from django.db.models import Sum
class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ["product", "quantity_requested"]

class OrderCreateSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["store", "items"]
    def validate(self,data):
        store=data["store"]
        items=data["items"]
        insuff=False
        inven={}
        for it in items:
            prod=it["product"]
            qty=it["quantity_requested"]
            inv = Inventory.objects.filter(
                store=store,
                product=prod
            ).first()
            if not inv:
                insuff=True
                break
            if inv.quantity<qty:
                 insuff=True
                 break
            inven[prod.id]=inv
        data["insuff"]=insuff
        data["inven"]=inven
        return data
    @transaction.atomic 
    def create(self,valid_data):
        items=valid_data.pop("items")
        insuff= valid_data.pop('insuff')
        inven= valid_data.pop('inven')
        if insuff:
            order= Order.objects.create(
                store=valid_data["store"],
                status="REJECTED"
            )
        else:
             order= Order.objects.create(
                store=valid_data["store"],
                status="CONFIRMED"
            )
            
             for it in items:

                prod = it["product"]
                qty = it["quantity_requested"]

                inv = inven[prod.id]
                inv.quantity -= qty
                inv.save()

        for it in items:

            OrderItem.objects.create(
                order=order,
                product=it["product"],
                quantity_requested=it["quantity_requested"]
            )

        return order



class  OrderGetSerializer(serializers.ModelSerializer):
    total_items = serializers.SerializerMethodField()

    class Meta:
        model=Order
        fields=["id","status","created_at","total_items"]
    
    def get_total_items(self, obj):

        return obj.items.aggregate(
            total=Sum("quantity_requested")
        )["total"] or 0
    

class CategoryNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["name"]

class ProductSerializer(serializers.ModelSerializer):
    
    category = CategoryNameSerializer()
   
    class Meta:
        model=Product
        fields=["title","price","category"]
    
class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model=Inventory
        fields=["product","quantity"]