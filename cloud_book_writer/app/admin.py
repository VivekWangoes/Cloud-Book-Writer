from django.contrib import admin
from .models import BookModel, User, Section  # Subsection, SubsectionLink

admin.site.register(BookModel)
admin.site.register(User)
# admin.site.register(Section)
# admin.site.register(Subsection)
# admin.site.register(SubsectionLink)


class SectionAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


admin.site.register(Section, SectionAdmin)
