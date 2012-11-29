from django import forms
from django.utils.translation import ugettext as _
from product.models import Collection, Product, Brand, Category, OptionGroup

class ChildProductForm(forms.ModelForm):
    stock = forms.IntegerField(widget=forms.TextInput(attrs={'class':'input-mini', 'placeholder': _('qty')}))
    price = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class':'input-mini', 'placeholder': 'NT $'}))
    
    class Meta:
        model = Product
        fields = ('option', 'stock', 'price')

class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'input-large', 'row': '10'}))

    class Meta:
        model = Product
        fields = ('name', 'slug', 'price', 'gender', 'composition', 'description', 'remark', 'has_options', 'option_group', )

    def clean_name(self):
        if not self.cleaned_data['name']:
            raise forms.ValidationError(_('This field is required'))
        return self.cleaned_data['name']

    def clean_price(self):
        if not self.cleaned_data['price']:
            raise forms.ValidationError(_('This field is required'))
        return self.cleaned_data['price']

    def clean_option_group(self):
        if self.cleaned_data['has_options'] and not self.cleaned_data['option_group']:
            raise forms.ValidationError(_('Option Group Required'))
        else:
            return self.cleaned_data['option_group']

class ProductThumbForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())
    url = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'thumb_url'}))
    x1 = forms.CharField(widget=forms.HiddenInput())
    y1 = forms.CharField(widget=forms.HiddenInput())
    x2 = forms.CharField(widget=forms.HiddenInput())
    y2 = forms.CharField(widget=forms.HiddenInput())
    
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
