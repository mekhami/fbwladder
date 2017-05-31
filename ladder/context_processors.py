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
