from django.http import response
from rest_framework import serializers,status
from product.models import *
from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import SessionAuthentication,BaseAuthentication
from rest_framework.permissions import IsAuthenticated
import base64
from django.core.files.base import ContentFile 




class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['title','sku','description']
class VariantSaver(serializers.ModelSerializer):
    class Meta:
        model=ProductVariant
        fields=['variant_title','variant','product']
@api_view(['POST'])
def CreateProductApi(request):
    if request.method=="POST":
        print("########################333")
        #print(request.data)
        data=request.data
        product=Product()
        serializer=CreateProductSerializer(product,{'title':data["title"],'sku':data['sku'],'description':data['description']})
        if serializer.is_valid():
            serializer.save()
        
        for i in data['product_variant']:
            for j in i['tags']:
                c={'variant_title':j+"/",'variant':Variant.objects.get(id=i['option']),'product':list(Product.objects.all())[-1]} 
                product_variant=ProductVariant(variant_title=c['variant_title'],variant=c['variant'],product=c['product'])
                product_variant.save()
        for i in data['product_variant_prices']:
            tags=i['title']
            tags=tags.split("/")
            tags=tags[0:-1]
            product_variant_one=None
            product_variant_two=None
            product_variant_three=None
            for j in range (len(tags)):
                if j==0:
                    product_variant_one=(ProductVariant.objects.filter(variant_title=(tags[j]+'/'),product=Product.objects.last()))[0]
                elif j==1:
                    product_variant_two=(ProductVariant.objects.filter(variant_title=(tags[j]+'/'),product=Product.objects.last()))[0]
                elif j==2:
                    product_variant_three=(ProductVariant.objects.filter(variant_title=(tags[j]+'/'),product=Product.objects.last()))[0]
            ProductVariantPrice(product_variant_one=product_variant_one,product_variant_two=product_variant_two,product_variant_three=product_variant_three,price=i['price'],stock=i['stock'],product=list(Product.objects.all())[-1]).save()
        format,imstring=(data['product_image'][0]).split(';base64,')
        ext=format.split('/')[-1]
        print(ext)
        image=base64.b64decode(imstring)
        name=Product.objects.all()
        id=list(Product.objects.all())
        id=id[-1]
        id=id.id
        image=ContentFile(image,name="image_"+str(id)+'.'+ext)
        im=ProductImage()
        im.file_path=image
        im.product=list(Product.objects.all())[-1]
        im.save()
        #ProductImage(product=list(Product.objects.all())[-1],file_path=f).save()
    return Response("Successs",status=None)