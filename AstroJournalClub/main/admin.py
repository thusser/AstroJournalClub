import datetime

from django.contrib import admin
from AstroJournalClub.main.models import Schedule


class ScheduleAdmin(admin.ModelAdmin):
    actions = ['abort_schedule']

    def abort_schedule(self, request, queryset):
        """Abort a schedule by setting its end day to today."""
        queryset.update(end=datetime.date.today())


admin.site.register(Schedule, ScheduleAdmin)
