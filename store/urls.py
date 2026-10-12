from codecs import lookup
import collections

from django.db import router
from django.urls import path
from . import views
from rest_framework_nested import routers

router =routers.DefaultRouter()
#parent
router.register('products',views.ProductViewSet , basename='products')
router.register('collections',views.CollectionViewSet)
router.register('carts' , views.CartViewSet)
router.register('customers' , views.CustomerViewSet)
#children 
products_router = routers.NestedDefaultRouter(router,'products' , lookup ='product')
products_router.register('reviews',views.ReviewViewSet , basename='product-review')
carts_router = routers.NestedDefaultRouter(router , 'carts' , lookup = 'cart')
carts_router.register('items' ,views.CartItemViewSet,basename='cart-items' )
#collections_router = routers.NestedDefaultRouter(router , 'collections' , lookup = 'collection')
#collections_router.register('reviews',views.ReviewViewSet , basename='collection-review')
urlpatterns = router.urls + products_router.urls + carts_router.urls #+ collections_router.urls

# URLConf
# urlpatterns = [
#     # path('products/' , views.ProductList.as_view()),
#     # path('products/<int:pk>', views.ProductDetail.as_view()) ,
#     # path('collections/', views.CollectionList.as_view()) ,
#     # path('collections/<int:pk>', views.collection_detail, name = 'collection-detail')
# ]
