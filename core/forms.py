from django import forms
from .models import EmployeeProfile, Attachment, User


from django import forms
from django.core.exceptions import ValidationError
from .models import EmployeeProfile, User


class EmployeeCreateForm(forms.ModelForm):
    full_name = forms.CharField(label="الاسم الكامل", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="البريد الإلكتروني", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="اسم المستخدم", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="كلمة المرور", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = EmployeeProfile
        fields = ['national_id', 'job_title', 'phone', 'department', 'personal_image']
        labels = {
            'national_id': 'رقم الهوية',
            'job_title': 'المسمى الوظيفي',
            'phone': 'رقم الجوال',
            'department': 'القسم',
            'personal_image': 'الصورة الشخصية',
        }
        widgets = {
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'personal_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("⚠️ اسم المستخدم مستخدم مسبقاً.")
        return username

    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        if EmployeeProfile.objects.filter(national_id=national_id).exists():
            raise ValidationError("⚠️ رقم الهوية مستخدم مسبقاً.")
        return national_id

from django import forms
from .models import EmployeeProfile

class EmployeeEditForm(forms.ModelForm):
    full_name = forms.CharField(
        label="الاسم الكامل",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل الاسم الكامل'
        })
    )
    email = forms.EmailField(
        label="البريد الإلكتروني",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@email.com'
        })
    )
    username = forms.CharField(
        label="اسم المستخدم",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل اسم المستخدم'
        })
    )
    password = forms.CharField(
        label="كلمة المرور",
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'اتركه فارغًا إذا لا تريد تغييره'
        })
    )

    class Meta:
        model = EmployeeProfile
        fields = ['national_id', 'job_title', 'phone', 'department', 'personal_image']
        labels = {
            'national_id': 'رقم الهوية',
            'job_title': 'المسمى الوظيفي',
            'phone': 'رقم الجوال',
            'department': 'القسم',
            'personal_image': 'الصورة الشخصية',
        }
        widgets = {
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل رقم الهوية'
            }),
            'job_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل المسمى الوظيفي'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '05XXXXXXXX'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: الموارد البشرية'
            }),
            'personal_image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class AttachmentEditForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

from django import forms
from django.contrib.auth.models import User
from .models import EmployeeProfile

class AddEmployeeForm(forms.ModelForm):
    full_name = forms.CharField(label="الاسم الكامل")
    email = forms.EmailField(label="البريد الإلكتروني")
    username = forms.CharField(label="اسم المستخدم")
    password = forms.CharField(label="كلمة المرور", widget=forms.PasswordInput)

    class Meta:
        model = EmployeeProfile
        fields = ['national_id', 'job_title', 'phone', 'department', 'personal_image']
        labels = {
            'national_id': 'رقم الهوية',
            'job_title': 'المسمى الوظيفي',
            'phone': 'رقم الجوال',
            'department': 'القسم',
            'personal_image': 'الصورة الشخصية',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("اسم المستخدم مستخدم بالفعل.")
        return username

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if EmployeeProfile.objects.filter(national_id=national_id).exists():
            raise forms.ValidationError("رقم الهوية مسجل مسبقًا.")
        return national_id

from django import forms
from django.core.exceptions import ValidationError
from .models import EmployeeProfile, User

class EmployeeForm(forms.ModelForm):
    full_name = forms.CharField(label="الاسم الكامل")
    email = forms.EmailField(label="البريد الإلكتروني")
    username = forms.CharField(label="اسم المستخدم")
    password = forms.CharField(label="كلمة المرور", widget=forms.PasswordInput)

    class Meta:
        model = EmployeeProfile
        fields = ['national_id', 'job_title', 'phone', 'department', 'personal_image']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("اسم المستخدم مستخدم من قبل. الرجاء اختيار اسم آخر.")
        return username

    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        if EmployeeProfile.objects.filter(national_id=national_id).exists():
            raise ValidationError("رقم الهوية مستخدم من قبل.")
        return national_id
