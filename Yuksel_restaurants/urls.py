
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
import home
from home import views 

urlpatterns = [
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('product/', include('product.urls')),

    path('jet/', include('jet.urls')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),

    path('category/<int:id>/<slug:slug>', views.category_products, name='category_products'),

    path(('about/'), views.aboutus, name='aboutus'),
    path(('contact/'), views.contactus, name='contactus'),
    path('search/', views.search, name='search'),
    path('search_auto/', views.search_auto, name='search_auto'),

    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('category/<int:id>/<slug:slug>', views.category_products, name='category_products'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
