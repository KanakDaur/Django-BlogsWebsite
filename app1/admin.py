from django.contrib import admin
from app1.models import post,comment,Profile
# Register your models here.
class postadmin(admin.ModelAdmin):
    list_display = ['title','slug','author','body','publish','created','updated','status','category','image']
    prepopulated_fields = {'slug':('title',)}
admin.site.register(post,postadmin)

class commentadmin(admin.ModelAdmin):
    list_display = ['pst','user','content','comment_time']
admin.site.register(comment,commentadmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','dob','photo')
admin.site.register(Profile,ProfileAdmin)
