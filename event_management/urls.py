from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.conf import settings

from core.views import home_event_data, no_permission
from events.views import organizer_dashboard  

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Home Page (core/views.py -> home_event_data)
    path('', home_event_data, name='home'),

    # ✅ Include app urls
    path('events/', include('events.urls')),
    path('users/', include('users.urls')),

    # ✅ Permission Page
    path('no-permission/', no_permission, name='no-permission'),
] + debug_toolbar_urls()

# ✅ Media & Static setup
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# from django.contrib import admin
# from core.views import views
# from django.urls import path,include
# from debug_toolbar.toolbar import debug_toolbar_urls
# from events.views import organizer_dashboard
# from core.views import home_event_data,no_permission
# from django.conf.urls.static import static
# from django.conf import settings

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('',home,name='home'),
#     path('', views.home_event_data, name='home_event_data'),
#     path('events/',include('events.urls')),
#     path('users/',include('users.urls')),
#     path('no-permission/',no_permission,name='no-permission')
# ]+ debug_toolbar_urls()

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 
