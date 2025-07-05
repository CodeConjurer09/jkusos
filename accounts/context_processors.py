from .models import ContactSettings

def contact_settings(request):
    contact_info = ContactSettings.objects.last()
    return {'contact_info': contact_info}
