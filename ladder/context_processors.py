def unconfirmed_matches(request):
    if request.user.is_authenticated():
        return {'unconfirmed_matches': request.user.unconfirmed_matches}
    else:
        return {}
