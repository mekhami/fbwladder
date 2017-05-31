from django.contrib import admin

from .models import Match, Report


class MatchAdmin(admin.ModelAdmin):
    readonly_fields = ('date', 'winner_rating_change', 'loser_rating_change', 'calculated')


admin.site.register(Match, MatchAdmin)
admin.site.register(Report)
