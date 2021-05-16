from django.contrib import admin
from .models import Book,StudentExtra,IssuedBook
#admin.sites.registered(Book)
# Register your models here.

admin.site.register(Book)
admin.site.register(StudentExtra)
admin.site.register(IssuedBook)