
from siterestaurant import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.views.defaults import page_not_found
# from restaurant import views, converters
from restaurant import converters
from django.urls import path, include, register_converter

register_converter(converters.FourDigitYearConverter, "year4")

handler404 = page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurant/', include('restaurant.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Панель администрирования"
