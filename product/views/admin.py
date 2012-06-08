from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms.models import modelformset_factory
from product.forms import ProductGroupForm, ChildProductForm, ProductImageForm, ProductForm, CategoryForm, BrandForm, OptionGroupForm
from product.models import Product, Option, ProductImage, ProductGroup, OptionGroup
from empor.shortcuts import JSONResponse

def index(request):
    return render('something')

def create_group(request):
    form = ProductGroupForm(request.POST or None)
    if form.is_valid():
        group = form.save()
        return redirect('product-admin-create-product', group_id=group.id)

    return render(request, 'admin/create-group.html', {'form' : form}) 

def create_product(request, group_id):
    group = ProductGroup.objects.get(id=group_id)
    products = group.products.filter(parent=None)
    product_form = ProductForm(request.POST or None)
    ChildProductFormSet = modelformset_factory(Product, form=ChildProductForm)
    child_formset = ChildProductFormSet(request.POST or None, prefix='child', queryset=Product.objects.none())
    if product_form.is_valid():
        product = product_form.save(commit=False)
        product.product_group = group
        product.category = group.category
        product.brand = group.brand
        product.save()
        if product.has_options:
            children = child_formset.save(commit=False)
            for (counter, child) in enumerate(children):
                child.parent = product
                child.name = product.name
                child.description = product.description
                child.brand = product.brand
                child.category = product.category
                child.has_options = True
                child.save()
                child.option_set.add(Option.objects.get(id=child_formset[counter].cleaned_data['option']))
                child.optiongroup_set.add(OptionGroup.objects.get(id=child_formset[counter].cleaned_data['option_group']))
        return HttpResponse('done')

    return render(request, 'admin/create-product.html', {
        'group': group,
        'products': products,
        'product_form': product_form,
        'child_formset': child_formset,
    })

def _render_options(request, group_id):
    if request.is_ajax():
        choices = []
        for option in Option.objects.filter(option_group=group_id):
            choice = {'id': option.id, 'name': unicode(option.name)}
            choices.append(choice)
        
        return JSONResponse(choices)

def _create_brand(request):
    form = BrandForm(request.POST, request.FILES or None)
    if form.is_valid():
        brand = form.save()
        return JSONResponse({'id': brand.id, 'name': brand.name})
    return render(request, 'admin/create-form.html', {'form': form})

def _create_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        cat = form.save()
        return JSONResponse({'id': cat.id, 'name': cat.name})
    return render(request, 'admin/create-form.html', {'form': form})

def _create_optiongroup(request):
    form = OptionGroupForm(request.POST or None)
    if form.is_valid():
        opt = form.save()
        return JSONResponse({'id': opt.id, 'name': opt.name})
