from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from tracker import views as tracker_view
from tracker import urls as tracker_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tracker/', include(tracker_urls)),
    path('logout/', tracker_view.user_logout, name='logout'),
    re_path(r'^$', tracker_view.index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
