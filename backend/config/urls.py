from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from .routers import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("api/__debug__/", include(debug_toolbar.urls)),)

if settings.API_DOCS_ENABLE:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

    urlpatterns += (
        path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    )
