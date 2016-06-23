from django.contrib import admin
from contact.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ["send_user", "to_user", "homework", "title", "is_answered",
                    "added_time", "content"]
    search_fields = ["title", "homework"]
    list_filter = ["is_answered", "added_time"]
    exclude = ["slug"]


admin.site.register(Message, MessageAdmin)
