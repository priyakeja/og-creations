from django.db import models


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default='OG Creations')
    tagline = models.CharField(max_length=100, blank=True, default='Concept To Creation')
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)

    nav_button_text = models.CharField(max_length=50, blank=True, default='Start a Project')
    nav_button_link = models.CharField(max_length=200, blank=True, default='#contact')

    phone_number = models.CharField(
        max_length=20, blank=True,
        help_text='Example: +919876543210'
    )
    phone_icon = models.CharField(
        max_length=50, default='bx bxs-phone-call',
        help_text='Boxicons class. Browse icons at boxicons.com'
    )
    whatsapp_number = models.CharField(
        max_length=20, blank=True,
        help_text='Country code + number, no plus or spaces. Example: 919876543210'
    )
    whatsapp_icon = models.CharField(max_length=50, default='bx bxl-whatsapp')
    whatsapp_message = models.CharField(
        max_length=200, blank=True,
        default='Hi OG Creations, I would like to discuss a project.'
    )

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name


class NavMenuItem(models.Model):
    title = models.CharField(max_length=50)
    link = models.CharField(max_length=200, default='#home', help_text='Example: #about or /about/')
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Navbar Menu Item'
        verbose_name_plural = 'Navbar Menu Items'

    def __str__(self):
        return self.title


class HeroSection(models.Model):
    eyebrow = models.CharField(max_length=150, blank=True, default='Film & Creative Production · Chennai')
    heading_before = models.CharField(max_length=50, default='From', help_text='Normal text before the italic word')
    heading_italic = models.CharField(max_length=50, default='Concept', help_text='Italic word')
    heading_after = models.CharField(max_length=80, default='to Creation', help_text='Second line')
    description = models.TextField(
        default='OG Creations brings stories to the screen — movies, web series, commercials, '
                'casting, modeling and events, produced with cinematic care.'
    )
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True)

    primary_button_text = models.CharField(max_length=50, blank=True, default='Start a Project')
    primary_button_link = models.CharField(max_length=200, blank=True, default='#contact')
    secondary_button_text = models.CharField(max_length=50, blank=True, default='Explore Our Craft')
    secondary_button_link = models.CharField(max_length=200, blank=True, default='#works')

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Section'

    def __str__(self):
        return 'Hero Section'


class HeroTag(models.Model):
    hero = models.ForeignKey(HeroSection, on_delete=models.CASCADE, related_name='tags')
    title = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    


class MarqueeSetting(models.Model):
    speed = models.PositiveIntegerField(
        default=35,
        help_text='Seconds for one full loop. Bigger number = slower. Try 25 to 50.'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Moving Strip'
        verbose_name_plural = 'Moving Strip'

    def __str__(self):
        return 'Moving Strip'


class MarqueeItem(models.Model):
    strip = models.ForeignKey(MarqueeSetting, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class AboutSection(models.Model):
    eyebrow = models.CharField(max_length=80, blank=True, default='The Studio')
    heading_normal = models.CharField(
        max_length=150, default='Built for stories that deserve',
        help_text='Black part of the heading'
    )
    heading_highlight = models.CharField(
        max_length=100, default='the big screen.',
        help_text='Maroon part of the heading'
    )
    paragraph_one = models.TextField(
        default='OG CREATIONS is a film and creative production house devoted to the craft of cinema '
                '— direction, cinematography, casting, art and post, held to a single standard of finish.'
    )
    paragraph_two = models.TextField(
        blank=True,
        default='We keep our sets bright and our crews sharp. Whether the brief is a feature film, '
                'a streaming series or a sixty-second spot, the work is art-directed frame by frame '
                '— nothing left to default.'
    )
    button_text = models.CharField(max_length=60, blank=True, default='See What We Produce')
    button_link = models.CharField(max_length=200, blank=True, default='#works')

    image_main = models.ImageField(upload_to='about/', blank=True, null=True, help_text='Big image (top left of the group)')
    image_side = models.ImageField(upload_to='about/', blank=True, null=True, help_text='Tall image (right side)')
    image_bottom = models.ImageField(upload_to='about/', blank=True, null=True, help_text='Bottom image (overlaps the big one)')

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'About Section'
        verbose_name_plural = 'About Section'

    def __str__(self):
        return 'About Section'
    


class ServicesSection(models.Model):
    eyebrow = models.CharField(max_length=80, blank=True, default='Our Services')
    heading = models.CharField(max_length=120, default='What We Create')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Services Section'
        verbose_name_plural = 'Services Section'

    def __str__(self):
        return 'Services Section'


class ServiceCard(models.Model):
    section = models.ForeignKey(ServicesSection, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='services/', help_text='Portrait image, about 800 x 1000')
    order = models.PositiveIntegerField(default=1, help_text='Also decides the number badge: 1 = 01, 2 = 02')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    


class ProjectsSection(models.Model):
    eyebrow = models.CharField(max_length=80, blank=True, default='Featured Projects')
    heading = models.CharField(max_length=120, default='Our Works')
    all_label = models.CharField(max_length=30, default='All', help_text='Text of the first filter tab')
    note = models.CharField(
        max_length=250, blank=True,
        default="Project titles and imagery are placeholders until OG Creations' portfolio is added.",
        help_text='Small grey text under the grid. Leave empty to hide it.'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Projects Section'
        verbose_name_plural = 'Projects Section'

    def __str__(self):
        return 'Projects Section'


class ProjectCategory(models.Model):
    name = models.CharField(max_length=50, help_text='Shown as a filter tab and on each card')
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Project Category'
        verbose_name_plural = 'Project Categories'

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=100, default='Project Title')
    category = models.ForeignKey(ProjectCategory, on_delete=models.PROTECT, related_name='projects')
    image = models.ImageField(upload_to='projects/', help_text='Landscape image, about 1600 x 1000')
    video_url = models.URLField(
        blank=True,
        help_text='Optional. YouTube or Vimeo link. If filled, a play button appears on hover.'
    )
    order = models.PositiveIntegerField(default=1, help_text='Order 1 becomes the big card')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    


class BehindScenesSection(models.Model):
    heading_bold = models.CharField(max_length=40, default='Behind', help_text='Bold maroon word')
    heading_light = models.CharField(max_length=60, default='The Scenes', help_text='Black part of the heading')

    left_top_image = models.ImageField(upload_to='behind/', blank=True, null=True, help_text='Portrait 4:5, about 800 x 1000')
    left_top_caption = models.CharField(max_length=80, blank=True, default='Scene 72 · Take 4')

    left_bottom_image = models.ImageField(upload_to='behind/', blank=True, null=True, help_text='Portrait 4:5, about 800 x 1000')
    left_bottom_caption = models.CharField(max_length=80, blank=True, default='The quiet before the scene')

    center_image = models.ImageField(upload_to='behind/', blank=True, null=True, help_text='Tall portrait, about 1000 x 1600')
    center_title = models.CharField(max_length=100, blank=True, default='Every frame earns its place')
    center_subtitle = models.CharField(max_length=150, blank=True, default='A working set, from first light to last.')

    right_top_image = models.ImageField(upload_to='behind/', blank=True, null=True, help_text='Portrait 4:5, about 800 x 1000')
    right_top_caption = models.CharField(max_length=80, blank=True, default='Every frame, monitored')

    right_bottom_image = models.ImageField(upload_to='behind/', blank=True, null=True, help_text='Portrait 4:5, about 800 x 1000')
    right_bottom_caption = models.CharField(max_length=80, blank=True, default='Golden hour, on location')

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Behind The Scenes Section'
        verbose_name_plural = 'Behind The Scenes Section'

    def __str__(self):
        return 'Behind The Scenes Section'
    


class ProcessSection(models.Model):
    eyebrow = models.CharField(max_length=80, blank=True, default='Our Production Process')
    heading = models.CharField(max_length=120, default='Five Stages, One Vision')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Process Section'
        verbose_name_plural = 'Process Section'

    def __str__(self):
        return 'Process Section'


class ProcessStep(models.Model):
    section = models.ForeignKey(ProcessSection, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    icon = models.CharField(
        max_length=50, default='bx bx-bulb',
        help_text='Boxicons class. Browse icons at boxicons.com. Example: bx bx-bulb'
    )
    order = models.PositiveIntegerField(default=1, help_text='Also decides the number: 1 = 01, 2 = 02')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    


class UpcomingSection(models.Model):
    heading = models.CharField(max_length=100, default='Upcoming Projects')
    tagline = models.CharField(
        max_length=200, blank=True,
        default='Exciting Stories · Powerful Performances · Coming Soon'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Upcoming Projects Section'
        verbose_name_plural = 'Upcoming Projects Section'

    def __str__(self):
        return 'Upcoming Projects Section'

    @property
    def tagline_parts(self):
        return [p.strip() for p in self.tagline.split('·') if p.strip()]


class UpcomingProject(models.Model):
    label = models.CharField(max_length=40, blank=True, default='Upcoming', help_text='Small text above the title')
    title = models.CharField(max_length=120)
    tagline = models.TextField(blank=True, help_text='Press Enter to start a new line')
    release_date = models.CharField(max_length=40, blank=True, default='Dec 2025')
    release_status = models.CharField(max_length=40, blank=True, default='In Cinemas')
    image = models.ImageField(upload_to='upcoming/', help_text='Landscape image, about 1300 x 1100')
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Upcoming Project'
        verbose_name_plural = 'Upcoming Projects'

    def __str__(self):
        return self.title


class CastGroup(models.Model):
    project = models.ForeignKey(UpcomingProject, on_delete=models.CASCADE, related_name='cast')
    label = models.CharField(max_length=60, help_text='Example: Lead Actor')
    names = models.TextField(help_text='One name per line')
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label

    @property
    def names_list(self):
        return [n.strip() for n in self.names.splitlines() if n.strip()]
    


class WhyChooseSection(models.Model):
    eyebrow = models.CharField(max_length=80, blank=True, default='Why Choose OG Creations')
    heading = models.CharField(max_length=120, default='Crafted with Intent')
    image = models.ImageField(upload_to='why/', blank=True, null=True, help_text='Tall portrait image, about 1000 x 1350')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Why Choose Us Section'
        verbose_name_plural = 'Why Choose Us Section'

    def __str__(self):
        return 'Why Choose Us Section'


class WhyPoint(models.Model):
    section = models.ForeignKey(WhyChooseSection, on_delete=models.CASCADE, related_name='points')
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=250)
    order = models.PositiveIntegerField(default=1, help_text='Also decides the number: 1 = 01, 2 = 02')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    
class ContactSection(models.Model):
    eyebrow = models.CharField(max_length=80, blank=True, default='Start a Project')
    heading = models.CharField(max_length=100, default='Have a Story to Tell?')
    subheading = models.CharField(
        max_length=100, blank=True, default="Let's Bring It to Life.",
        help_text='Maroon italic line under the heading'
    )
    background_image = models.ImageField(
        upload_to='contact/', blank=True, null=True,
        help_text='Wide background image, about 1800 x 900'
    )

    # ----- contact details (left side) -----
    phone_icon = models.CharField(max_length=50, default='bx bx-phone', help_text='Boxicons class')
    phone_label = models.CharField(max_length=30, default='Phone')
    phone_display = models.CharField(max_length=30, default='9884277001', help_text='Text shown on the page')
    phone_number = models.CharField(
        max_length=20, default='+919884277001',
        help_text='Used for tap-to-call. Example: +919884277001'
    )

    email_icon = models.CharField(max_length=50, default='bx bx-envelope', help_text='Boxicons class')
    email_label = models.CharField(max_length=30, default='Email')
    email = models.EmailField(default='ogcreationsofficial@gmail.com')

    address_icon = models.CharField(max_length=50, default='bx bx-map', help_text='Boxicons class')
    address_label = models.CharField(max_length=30, default='Studio')
    address = models.TextField(default='No. 15, Rajamannar Salai, KK Nagar, Chennai 600 078')

    # ----- map -----
    map_embed_url = models.URLField(
        max_length=1000, blank=True,
        help_text='Google Maps > Share > Embed a map > copy ONLY the link inside src="...". '
                  'Leave empty to search the address automatically.'
    )
    map_link = models.URLField(
        max_length=1000, blank=True,
        help_text='Google Maps share link, opens when the address or directions button is clicked. '
                  'Leave empty to search the address automatically.'
    )

    # ----- form text -----
    f_name_label = models.CharField(max_length=40, default='Full Name')
    f_name_placeholder = models.CharField(max_length=60, default='Your name')
    f_phone_label = models.CharField(max_length=40, default='Phone Number')
    f_phone_placeholder = models.CharField(max_length=60, blank=True, default='10-digit number')
    f_email_label = models.CharField(max_length=40, default='Email Address')
    f_email_placeholder = models.CharField(max_length=60, default='you@example.com')
    f_service_label = models.CharField(max_length=40, default='Service Required')
    f_service_placeholder = models.CharField(max_length=60, default='Select a service')
    f_details_label = models.CharField(max_length=40, default='Project Details')
    f_details_placeholder = models.CharField(max_length=80, default='Tell us about your project')
    button_text = models.CharField(max_length=40, default='Start a Project')

    # ----- where the enquiry goes -----
    notify_email = models.EmailField(
        blank=True,
        help_text='Enquiries are emailed here. Leave empty to use the Email above.'
    )
    whatsapp_number = models.CharField(
        max_length=20, blank=True,
        help_text='Country code + number, no plus or spaces. Example: 919884277001. '
                  'Leave empty to use the WhatsApp number in Site Settings.'
    )

    # ----- thank you message -----
    success_title = models.CharField(max_length=80, default='Thank You!')
    success_message = models.CharField(
        max_length=250,
        default='Your enquiry has been received. Our team will get back to you shortly.'
    )
    success_button_text = models.CharField(max_length=40, default='Send Another Enquiry')

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Contact Section'
        verbose_name_plural = 'Contact Section'

    def __str__(self):
        return 'Contact Section'

    @property
    def tel_href(self):
        return 'tel:' + (self.phone_number or self.phone_display).replace(' ', '')

    @property
    def mailto_href(self):
        return 'mailto:' + self.email

    @property
    def map_url(self):
        from urllib.parse import quote
        if self.map_link:
            return self.map_link
        return 'https://www.google.com/maps/search/?api=1&query=' + quote(' '.join(self.address.split()))

    @property
    def embed_src(self):
        from urllib.parse import quote
        if self.map_embed_url:
            return self.map_embed_url
        return 'https://www.google.com/maps?q=' + quote(' '.join(self.address.split())) + '&output=embed'


class ContactService(models.Model):
    name = models.CharField(max_length=60, help_text='Shown in the Service Required dropdown')
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Contact Form Service'
        verbose_name_plural = 'Contact Form Services'

    def __str__(self):
        return self.name


class ProjectEnquiry(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    service = models.CharField(max_length=60)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False, help_text='Tick after you have replied')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project Enquiry'
        verbose_name_plural = 'Project Enquiries'

    def __str__(self):
        return f'{self.name} - {self.service}'
    
class FooterSection(models.Model):
    logo = models.ImageField(
        upload_to='footer/', blank=True, null=True,
        help_text='Leave empty to use the logo from Site Settings'
    )
    brand_name = models.CharField(max_length=80, default='OG Creations')
    brand_tagline = models.CharField(max_length=80, blank=True, default='Concept To Creation')
    description = models.CharField(
        max_length=200, blank=True,
        default='Film and creative production, from concept to creation.'
    )
    follow_label = models.CharField(max_length=40, blank=True, default='Follow Us,')

    navigate_title = models.CharField(max_length=40, default='Navigate')
    services_title = models.CharField(max_length=40, default='Services')
    contact_title = models.CharField(max_length=40, default='Contact')

    phone_display = models.CharField(
        max_length=30, blank=True,
        help_text='Leave empty to use the phone from Contact Section'
    )
    phone_number = models.CharField(
        max_length=20, blank=True,
        help_text='Used for tap-to-call. Example: +919884277001'
    )
    email = models.EmailField(blank=True, help_text='Leave empty to use the email from Contact Section')
    address = models.TextField(blank=True, help_text='Leave empty to use the address from Contact Section')
    map_link = models.URLField(
        max_length=1000, blank=True,
        help_text='Google Maps link opened when the address is clicked. Leave empty to search the address.'
    )

    copyright_text = models.CharField(
        max_length=150, default='OG Creations. All rights reserved.',
        help_text='The symbol and the year are added automatically'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Footer Section'
        verbose_name_plural = 'Footer Section'

    def __str__(self):
        return 'Footer Section'

    def _contact(self):
        if not hasattr(self, '_contact_cache'):
            self._contact_cache = ContactSection.objects.filter(is_active=True).first()
        return self._contact_cache

    @property
    def show_phone(self):
        c = self._contact()
        return self.phone_display or (c.phone_display if c else '')

    @property
    def tel_href(self):
        if self.phone_number or self.phone_display:
            return 'tel:' + (self.phone_number or self.phone_display).replace(' ', '')
        c = self._contact()
        return c.tel_href if c else ''

    @property
    def show_email(self):
        c = self._contact()
        return self.email or (c.email if c else '')

    @property
    def mailto_href(self):
        return 'mailto:' + self.show_email if self.show_email else ''

    @property
    def show_address(self):
        c = self._contact()
        return self.address or (c.address if c else '')

    @property
    def map_url(self):
        from urllib.parse import quote
        if self.map_link:
            return self.map_link
        c = self._contact()
        if not self.address and c:
            return c.map_url
        return 'https://www.google.com/maps/search/?api=1&query=' + quote(' '.join(self.show_address.split()))


class FooterLink(models.Model):
    footer = models.ForeignKey(FooterSection, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=50)
    link = models.CharField(max_length=200, default='#about', help_text='Example: #about or /about/')
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Navigate Link'
        verbose_name_plural = 'Navigate Links'

    def __str__(self):
        return self.title


class FooterService(models.Model):
    footer = models.ForeignKey(FooterSection, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=50)
    link = models.CharField(max_length=200, default='#services', help_text='Example: #services')
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Footer Service'
        verbose_name_plural = 'Footer Services'

    def __str__(self):
        return self.title


class FooterSocial(models.Model):
    footer = models.ForeignKey(FooterSection, on_delete=models.CASCADE, related_name='socials')
    name = models.CharField(max_length=40, help_text='Example: Instagram (used for accessibility)')
    icon = models.CharField(
        max_length=50, default='bx bxl-instagram',
        help_text='Boxicons class. Examples: bx bxl-instagram, bx bxl-whatsapp, bx bxl-facebook, bx bxl-youtube'
    )
    url = models.URLField(max_length=500, help_text='Full link. WhatsApp example: https://wa.me/919884277001')
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Social Link'
        verbose_name_plural = 'Social Links'

    def __str__(self):
        return self.name