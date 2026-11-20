from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/accounts/', include('accounts.urls')),

    path('api/', include('projects.urls')),

    path('api/', include('tasks.urls')),

    path('api/', include('dashboard.urls')),

    path('api/', include('risks.urls')),

    path('api/', include('notifications.urls')),

    path('api/', include('reports.urls')),
]