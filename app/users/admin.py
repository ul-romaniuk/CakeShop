from django.contrib import admin

from users.models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'comment']


admin.site.register(Feedback, FeedbackAdmin)

