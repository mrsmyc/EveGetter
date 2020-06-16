from django.urls import path, include
from . import views 
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from .views import myEventsList, myTickets, UserLookUp
from django.contrib.auth import views as auth_views


urlpatterns = [ 
   # url(r'^', include('django.contrib.auth.urls')),
   path(r'^register/$', views.registerPage, name='register'),   
   path(r'^login/$', views.loginPage, name="login"),
   path(r'^logout/$', views.logoutUser, name="logout"),
   path(r'^myaccount/$', views.accountControl, name="acclook"),
   path(r'^change_info/$', views.UpdateUser, name="updateuser"),
   path(r'^myevents/$',myEventsList.as_view(), name="myevents"),
   path(r'^mytickets/$', myTickets.as_view(), name="mytickets"),
   path(r'^userlook/<int:pk>/$', views.UserLookUp, name='look_for_user'),
   # path(r'^reset_password/$', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name="reset_password"),
   # path(r'^reset_password_sent/$', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name="reset_password_done"),
   # path(r'^reset/<uidb64>/<token>/$', auth_views.PasswordResetConfirmView.as_view(), name="reset_password_confirm"),
   # path(r'^reset_password_complete/$', auth_views.PasswordResetCompleteView.as_view(), name="reset_password_complete"),



   #path(r'^change-password/$', views.change_password, name="change_password"),
]