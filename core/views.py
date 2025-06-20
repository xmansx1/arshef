from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Attachment, EmployeeProfile, User
from .forms import AttachmentEditForm, EmployeeCreateForm, EmployeeEditForm

from django.contrib.auth.decorators import user_passes_test

def is_manager(user):
    return user.is_authenticated and user.role == 'manager'

def is_employee(user):
    return user.is_authenticated and user.role == 'employee'

class CustomLoginView(LoginView):
    template_name = 'core/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.role == 'manager':
            return '/dashboard/manager/'
        else:
            return f'/profile/{user.id}/'


def home(request):
    return render(request, 'core/home.html')


def is_manager(user):
    return user.role == 'manager'


@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    employees = EmployeeProfile.objects.order_by('-id')
    latest_employees = EmployeeProfile.objects.order_by('-id')[:5]
    return render(request, 'core/manager_dashboard.html', {
        'employees': employees,
        'latest_employees': latest_employees
    })

from django.contrib import messages

@login_required
def employee_profile(request, user_id):
    try:
        profile = EmployeeProfile.objects.get(user_id=user_id)
    except EmployeeProfile.DoesNotExist:
        return redirect('logout')

    if request.user.id != user_id and request.user.role != 'manager':
        return redirect('login')

    if request.method == 'POST' and request.user.role == 'manager':
        if profile.attachments.count() < 10:
            title = request.POST.get('title')
            file = request.FILES.get('file')
            if title and file:
                Attachment.objects.create(profile=profile, title=title, file=file)
                messages.success(request, "✅ تم رفع المرفق بنجاح.")
                return redirect('employee_profile', user_id=user_id)
            else:
                messages.error(request, "❌ يرجى تعبئة جميع الحقول المطلوبة.")
        else:
            messages.warning(request, "⚠️ تم الوصول إلى الحد الأقصى للمرفقات (10).")

    return render(request, 'core/employee_profile.html', {'profile': profile})


from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import EmployeeCreateForm
from .models import User, EmployeeProfile
 

@login_required
@user_passes_test(is_manager)
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            national_id = form.cleaned_data['national_id']

            # تحقق من عدم تكرار اسم المستخدم
            if User.objects.filter(username=username).exists():
                form.add_error('username', '⚠️ اسم المستخدم مستخدم مسبقاً.')
            # تحقق من عدم تكرار الهوية الوطنية
            elif EmployeeProfile.objects.filter(national_id=national_id).exists():
                form.add_error('national_id', '⚠️ رقم الهوية مستخدم مسبقاً.')
            else:
                try:
                    # إنشاء المستخدم
                    user = User.objects.create(
                        username=username,
                        email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['full_name'],
                        role='employee',
                        password=make_password(form.cleaned_data['password'])
                    )

                    # إنشاء الملف الشخصي
                    profile = form.save(commit=False)
                    profile.user = user
                    profile.personal_image = form.cleaned_data.get('personal_image')
                    profile.save()

                    messages.success(request, '✅ تم إضافة الموظف بنجاح.')
                    return redirect('add_employee')

                except IntegrityError:
                    form.add_error(None, '❌ حدث خطأ في إنشاء المستخدم. الرجاء المحاولة مجددًا.')
        else:
            messages.error(request, '❌ تأكد من صحة البيانات المدخلة.')

    else:
        form = EmployeeCreateForm()

    return render(request, 'core/add_employee.html', {'form': form})

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import Attachment
from .forms import AttachmentEditForm


def is_manager(user):
    return user.is_superuser or user.role == 'manager'


@login_required
@user_passes_test(is_manager)
def edit_attachment(request, attachment_id):
    attachment = get_object_or_404(Attachment, id=attachment_id)

    if request.method == 'POST':
        form = AttachmentEditForm(request.POST, request.FILES, instance=attachment)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ تم حفظ التعديلات على المرفق بنجاح.")
            return redirect('employee_profile', user_id=attachment.profile.user.id)
        else:
            messages.error(request, "❌ يوجد أخطاء في البيانات المدخلة، يرجى التحقق.")
    else:
        form = AttachmentEditForm(instance=attachment)

    return render(request, 'core/edit_attachment.html', {
        'form': form,
        'attachment': attachment
    })


@login_required
@user_passes_test(is_manager)
def search_employees(request):
    query_name = request.GET.get('name')
    query_nid = request.GET.get('nid')
    query_phone = request.GET.get('phone')

    results = EmployeeProfile.objects.all()

    if query_name:
        results = results.filter(user__first_name__icontains=query_name)
    if query_nid:
        results = results.filter(national_id__icontains=query_nid)
    if query_phone:
        results = results.filter(phone__icontains=query_phone)

    return render(request, 'core/search.html', {'results': results})


@login_required
@user_passes_test(is_manager)
def delete_attachment(request, attachment_id):
    attachment = get_object_or_404(Attachment, id=attachment_id)
    employee_id = attachment.profile.user.id
    attachment.delete()
    return redirect('employee_profile', user_id=employee_id)


@login_required
@user_passes_test(is_manager)
def edit_employee(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(EmployeeProfile, user=user)

    if request.method == 'POST':
        form = EmployeeEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            # تحديث بيانات المستخدم
            user.first_name = form.cleaned_data['full_name'].split()[0]
            user.last_name = ' '.join(form.cleaned_data['full_name'].split()[1:])
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            profile.save()
            messages.success(request, "✅ تم حفظ التعديلات بنجاح.")
            return redirect('employee_profile', user_id=user.id)
        else:
            messages.error(request, "❌ يوجد أخطاء في النموذج.")
    else:
        initial_data = {
            'full_name': f"{user.first_name} {user.last_name}",
            'email': user.email,
            'username': user.username,
        }
        form = EmployeeEditForm(instance=profile, initial=initial_data)

    return render(request, 'core/edit_employee.html', {
        'form': form,
        'profile': profile,
    })

from django.shortcuts import render
from .models import EmployeeProfile

def employee_search(request):
    name = request.GET.get('name')
    nid = request.GET.get('nid')
    phone = request.GET.get('phone')

    results = EmployeeProfile.objects.all()

    if name:
        results = results.filter(user__first_name__icontains=name)  # حسب ما تستخدم
    if nid:
        results = results.filter(national_id__icontains=nid)
    if phone:
        results = results.filter(phone__icontains=phone)

    return render(request, 'core/search.html', {'results': results})
