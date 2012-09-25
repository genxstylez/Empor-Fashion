# -*- coding: utf-8 -*-
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render,redirect, get_object_or_404
from django.core.files.base import ContentFile
from django.conf import settings
from django.views.decorators.http import require_POST
from django.forms.models import modelformset_factory
from product.forms import CollectionForm, ChildProductForm, ProductForm, CategoryForm, BrandForm, OptionGroupForm
from product.models import Product, Option, ProductImage, Collection, ProductThumb
from empor.shortcuts import JsonResponse
from empor.thumbs import thumb_resize, generate_crop

@staff_member_required
def index(request):
    collections = Collection.objects.all()
    return render(request, 'staff/index.html', {'collections': collections})

@staff_member_required
def collection(request, collection_id):   
    collection = get_object_or_404(Collection, id=collection_id)
    products = collection.products.filter(parent=None)
    return render(request, 'staff/collection.html', {'collection': collection, 'products': products})

@staff_member_required
def collection_create(request):
    form = CollectionForm(request.POST or None)
    if form.is_valid():
        collection = form.save()
        if 'add' in request.POST:
            return redirect('staff-create-product', collection_id=collection.id)
        else:
            return redirect(index)

    return render(request, 'staff/create-collection.html', {'form' : form}) 

@staff_member_required
def product_create(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    ChildProductFormSet = modelformset_factory(Product, form=ChildProductForm)
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        child_formset = ChildProductFormSet(request.POST, prefix='child')
        if product_form.data.has_key('has_options'):
            if child_formset.is_valid() and product_form.is_valid():
                check = True
            else:
                check = False
        else:
            if product_form.is_valid():
                check = True
            else:
                check = False
        if check:
            product = product_form.save(commit=False)
            product.collection = collection 
            product.category = collection.category
            product.brand = collection.brand
            product.save()
            product_form.save_m2m()

            if product.has_options:
                for (counter, form) in enumerate(child_formset.forms):
                    child = form.save(commit=False) 
                    child.parent = product
                    child.name = product.name
                    child.description = product.description
                    child.brand = product.brand
                    child.category = product.category
                    child.has_options = True
                    child.option_group = product.option_group
                    if not child.price:
                        child.price = product.price
                    child.collection = collection
                    child.save()
                    for gender in product.gender.all():
                        child.gender.add(gender)
            if 'add' in request.POST:   
                return redirect('staff-product-image', product.id)
            else:
                return redirect('staff-collection', collection_id=collection_id)
    else:
        product_form = ProductForm()
        child_formset = ChildProductFormSet(prefix='child', queryset=Product.objects.none())

    return render(request, 'staff/create-product.html', {
        'collection': collection,
        'product_form': product_form,
        'child_formset': child_formset,
    })

@staff_member_required
def product_edit(request, collection_id, product_id):
    product = get_object_or_404(Product, id=product_id)
    collection = Collection.objects.get(id=collection_id)
    children = Product.objects.filter(parent=product)
    ChildProductFormSet = modelformset_factory(Product, form=ChildProductForm, extra=0)

    product_form = ProductForm(request.POST or None, instance=product)
    child_formset = ChildProductFormSet(request.POST or None, prefix='child', queryset=children)
    if product_form.data.has_key('has_options'):
        if child_formset.is_valid() and product_form.is_valid():
            check = True
        else:
            check = False
    else:
        if product_form.is_valid():
            check = True
        else:
            check = False

    if check:
        product = product_form.save()

        if product.has_options:
            for (counter, form) in enumerate(child_formset.forms):
                child = form.save(commit=False)
                child.parent = product
                child.option_group = product.option_group
                child.description = product.description
                child.brand = product.brand
                child.category = product.category
                child.has_options = True
                child.option_group = product.option_group
                if not child.price:
                    child.price = product.price
                child.collection = collection
                child.save()
                child.gender.clear()
                for gender in product.gender.all():
                    child.gender.add(gender)

        if 'add' in request.POST:   
            return redirect('staff-product-image', product.id)
        else:
            return redirect('staff-collection', collection_id)


    return render(request, 'staff/edit-product.html', {
        'collection': collection,
        'product_form': product_form,
        'child_formset': child_formset,
    })

@staff_member_required
def product_image(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = ProductImage.objects.filter(product=product)
    if request.method == 'POST':
        image_id = request.POST.get('main', '')
        image = ProductImage.objects.get(id=image_id)
        image.main = True
        image.save()

        if 'add' in request.POST:   
            return redirect('staff-product-thumb', product.id)
        else:
            return redirect('staff-collection', product.collection.id)

    return render(request, 'staff/product-image.html', {'product': product, 'images': images})

@staff_member_required
def product_thumb(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        thumb = ProductThumb.objects.get(product=product)
    except ProductThumb.DoesNotExist:
        thumb = None
    if request.method == 'POST':
        x1 = request.POST.get('x1', 0)
        y1 = request.POST.get('y1', 0)
        x2 = request.POST.get('x2', 0)
        y2 = request.POST.get('y2', 0)
        thumb_file = generate_crop(thumb.original.file, thumb.original.name.split('.')[1], int(x1), int(y1), int(x2), int(y2))
        thumb.thumb.save(thumb_file[0], thumb_file[1], save=False)
        thumb.x1 = x1
        thumb.y1 = y1
        thumb.x2 = x2
        thumb.y2 = y2
        thumb.save()
        return redirect('staff-collection', product.collection.id)

    return render(request, 'staff/product-thumb.html', {'product': product, 'thumb': thumb})

@staff_member_required
def _render_options(request, group_id):
    if request.is_ajax():
        choices = []
        for option in Option.objects.filter(option_group=group_id):
            choice = {'id': option.id, 'name': unicode(option.name)}
            choices.append(choice)
        
        return JsonResponse(choices)

@staff_member_required
def _create_brand(request):
    form = BrandForm(request.POST, request.FILES or None)
    if form.is_valid():
        brand = form.save()
        return JsonResponse({'id': brand.id, 'name': brand.name})
    return render(request, 'staff/create-form.html', {'form': form})

@staff_member_required
def _create_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        cat = form.save()
        return JsonResponse({'id': cat.id, 'name': cat.name})
    return render(request, 'staff/create-form.html', {'form': form})

@staff_member_required
def _create_optiongroup(request):
    form = OptionGroupForm(request.POST or None)
    if form.is_valid():
        opt = form.save()
        return JsonResponse({'id': opt.id, 'name': opt.name})


@staff_member_required
@require_POST
def _upload(request):
    product_id = request.POST.get('product_id', None)
    product = get_object_or_404(Product, id=product_id)
    uploaded_file = request.FILES.get('file', None)
    chunk = request.POST.get('chunk', '0')
    chunks = request.POST.get('chunks', '0')
    name = request.POST.get('name', '')
    if not name :
        name = uploaded_file.name
    if uploaded_file:
        filepath = '%s/%s' % (settings.FILE_UPLOAD_TEMP_DIR, name)
        with open(filepath, ('wb' if chunk == '0' else 'ab')) as f:
            for content in uploaded_file.chunks():
                f.write(content)
    if int(chunk) + 1 >= int(chunks):
        f = open(filepath)
        image_file = ContentFile(f.read())
        f.close()
        image = ProductImage()
        image.product = product
        image.image.save(name, image_file, save=False)
        image.save()

        return JsonResponse({'success': True, 'image_id': image.id, 'image_url': image.image['small'].url })
    return JsonResponse({'success': True})

@staff_member_required
@require_POST
def _thumb_upload(request):
    product_id = request.POST.get('product_id', None)
    product = get_object_or_404(Product, id=product_id)
    uploaded_file = request.FILES.get('file', None)
    chunk = request.REQUEST.get('chunk', '0')
    chunks = request.REQUEST.get('chunks', '0')
    name = request.REQUEST.get('name', '')
    if not name :
        name = uploaded_file.name
    if uploaded_file:
        filepath = '%s/%s' % (settings.FILE_UPLOAD_TEMP_DIR, name)
        with open(filepath, ('wb' if chunk == '0' else 'ab')) as f:
            for content in uploaded_file.chunks():
                f.write(content)
    if int(chunk) + 1 >= int(chunks):
        f = open(filepath)
        image_file = ContentFile(f.read())
        f.close()

        t = thumb_resize(image_file, name.split('.')[1], 420)

        try:
            thumb = ProductThumb.objects.get(product=product)
            thumb.delete()
        except ProductThumb.DoesNotExist:
            pass

        image = ProductThumb()
        image.product = product
        image.original.save(t[0], t[1], save=False)
        image.save()

    return JsonResponse({'success': True, 'image_id': image.id, 'image_url': image.original.url })
