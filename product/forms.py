from django import forms
from django.utils.translation import ugettext as _
from product.models import ProductGroup, Product, OptionGroup, ProductImage, Brand, Category, Option

OPTION_CHOICES = [(0, '-----'),]
OPTION_CHOICES += [(option.id, option.name) for option in OptionGroup.objects.all()]
SUB_OPTION_CHOICES = [(0, '-----'),]
SUB_OPTION_CHOICES += [(option.id, option.name) for option in Option.objects.all()]

class ChildProductForm(forms.ModelForm):
    option_group = forms.ChoiceField(label=_('Option Group'), choices=OPTION_CHOICES)
    stock = forms.CharField(label=_('Stock'))
    option = forms.ChoiceField(label=_('Option'), choices=SUB_OPTION_CHOICES)
     
    class Meta:
        model = Product
        exclude = ('sold','parent', 'brand', 'category', 'has_options', 'name', 'description', 'product_group', 'thumbnail')

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('product_group', 'parent', 'brand', 'category')

class ProductGroupForm(forms.ModelForm):
    class Meta:
        model = ProductGroup
        exclude = ('stock', 'sold')

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category

class OptionGroupForm(forms.ModelForm):
    class Meta:
        model = OptionGroup
