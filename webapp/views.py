# webapp/views.py
from django.core.paginator import Paginator
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from .models import Order,Inventory,Product
from django.core.cache import cache
from .tasks import send_order_confirmation


from .serializers import OrderCreateSerializer, OrderGetSerializer,InventorySerializer,ProductSerializer

class OrderCreateAPI(APIView):

    def post(self, request):

        serializer = OrderCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        order = serializer.save()
        cache_key = f"store_orders_{order.store_id}"
        cache.delete(cache_key)
        send_order_confirmation.delay(order.id)


        return Response(
            {
                "order_id": order.id,
                "status": order.status
            },
            status=status.HTTP_201_CREATED
        )
class StoreOrderListAPI(APIView):

    def get(self, request, store_id):
        cache_key = f"store_order_{store_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)
        
        
        orders = (
            Order.objects
            .filter(store_id=store_id)
            .prefetch_related("items")   # avoid N+1
            .order_by("-created_at")     # newest first
        )

        serializer = OrderGetSerializer(orders, many=True)
        data = serializer.data


        cache.set(cache_key, data, timeout=800)

        return Response(serializer.data)
class InventoryAPI(APIView):
    def get(self,request,store_id):
        inventory=(Inventory.objects.filter(store_id=store_id).select_related("product","product__category").order_by("product__title"))
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)
class SmartSearch(APIView):
    def get(self,request):
        search= request.GET.get("q","")
        category = request.GET.get("category")
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        store_id = request.GET.get("store_id")
        in_stock = request.GET.get("in_stock")
        sort = request.GET.get("sort", "relevance")

        page = request.GET.get("page", 1)
        page_size = request.GET.get("page_size", 10)
        products = (Product.objects.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(category__name__icontains=search)))
        if category:
            products = products.filter(category__name__iexact=category)

        
        if min_price:
            products = products.filter(price__gte=min_price)

        if max_price:
            products = products.filter(price__lte=max_price)
        if store_id:

            products = products.filter(
                inventory__store_id=store_id
            )

            if in_stock == "true":
                products = products.filter(
                    inventory__quantity__gt=0
                )
        if sort == "price":
            products = products.order_by("price")

        elif sort == "newest":
            products = products.order_by("-id")

        elif sort=="id":   
            products = products.order_by("-id")


        products = products.distinct()
        paginator = Paginator(products, page_size)
        page_obj = paginator.get_page(page)


       
        serializer = ProductSerializer(page_obj, many=True)

        return Response({

            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number,

            "results": serializer.data
        })
class Autocomplete(APIView):
    def get(self,request):
        query=request.GET.get('q',"").strip()
        prods= Product.objects.all()
        if len(query) < 3:
            return Response([])
        else:
            pref_ans= Product.objects.filter(title__istartswith=query).values_list("title",flat=True)
            gen_ans = Product.objects.filter(
            title__icontains=query
        ).exclude(
            title__istartswith=query
        ).values_list("title", flat=True)

        results = list(pref_ans) + list(gen_ans)

    
        results = results[:10]

        return Response(results)

