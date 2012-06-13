from django import forms
from django.utils.translation import ugettext as _
from product.models import Collection, Product, OptionGroup, ProductImage, Brand, Category

OPTION_CHOICES = [(0, '-----'),]
OPTION_CHOICES += [(option.id, option.name) for option in OptionGroup.objects.all()]

class ChildProductForm(forms.ModelForm):
    option_group = forms.ChoiceField(label=_('Option Group'), choices=OPTION_CHOICES, widget=forms.Select(attrs={'class':'optiongroup'}))
    stock = forms.CharField(label=_('Stock'))
    option = forms.ChoiceField(label=_('Option'), choices=[(0, '------')], widget=forms.Select(attrs={'class': 'options'}))
     
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

class CollectionForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-xxxlarge'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'input-xxxlarge', 'row': '5'}))

    class Meta:
        model = Collection 
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
