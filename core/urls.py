from django.urls import path
from .views import CustomLoginView, manager_dashboard, employee_profile
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import (
    CustomLoginView,
    manager_dashboard,
    employee_profile,
    add_employee,
    home,
    edit_attachment,
    delete_attachment,
    search_employees,
    edit_employee,  # ✅ هذا السطر مفقود في كودك الحالي
)


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('dashboard/manager/', manager_dashboard, name='manager_dashboard'),
    path('profile/<int:user_id>/', employee_profile, name='employee_profile'),
    path('add/', add_employee, name='add_employee'),
    path('', home, name='home'),
    path('attachment/edit/<int:attachment_id>/', edit_attachment, name='edit_attachment'),
    path('search/', views.search_employees, name='employee_search'),
    path('attachment/delete/<int:attachment_id>/', delete_attachment, name='delete_attachment'),
    path('employees/search/', views.employee_search, name='search_employees'),
    path('employee/edit/<int:user_id>/', views.edit_employee, name='edit_employee'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)