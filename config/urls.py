from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('assistant/', include('product.urls')),
    path('auth/', include('authorization.urls'))

]