from django.contrib import admin
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from .models import Match, Report


class ConfirmedMatchFilter(admin.SimpleListFilter):
    title = _('confirmed',)
    parameter_name = 'confirmed'

    def lookups(self, request, model_admin):
        return (
            ('confirmed', _('confirmed by both players')),
            ('unconfirmed', _('not confirmed by both players')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'confirmed':
            return queryset.filter(winner_confirmed=True, loser_confirmed=True)
        elif self.value() == 'unconfirmed':
            return queryset.filter(Q(winner_confirmed=False) | Q(loser_confirmed=False))


class NoRaceFilter(admin.SimpleListFilter):
    title = _('submitted races',)
    parameter_name = 'unraced'

    def lookups(self, request, model_admin):
        return (
            ('unraced', _('races not set')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'unraced':
            return queryset.filter(Q(winner_race__isnull=True) | Q(loser_race__isnull=True) | Q(winner_race__exact='') | Q(loser_race__exact=''))


class MatchAdmin(admin.ModelAdmin):
    readonly_fields = ('date', 'winner_rating_change', 'loser_rating_change', 'calculated')
    list_filter = (ConfirmedMatchFilter, NoRaceFilter)


admin.site.register(Match, MatchAdmin)
admin.site.register(Report)
