from django.urls import path
from estoreapp import views
from estore import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='home'),
    path('productdetails/<pid>',views.productsdetails),
    path('viewcart',views.cart),
    path('login',views.ulogin),
    path('register',views.uregistartion),
    path('logout/',views.ulogout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
  



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
