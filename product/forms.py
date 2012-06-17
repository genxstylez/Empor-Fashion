from django import forms
from django.utils.translation import ugettext as _
from product.models import Collection, Product, OptionGroup, ProductImage, Brand, Category, Option

OPTIONGROUP_CHOICES = [(0, '-----'),]
OPTIONGROUP_CHOICES += [(option.id, option.name) for option in OptionGroup.objects.all()]

OPTION_CHOICES = [(0, '-----'),]
OPTION_CHOICES += [(option.id, option.name) for option in Option.objects.all()]

class ChildProductForm(forms.Form):
    option = forms.ChoiceField(label=_('Option'), choices=OPTION_CHOICES, widget=forms.Select(attrs={'class': 'options', 'disabled': 'disabled'}))
    stock = forms.CharField(label=_('Stock'), widget=forms.TextInput(attrs={'class':'input-mini', 'placeholder': _('qty')}))
    price = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'input-mini', 'placeholder': 'NT $'}))
     
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage

class ProductForm(forms.ModelForm):
    option_group = forms.ChoiceField(label=_('Option Group'), choices=OPTIONGROUP_CHOICES, 
        required=False, widget=forms.Select(attrs={'class':'optiongroup'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'input-large', 'row': '10'}))

    class Meta:
        model = Product
        exclude = ('collection', 'parent', 'brand', 'category', 'thumbnail', 'gender', 'featured')
        fields = ('name', 'price', 'composition', 'description', 'has_options', 'option_group')

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
