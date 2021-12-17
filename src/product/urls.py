from django.urls import path
from django.views.generic import TemplateView

from product.views.product import CreateProductView,LoadList,EditProduct
from product.views.variant import VariantView, VariantCreateView, VariantEditView
from product.views.api import CreateProductApi

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('list/', LoadList, name='list.product'),
    path('product',CreateProductApi,name='product'),
    path('eidt_product/<str:pk>/',EditProduct,name='edit_product'),
]
