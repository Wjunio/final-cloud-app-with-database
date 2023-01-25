from django.contrib import admin
# <HINT> Import any new Models here
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5
    
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'choice_text', 'correct')

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 5
    
class QuestionInline(admin.StackedInline):
    model = Question
    inlines = [ChoiceInline]
    extra = 3

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']
    
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text',)
    search_fields = ['text',]

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
