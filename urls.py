from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('',views.introPage,name ='introPage'),
	path('register/',views.userRegister,name ='userRegister'),
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
	path('login/',views.userLogin,name ='userLogin'),
	path('logout/',views.userLogout,name ='userLogout'),
	path('contact/',views.Contact_PG,name ='Contact_PG'),
	path('findpg/',views.Find_pg,name = 'Find_pg'),
	path('listpg/',views.listPG,name ='listPG'),
	path('addpg/',views.addPG,name ='addPG'),
	path('viewpg/<int:pg_id>/',views.viewPG,name ='viewPG'),
	path('editpg/<int:pg_id>/',views.editPG,name ='editPG'),
	path('deletepg/<int:pg_id>/',views.deletePG,name ='deletePG'),
	path('changepassword/<int:user_id>/',views.changePassword,name ='changePassword'),
	path('sample_ajax_view/<int:pg_id>/',views.sample_ajax_view,name = 'sample_ajax_view'),
	]