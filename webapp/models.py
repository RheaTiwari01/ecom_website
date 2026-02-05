from django.db import models

# Create your models here.
#Category
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#Product
class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    def __str__(self):
        return self.title
#Store
class Store(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name
#Inventory
class Inventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        
        unique_together = ('store', 'product')

    def __str__(self):
        return f"{self.store} - {self.product}"
#Order 
class Order(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('REJECTED', 'Rejected'),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity_requested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.order.id} - {self.product}"