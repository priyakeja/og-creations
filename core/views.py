import logging
import re
import unicodedata
from urllib.parse import quote

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import (
    SiteSetting,
    HeroSection, MarqueeSetting, AboutSection, ServicesSection,
    ProjectsSection, ProjectCategory, Project, BehindScenesSection,
    ProcessSection, UpcomingSection, UpcomingProject, WhyChooseSection,
    ContactSection, ContactService, ProjectEnquiry,
)

logger = logging.getLogger(__name__)


def home(request):
    hero = HeroSection.objects.filter(is_active=True).prefetch_related('tags').first()
    marquee = MarqueeSetting.objects.filter(is_active=True).prefetch_related('items').first()
    about = AboutSection.objects.filter(is_active=True).first()
    services = ServicesSection.objects.filter(is_active=True).first()
    service_cards = services.cards.filter(is_active=True) if services else []

    works = ProjectsSection.objects.filter(is_active=True).first()
    projects = Project.objects.filter(
        is_active=True, category__is_active=True
    ).select_related('category')
    work_categories = ProjectCategory.objects.filter(
        is_active=True, projects__is_active=True
    ).distinct()

    bts = BehindScenesSection.objects.filter(is_active=True).first()

    process = ProcessSection.objects.filter(is_active=True).first()
    process_steps = process.steps.filter(is_active=True) if process else []

    upcoming = UpcomingSection.objects.filter(is_active=True).first()
    upcoming_projects = UpcomingProject.objects.filter(is_active=True).prefetch_related('cast')

    why = WhyChooseSection.objects.filter(is_active=True).first()
    why_points = why.points.filter(is_active=True) if why else []

    contact = ContactSection.objects.filter(is_active=True).first()
    contact_services = ContactService.objects.filter(is_active=True)

    return render(request, 'core/home.html', {
        'hero': hero,
        'marquee': marquee,
        'about': about,
        'services': services,
        'service_cards': service_cards,
        'works': works,
        'projects': projects,
        'work_categories': work_categories,
        'bts': bts,
        'process': process,
        'process_steps': process_steps,
        'upcoming': upcoming,
        'upcoming_projects': upcoming_projects,
        'why': why,
        'why_points': why_points,
        'contact': contact,
        'contact_services': contact_services,
    })


# ---------------------------------------------------------------
# Contact form
# ---------------------------------------------------------------
def _validate_enquiry(data):
    errors = {}

    # Name: letters only, at least 3 letters
    name = data['name']
    if not name:
        errors['name'] = 'Please enter your full name.'
    elif any(ch.isdigit() for ch in name):
        errors['name'] = 'Name should not contain numbers.'
    elif not all(ch.isalpha() or unicodedata.category(ch).startswith('M') or ch in " .'-" for ch in name):
        errors['name'] = 'Name can contain letters only.'
    elif sum(ch.isalpha() for ch in name) < 3:
        errors['name'] = 'Name must be at least 3 characters.'

    # Phone: exactly 10 digits, without country code
    if not data['phone']:
        errors['phone'] = 'Please enter your phone number.'
    elif not re.fullmatch(r'\d{10}', data['phone']):
        errors['phone'] = 'Enter a valid 10-digit phone number (without +91).'

    # Email
    if not data['email']:
        errors['email'] = 'Please enter your email address.'
    else:
        try:
            validate_email(data['email'])
        except ValidationError:
            errors['email'] = 'Enter a valid email address.'

    # Service must be one of the active options
    if not data['service']:
        errors['service'] = 'Please select a service.'
    elif not ContactService.objects.filter(is_active=True, name=data['service']).exists():
        errors['service'] = 'Please select a service from the list.'

    # Details
    if not data['details']:
        errors['details'] = 'Please share your project details.'
    elif len(data['details']) < 10:
        errors['details'] = 'Please add a little more detail (at least 10 characters).'

    return errors


def _whatsapp_digits(contact):
    raw = (contact.whatsapp_number if contact else '') or ''
    if not raw:
        site = SiteSetting.objects.first()
        raw = site.whatsapp_number if site else ''
    digits = re.sub(r'\D', '', raw)
    if len(digits) == 10:
        digits = '91' + digits
    return digits


@require_POST
def contact_submit(request):
    # hidden spam trap: bots fill it, humans never see it
    if request.POST.get('website'):
        return JsonResponse({'ok': True, 'whatsapp_url': ''})

    data = {k: (request.POST.get(k) or '').strip()
            for k in ('name', 'phone', 'email', 'service', 'details')}
    data['name'] = ' '.join(data['name'].split())

    errors = _validate_enquiry(data)
    if errors:
        return JsonResponse({'ok': False, 'errors': errors}, status=400)

    enquiry = ProjectEnquiry.objects.create(**data)
    contact = ContactSection.objects.filter(is_active=True).first()

    # ----- email -----
    to_email = ''
    if contact:
        to_email = contact.notify_email or contact.email
    to_email = to_email or settings.DEFAULT_FROM_EMAIL
    try:
        body = (
            'New project enquiry from the OG Creations website\n\n'
            f'Name: {enquiry.name}\n'
            f'Phone: +91 {enquiry.phone}\n'
            f'Email: {enquiry.email}\n'
            f'Service: {enquiry.service}\n\n'
            f'Project details:\n{enquiry.details}\n'
        )
        EmailMessage(
            subject=f'New Project Enquiry - {enquiry.name} ({enquiry.service})',
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
            reply_to=[enquiry.email],
        ).send(fail_silently=False)
        enquiry.email_sent = True
        enquiry.save(update_fields=['email_sent'])
    except Exception:
        logger.exception('Enquiry email could not be sent')

    # ----- whatsapp link (opens WhatsApp with the message ready) -----
    wa_url = ''
    digits = _whatsapp_digits(contact)
    if digits:
        text = (
            '*New Project Enquiry - OG Creations*\n\n'
            f'*Name:* {enquiry.name}\n'
            f'*Phone:* +91 {enquiry.phone}\n'
            f'*Email:* {enquiry.email}\n'
            f'*Service:* {enquiry.service}\n'
            f'*Project Details:* {enquiry.details}'
        )
        wa_url = f'https://wa.me/{digits}?text={quote(text)}'

    return JsonResponse({'ok': True, 'whatsapp_url': wa_url})