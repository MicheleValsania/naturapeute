"""naturapeute URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', naturapeute_views.Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from naturapeute import views as naturapeute_views
from blog import views as blog_views
from api import views as api_views


urlpatterns = [
    path("", naturapeute_views.HomeView.as_view()),

    path("api/therapist/<email_or_pk>", api_views.TherapistView.as_view(), name="api_therapist"),
    path("api/therapist/<id>", api_views.TherapistView.as_view(), name="api_therapist"),
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),

    path("journal/", blog_views.HomeView.as_view(), name="blog"),
    path("journal/<slug>/", blog_views.ArticleView.as_view(), name="article"),

    path("therapeutes/", naturapeute_views.TherapistsView.as_view(), name="therapists"),
    path("therapeutes/<practice_slug>/", naturapeute_views.TherapistsView.as_view(), name="therapists_practice"),
    path("therapeutes/<slug0>/<slug1>/", naturapeute_views.TherapistView.as_view(), name="therapist"),
    path(
        "therapeutes/<slug0>/<slug1>/vcf/",
        naturapeute_views.TherapistVcardView.as_view(),
        name="therapist_vcf",
    ),
    path(
        "therapeutes/<slug0>/<slug1>/<oldid>/",
        naturapeute_views.TherapistOldView.as_view(),
        name="therapist_redirect",
    ),
    path("admin/", admin.site.urls),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:  # Debug Toolbar è disponibile solo se DEBUG è True
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),  # URL Debug Toolbar
    ] + urlpatterns
