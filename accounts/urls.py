from django.urls import path
from . import views
from .views import change_password,update_profile, get_all_users,admin_generate_report,get_test_report,user_test_report,generate_pdf
urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('change_password/', change_password, name='change_password'),
    path('update_profile/<int:user_id>/', update_profile, name='update_profile'),
    path('save_test_report/', admin_generate_report, name='save_test_report'),
    path('get_all_users/', get_all_users, name='get_all_users'),
    path('get_test_report/', get_test_report, name='get_test_report'),
    path('user_test_report/', user_test_report, name='user_test_report'),
    path('generate-pdf/<int:id>/', generate_pdf, name='generate_pdf'),
    path("admin_dashboard", views.admin_dashboard_view, name="admin_dashboard"),
    path("user_dashboard", views.user_dashboard_view, name="user_dashboard"),
]
