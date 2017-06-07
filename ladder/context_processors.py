from .models import Report


def unconfirmed_matches(request):
    if request.user.is_authenticated():
        return {'unconfirmed_matches': request.user.unconfirmed_matches}
    else:
        return {}

def outstanding_reports(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        return {'outstanding_reports': Report.objects.filter(resolved=False).count()}
    else:
        return {}

def no_profile_data(request):
    if request.user.is_authenticated():
        if not request.user.battlenet and not request.user.iccup:
            return {'no_profile': True}
        else:
            return {}
    else:
        return {}
