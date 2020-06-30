from django.db import models
from django.utils.text import slugify
from django.urls import reverse


def upload_location(instance, filename, *args, **kwargs):
    file_path = 'image/{cat}/{name}-{filename}'.format(cat=str(instance.category), name=str(instance.name), filename=filename
        )
    return file_path


class Category(models.Model):
    name    = models.CharField(max_length=200, db_index=True)
    slug    = models.SlugField(max_length=200, unique=True)


    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):

    category    = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name        = models.CharField(max_length=200, db_index=True)
    slug        = models.SlugField(max_length=200, db_index=True)
    image       = models.ImageField(upload_to=upload_location,max_length=200, db_index=True)
    price      = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    available   = models.BooleanField(default=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)



    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])
