from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',Home,name='home' ),
    path('login/',Login,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('register/', register, name="register"),
    path('search/', search,name='search'),
    path('donate/',donate,name='donate' ),
    path('detail/<slug>',detail,name='detail'),
    path('status/<str>',status_news,name='status'),
    path('category/<str>',category,name='category'),
    path('main_category/<str>',main_category,name='main_category'),
    path('tinymce/', include('tinymce.urls')),

    path('addnews/',AddNews,name='addnews'),
    path('add_main_category/',AddMainCategory,name='add_main_category'),
    path('addcategory/<main>',AddCategory,name='addcategory'),
    path('editcategory/<title>',editCategory,name='editcategory'),
    path('edit_main_category/<title>',editMainCategory,name='edit_main_category'),
    path('editnews/<slug>',editNews,name='editnews'),
    path('deletenews/<slug>',delNews,name='deletenews'),
    path('delMainCat/<title>',delMainCat,name='delMainCat'),
    path('delCat/<title>',delCat,name='delCat'),
    path('dashboard/',Admin_panel,name='dashboard'),
    path('admin_news/', Admin_news,name='admin_news'),
    path('admin_category/', Admin_category,name='admin_category'),

    path('donations/', Admin_donation,name='donations'),


    path('videos/', Admin_Videos,name='videos'),
    path('addvideo/',AddVideo,name='addvideo'),
    path('editvideo/<id>',editVideo,name='editvideo'),
    path('delvideo/<id>',delVideos,name='delvideo'),
    
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
