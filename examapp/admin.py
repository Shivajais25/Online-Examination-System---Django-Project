from django.contrib import admin
from examapp.models import Candidate, Subject, Question, Result, UserProfile
# Register your models here.
admin.site.register(Candidate)
admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(UserProfile)