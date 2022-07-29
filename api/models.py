from django.db import models


class User(models.Model):
		name = models.CharField(max_length=128, blank=False, verbose_name='name')


class Shop(models.Model):
		name = models.CharField(max_length=128, blank=False, verbose_name='name')


class Receipt(models.Model):
		user = models.CharField(max_length=128, blank=False, verbose_name='name')
		check_number = models.PositiveIntegerField(blank=False, verbose_name='check number')
		shop = models.CharField(max_length=128, blank=False, verbose_name='shop')
		date_of_issue = models.DateTimeField(blank=False)
		total_sum = models.PositiveIntegerField(blank=False, verbose_name='total sum')


class Product(models.Model):
		name = models.CharField(max_length=128, blank=False, verbose_name='name')
		receipt = models.ForeignKey(Receipt, on_delete=models.PROTECT, blank=False, related_name='product')
		count = models.PositiveIntegerField(blank=False, verbose_name='count')
		price = models.PositiveIntegerField(blank=False, verbose_name='price')
		product_sum = models.PositiveIntegerField(blank=True, verbose_name='product sum')
		
		def save(self, *args, **kwargs):
				product_sum = self.product_sum
				if product_sum:
						super(Product, self).save(*args, **kwargs)
				self.product_sum = self.count * self.price
				super(Product, self).save(*args, **kwargs)
