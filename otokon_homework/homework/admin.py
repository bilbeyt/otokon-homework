from django.contrib import admin
from homework.models import Homework, Lecture, AnswerSheet


class LectureAdmin(admin.ModelAdmin):
    list_display = ["name", "publish_date"]
    exclude = ["slug", "publish_date"]
    list_filter = ["publish_date"]


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ["lecture", "number", "content", "is_available",
                    "publish_date"]
    list_filter = ["publish_date", "lecture", "is_available"]
    exclude = ["slug", "publish_date"]
    search_fields = ["content", "lecture"]


class AnswerSheetAdmin(admin.ModelAdmin):
    list_display = ["user", "homework", "comment", "publish_date"]
    list_filter = ["publish_date", "homework"]
    exclude = ["slug", "publish_date"]
    search_fields = ["user"]


admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(AnswerSheet, AnswerSheetAdmin)
