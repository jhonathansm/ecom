from autoslug import AutoSlugField
from django.db import models
from django.db.models import Q
from django.urls import reverse
from model_utils.models import TimeStampedModel


class ProductQuerySet(models.query.QuerySet):
    
    # def active(self):
    #     return self.filter(active = True)

    # def featured(self):
    #     return self.filter(featured = True, active = True)

    def search(self, query):
        lookups = (Q(description = query) | 
                        Q(description__contains = query) | 
                        Q(price__contains = query))
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    
    def get_queryset(self):
        return ProductQuerySet(self.model, using = self._db)
    
    # def all(self):
    #     return self.get_queryset().active()

    def featured(self):
        #self.get_queryset().filter(featured = True)
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id = id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().search(query)

class AvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)


class Category(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(unique=True, always_update=False, populate_from="name")

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:list_by_category", kwargs={"slug": self.slug})


class Product(TimeStampedModel):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    slug = AutoSlugField(unique=True, always_update=False, populate_from="name")
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    objects = ProductManager()
    available = AvailableManager()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})

