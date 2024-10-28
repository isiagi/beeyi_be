"""
URL configuration for beyi_be project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from product import urls as product_urls
from category import urls as category_urls
from subcategory import urls as subcategory_urls
from userauth import urls as userauth_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include(userauth_urls)),
    path('api/products/', include(product_urls)),
    path('api/categories/', include(category_urls)),
    path('api/subcategories/', include(subcategory_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,)





