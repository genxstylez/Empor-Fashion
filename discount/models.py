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
    amount = models.PositiveIntegerField(_('Amount'), default=0)
    percentage = models.PositiveIntegerField(_('Percentage'), default=0)
    
    def __unicode__(self):
        return self.name

    def get_value(self):
        if self.percentage:
            return self.percentage/float(100)
        else:
            return int(self.amount)

    def save(self):
        if self.allowUses > 0 and self.numUses == self.allowUses:
            self.active = False
        super(Discount, self).save()
    

class Voucher(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    code = models.CharField(_('Code'), max_length=20)
    active = models.BooleanField(_('Active'), default=True)
    start_date = models.DateTimeField(_('Start Date'), auto_now_add=True)
    end_date = models.DateTimeField(_('End Date'), auto_now=True)
    allowUses = models.IntegerField(_('Number of allowed uses'), default=0)
    numUses = models.IntegerField(_('Number of times already used'), default=0)
    amount = models.PositiveIntegerField(_('Amount'), default=0)
    percentage = models.PositiveIntegerField(_('Percentage'), default=0)
    
    def __unicode__(self):
        return self.name

    def get_value(self):
        if self.percentage:
            return self.percentage/float(100)
        else:
            return int(self.amount)
            
    def get_display_value(self):
        if self.percentage:
            return '- %s%%' % self.percentage
        else:
            return '- NT$%s' % int(self.amount)

    def save(self):
        if self.allowUses > 0 and self.numUses == self.allowUses:
            self.active = False
        super(Voucher, self).save()

