from django.contrib import admin
from django.db import models
from .models import Topic, Course, Student, Order


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','topic','price','stages','for_everyone')
    actions = ['add_50_to_hours']

    def add_50_to_hours(self, request, queryset):
        for e in queryset:
            temp = int(e.stages) + 10
            e.stages = temp
            e.save()

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name','city','upper_case_name')

    def upper_case_name(self, obj):
        return ("%s %s" % (obj.first_name, obj.last_name)).upper()
    upper_case_name.short_description = 'Student Full Name'


# Register your models here.
#admin.site.register(Course,CourseAdmin)
admin.site.register(Topic)
#admin.site.register(Course)
#admin.site.register(Student)
admin.site.register(Order)