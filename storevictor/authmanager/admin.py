from django.contrib import admin
#from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model
from . models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#from . forms import UserAdminCreationForm, UserAdminChangeForm


from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


User = get_user_model()
# Register your models here.


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    #form = UserAdminChangeForm
    #add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin','staff','title','first_name','last_name','telephone')
    list_filter = ('admin','staff')
    fieldsets = (
        (None, {'fields': ( 'email','password')}),

        ('Personal info', {'fields': ('title','first_name', 'last_name','telephone')}),
        ('Permissions', {'fields': ('admin','staff')}),
      

    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'other_names', 'last_name', 'network' ,'password1', 'password2')}
        ),

    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()




admin.site.register(User, UserAdmin)

admin.site.register(Profile)
## Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

