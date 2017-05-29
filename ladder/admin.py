from django.contrib import admin

from .models import Match


class MatchAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)


admin.site.register(Match, MatchAdmin)
