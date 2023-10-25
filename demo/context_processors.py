from .models import UserPreference


def preferred_theme_processor(request):
    if request.user.is_authenticated:
        stored_user_pref = UserPreference.get_user_preferences(request.user.id)
        preferred_theme = stored_user_pref.preferred_theme if stored_user_pref.preferred_theme else None
    else:
        preferred_theme = None
    return {
        'preferred_theme': preferred_theme
    }
