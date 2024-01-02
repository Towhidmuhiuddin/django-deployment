from django.urls import path
from login_app import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

app_name = 'login_app'

urlpatterns = [
    path('',views.index, name='index'),
    path('user_form/',views.userform, name='user_form'),
    path('login_page/',views.login_page, name='login_page'),
    path('user_login/',views.user_login,name='user_login'),
    path('logout/',views.logout_page, name='logout'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)