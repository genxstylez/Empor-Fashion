from django.shortcuts import render,redirect
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import HttpResponse
from django.forms.models import formset_factory
from product.forms import CollectionForm, ChildProductForm, ProductForm, CategoryForm, BrandForm, OptionGroupForm, ProductImageForm, ProductThumbForm
from product.models import Product, Option, ProductImage, Collection, OptionGroup, ProductThumb
from empor.shortcuts import JsonResponse
from empor.thumbs import thumb_resize, generate_crop

def index(request):
    collections = Collection.objects.all()
    return render(request, 'product/admin/index.html', {'collections': collections})

def create_group(request):
    form = CollectionForm(request.POST or None)
    if form.is_valid():
        collection = form.save()
        if 'add' in request.POST:
            return redirect('product-admin-create-product', group_id=collection.id)
        else:
            return redirect(index)

    return render(request, 'product/admin/create-collection.html', {'form' : form}) 

def create_product(request, group_id):
    collection = Collection.objects.get(id=group_id)
    products = collection.products.filter(parent=None)
    ChildProductFormSet = formset_factory(ChildProductForm)
    ProductImageFormSet= formset_factory(ProductImageForm)
    if request.POST:
        product_form = ProductForm(request.POST)
        thumb_form = ProductThumbForm(request.POST)
        child_formset = ChildProductFormSet(request.POST, prefix='child')
        product_image_formset = ProductImageFormSet(request.POST, prefix='product_image')
        if product_form.is_valid() and product_image_formset.is_valid() and thumb_form.is_valid()\
            or product_form.data.has_key('has_options') and child_formset.is_valid() \
            and product_image_formset.is_valid() and product_form.is_valid() and thumb_form.is_valid():

            product = product_form.save(commit=False)
            product.collection = collection 
            product.category = collection.category
            product.brand = collection.brand
            product.save()
            product.option_group.add(OptionGroup.objects.get(id=product_form.cleaned_data['option_group']))

            thumb = ProductThumb.objects.get(id=thumb_form.cleaned_data['id'])
            x1 = thumb_form.cleaned_data['x1']
            y1 = thumb_form.cleaned_data['y1']
            x2 = thumb_form.cleaned_data['x2']
            y2 = thumb_form.cleaned_data['y2']
            thumb_file = generate_crop(thumb.original.file, thumb.original.name.split('.')[1], int(x1), int(y1), int(x2), int(y2))

            thumb.thumb.save(thumb_file[0], thumb_file[1], save=False)
            thumb.product = product
            thumb.x1 = x1
            thumb.y1 = y1
            thumb.x2 = x2
            thumb.y2 = y2
            thumb.save()

            for form in product_image_formset:
                image = ProductImage.objects.get(id=form.cleaned_data['id'])
                image.product = product
                image.main = True if form.cleaned_data['main'] else False
                image.save()

            if product.has_options:
                for (counter, form) in enumerate(child_formset.forms):
                    if form.is_valid():
                        child = Product()
                        child.stock = form.cleaned_data['stock']
                        child.price = form.cleaned_data['price'] if form.cleaned_data['price'] else product.price
                        child.parent = product
                        child.name = product.name
                        child.description = product.description
                        child.brand = product.brand
                        child.category = product.category
                        child.has_options = True
                        child.collection = collection
                        child.save()
                        child.gender.add = product.gender
                        child.options.add(Option.objects.get(id=child_formset[counter].cleaned_data['option']))
                        child.option_group.add(OptionGroup.objects.get(id=product_form.cleaned_data['option_group']))
            return HttpResponse('done')
    else:
        product_form = ProductForm()
        thumb_form = ProductThumbForm()
        child_formset = ChildProductFormSet(prefix='child')
        product_image_formset = ProductImageFormSet(prefix='product_image')

    return render(request, 'product/admin/create-product.html', {
        'collection': collection,
        'products': products,
        'thumb_form': thumb_form,
        'product_form': product_form,
        'child_formset': child_formset,
        'product_image_formset': product_image_formset
    })

def _render_options(request, group_id):
    if request.is_ajax():
        choices = []
        for option in Option.objects.filter(option_group=group_id):
            choice = {'id': option.id, 'name': unicode(option.name)}
            choices.append(choice)
        
        return JsonResponse(choices)

def _create_brand(request):
    form = BrandForm(request.POST, request.FILES or None)
    if form.is_valid():
        brand = form.save()
        return JsonResponse({'id': brand.id, 'name': brand.name})
    return render(request, 'admin/create-form.html', {'form': form})

def _create_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        cat = form.save()
        return JsonResponse({'id': cat.id, 'name': cat.name})
    return render(request, 'admin/create-form.html', {'form': form})

def _create_optiongroup(request):
    form = OptionGroupForm(request.POST or None)
    if form.is_valid():
        opt = form.save()
        return JsonResponse({'id': opt.id, 'name': opt.name})

def _upload(request):
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
        image = ProductImage()
        image.image.save(name, image_file, save=False)
        image.save()

    return JsonResponse({'success': True, 'file_id': image.id, 'file': image.image.url })

def _thumb_upload(request):
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
        image = ProductThumb()
        image.original.save(t[0], t[1], save=False)
        image.save()

    return JsonResponse({'success': True, 'file_id': image.id, 'file': image.original.url })
