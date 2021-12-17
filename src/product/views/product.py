from django.views import generic

from product.models import *
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.db import models
from .product_form import *
from django.utils.datastructures import MultiValueDictKeyError


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        print("#################################")
        return context

def LoadList(request):
    products=Product.objects.all()
    number=products.count()
    p_nator=Paginator(products,2)
    page=request.GET.get("page")
    vanues=p_nator.get_page(page)
    
    if request.method=="POST":
        filtered=products.filter(title=request.POST.get('title'))
        filtered=list(filtered)
        v=None
        if request.POST.get('variant'):
            v=Variant.objects.get(title=request.POST.get('variant'))
        
            v=list(v.productvariant_set.all())
            for i in v:
                filtered.append(i.product)
        
        price_from=request.POST.get('price_from')
        price_to=request.POST.get('price_to')
        try:
            
            if price_from!="" and price_to!="":
                price_from=float(price_from)
                price_to=float(price_to)
                p=ProductVariantPrice.objects.filter(price__range=(price_from,price_to))
                for i in p:
                    filtered.append(i.product)
            
        except:
            pass
        try:
            date=request.POST.get('date')
            d=products.filter(date_created=date)
            filtered=filtered+list(d)
        except:
            pass
        filtered=set(filtered)
        filtered=list(filtered)
        p_nator=Paginator(filtered,2)
        vanues=p_nator.get_page(page)
        url=request.get_full_path()
        context={
        'vanues':vanues,
        'number':number,
        'variants':Variant.objects.all(),
        }
        
    context={
        'vanues':vanues,
        'number':number,
        'variants':Variant.objects.all(),
    }
    return render(request,'products/list.html',context)

def EditProduct(request,pk):
    product=Product.objects.get(id=pk)
    variant=list(Variant.objects.filter(active=True))
    product_variant=list(product.productvariant_set.all())
    #print(product_variant)
    product_variant_price=list(product.productvariantprice_set.all())
    current_variants=[]
    p_v=product_variant_price[0]
    if p_v.product_variant_one:
        current_variants.append(p_v.product_variant_one.variant)
    if p_v.product_variant_two:
        current_variants.append(p_v.product_variant_two.variant)
    if p_v.product_variant_three:
        current_variants.append(p_v.product_variant_three.variant)
    current_product_variant={}
    not_variant=[]
    for i in variant:
        if i in current_variants:
            pass
        else:
            not_variant.append(i)
    context={
        'product':product,
        'variant':variant,
        'product_variant':product_variant,
        'product_variant_price':product_variant_price,
        'product_image':(list(product.productimage_set.all()))[-1],
        'current_variants':[],
        'not_variant':not_variant,
    }
    for i in current_variants:
        context[i.title]=product.productvariant_set.filter(variant=i)
        print("........................")
        s=''
        for j in context[i.title]:
            s=s+j.variant_title.split('/')[0]+','
        context['current_variants'].append({'var':i,'tag':s})
    if request.method=='POST':
        data=request.POST
        product.title=data['product_name']
        product.sku=data['product_sku']
        product.description=data['descriptions']
        im=(list(product.productimage_set.all()))[-1]
        filepath=''
        try:
            filepath = request.FILES['product_image']
        except MultiValueDictKeyError:
            filepath = False
        
        if filepath:
            im.file_path=filepath
            im.save()
        product.save()
        p=data.getlist('price')
        s=data.getlist('stock')
        #stock=request.POST['stock']
        #print("-----------")
        #print(p)
        j=0
        for i in product_variant_price:
            
            i.price=p[j]
            i.stock=s[j]
            i.save()
            j=j+1
        return redirect('product:list.product')

            
    return render(request,'products/edit.html',context)