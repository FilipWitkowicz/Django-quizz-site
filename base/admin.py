from django.contrib import admin

from .models import Quest, User, Contact, Answer_response

# Register your models here.

admin.site.register(User)
admin.site.register(Quest)
admin.site.register(Contact)
admin.site.register(Answer_response)
