#coding : utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Discount(models.Model):
	name = models.CharField(_('Name'), max_length=100)
	active = models.BooleanField(_('Active'), default=True)
	start_date = models.DateTimeField(_('Start Date'), auto_now_add=True)
	end_date = models.DateTimeField(_('End Date'), auto_now=True)
	allowUses = models.IntegerField(_('Number of allowed uses'), default=0)
	numUses = models.IntegerField(_('Number of times already used'), default=0)
	amount = models.PositiveIntegerField(_('Amount'), null=True, blank=True)
	percentage = models.DecimalField(_('Percentage'), decimal_places=2, max_digits=5, null=True, blank=True)
    
	def __unicode__(self):
		return self.name

	def get_value(self):
		if self.percentage:
			return self.percentage/100
		else:
			return int(self.amount)

	def save(self):
		if self.allowUses > 0 and self.numUses == self.allowUses:
			self.active = False
		else:
			self.active = True
		if not self.active:
			for product in self.products.all():
				product.discountable = False
				product.save()
		super(Discount, self).save()

class Voucher(models.Model):
	name = models.CharField(_('Name'), max_length=100)
	code = models.CharField(_('Code'), max_length=20)
	active = models.BooleanField(_('Active'), default=True)
	start_date = models.DateTimeField(_('Start Date'), auto_now_add=True)
	end_date = models.DateTimeField(_('End Date'), auto_now=True)
	allowUses = models.IntegerField(_('Number of allowed uses'), default=0)
	numUses = models.IntegerField(_('Number of times already used'), default=0)
	amount = models.PositiveIntegerField(_('Amount'), null=True, blank=True)
	percentage = models.DecimalField(_('Percentage'), decimal_places=2, max_digits=5, null=True, blank=True)
    
	def __unicode__(self):
		return self.name

	def get_value(self):
		if self.percentage:
			return self.percentage/100
		else:
			return int(self.amount)

	def save(self):
		if self.allowUses > 0 and self.numUses == self.allowUses:
			self.active = False
		else:
			self.active = True
		super(Voucher, self).save()

