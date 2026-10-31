from .models import SiteSetting, NavMenuItem, FooterSection


def site_settings(request):
    footer = FooterSection.objects.filter(is_active=True).first()
    return {
        'site': SiteSetting.objects.first(),
        'nav_items': NavMenuItem.objects.filter(is_active=True),
        'footer': footer,
        'footer_links': footer.links.filter(is_active=True) if footer else [],
        'footer_services': footer.services.filter(is_active=True) if footer else [],
        'footer_socials': footer.socials.filter(is_active=True) if footer else [],
    }