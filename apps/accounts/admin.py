from django import forms
from django.contrib import admin

from .forms import AccountAdminForm
from .models import Account
from django.contrib import messages

from apps.credentials.models import UserCategory



class UserCategoryStackedInline(admin.StackedInline):
    model = UserCategory
    extra = 0



@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'email', 'first_name', 'last_name', 'is_superuser','is_active']
    search_fields = ['email', 'uuid', 'first_name', 'last_name']
    list_filter = [
        'is_superuser',
        'is_active',
    ]
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    actions = ['generate_recovery_code']
    inlines = [UserCategoryStackedInline]

    form = AccountAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if obj is None:  # If creating a new user, ensure the password field is included
            form.base_fields['password'].widget = forms.PasswordInput()
        else:
            # Remove password field if editing an existing user
            form.base_fields['password'].widget = forms.HiddenInput()

        return form

    def get_queryset(self, request):

        return super().get_queryset(request).exclude(
            id=request.user.id
        )

    # Optionally, restrict fields for non-admin users
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['is_staff', 'is_superuser']
        return []

    def generate_recovery_code(self, request, queryset):
        for account in queryset:
            try:
                account.generate_recovery_code()
                self.message_user(request, f"Generated recovery code for {account.email}.", level=messages.SUCCESS)
            except Exception as e:
                print(e)
                self.message_user(request, f"Error generating recovery code for {account.email}: {str(e)}", level=messages.ERROR)

    generate_recovery_code.short_description = 'Generate Recovery Code for selected accounts'


admin.site.site_header = 'Ultra Secure Admin'
admin.site.site_title = 'Ultra Secure Admin'
admin.site.index_title = 'Ultra Secure'