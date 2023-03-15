from django.db import models


class CategoryFeature(models.Model):

    category = models.ForeignKey("mainapp.Category", verbose_name='Категорія', on_delete=models.CASCADE)
    feature_name = models.CharField(verbose_name="Ім'я ключа категорії", max_length=50)
    feature_filter_name = models.CharField(verbose_name="Ім'я для фільтру", max_length=50)
    unit = models.CharField(max_length=50, verbose_name='Одиниця виміру', null=True, blank=True)

    class Meta:
        unique_together = ('category', 'feature_name', 'feature_filter_name')

    def __str__(self):
        return f"{self.category.name} | {self.feature_name}"


class FeatureValidator(models.Model):

    category = models.ForeignKey("mainapp.Category", verbose_name='Категорія', on_delete=models.CASCADE)
    feature_key = models.ForeignKey(CategoryFeature, verbose_name='Ключ характеристики', on_delete=models.CASCADE)
    valid_feature_value = models.CharField(max_length=100, verbose_name='Валідне значення')

    def __str__(self):
        return f"Категорія {self.category.name} | " \
               f"Характристика {self.feature_key.feature_name} | " \
               f"Валідне значення {self.valid_feature_value}"


class ProductFeatures(models.Model):

    product = models.ForeignKey("mainapp.Product", verbose_name='Товар', on_delete=models.CASCADE)
    feature = models.ForeignKey(CategoryFeature, verbose_name='Характеристика', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name='Значення')

    def __str__(self):
        return f"Товар - {self.product.title} | " \
               f"Характеристика - {self.feature.feature_name} | " \
               f"Значення - {self.value}"
