from django.contrib import admin

from users.models import Feedback, Contact


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'comment']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'message']


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Contact, ContactAdmin)


