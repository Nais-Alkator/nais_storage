from django.contrib import admin
from django.urls import path, include, path
from django.conf import settings
from nais_storage.views import view_main_page
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view_main_page, name="main"),
    path('order_details/', include("nais_storage.urls")),
    path('account/', include('account.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns