from . import views
from django.urls import path, re_path
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView
from nais_storage.views import view_main_page

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    re_path(r'^password-change/$', PasswordChangeView.as_view(), name='password_change'),
    re_path(r'^password-change/done/$', PasswordChangeDoneView.as_view(), name='password_change_done'),
    re_path(r'^password-reset/$', PasswordResetView.as_view(), name='password_reset'),
    re_path(r'^password-reset/done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    path('make_box_order', views.make_box_order, name='make_box_order'),
    path('make_season_order', views.make_season_order, name='make_season_order'),
    path('move_to_profile', views.move_to_profile, name='move_to_profile'),
    path('move_to_main', view_main_page, name='move_to_main'),
    path('make_payment', views.make_payment, name="make_payment"),
    path('show_success_payment', views.show_success_payment, name="show_success_payment"),
]