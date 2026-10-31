from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSetting, NavMenuItem, HeroSection, HeroTag,
    MarqueeSetting, MarqueeItem, AboutSection,
    ServicesSection, ServiceCard,
    ProjectsSection, ProjectCategory, Project,
    BehindScenesSection,
    ProcessSection, ProcessStep,
    UpcomingSection, UpcomingProject, CastGroup,
    WhyChooseSection, WhyPoint,
    ContactSection, ContactService, ProjectEnquiry,
    FooterSection, FooterLink, FooterService, FooterSocial,
)


class SingletonAdmin(admin.ModelAdmin):
    """Only one record allowed (site settings, hero)."""
    def has_add_permission(self, request):
        return not self.model.objects.exists()


@admin.register(SiteSetting)
class SiteSettingAdmin(SingletonAdmin):
    list_display = ('site_name', 'tagline')
    readonly_fields = ('logo_preview', 'favicon_preview')
    fieldsets = (
        ('Branding', {'fields': ('site_name', 'tagline', 'logo', 'logo_preview', 'favicon', 'favicon_preview')}),
        ('Navbar Button', {'fields': ('nav_button_text', 'nav_button_link')}),
        ('Floating Buttons (Call & WhatsApp)', {
            'fields': ('phone_number', 'phone_icon', 'whatsapp_number', 'whatsapp_icon', 'whatsapp_message')
        }),
    )

    @admin.display(description='Logo preview')
    def logo_preview(self, obj):
        if obj and obj.logo:
            return format_html('<img src="{}" style="height:80px;width:80px;border-radius:50%;object-fit:cover;">', obj.logo.url)
        return 'No logo uploaded'

    @admin.display(description='Favicon preview')
    def favicon_preview(self, obj):
        if obj and obj.favicon:
            return format_html('<img src="{}" style="height:40px;">', obj.favicon.url)
        return 'No favicon uploaded'


@admin.register(NavMenuItem)
class NavMenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)


class HeroTagInline(admin.TabularInline):
    model = HeroTag
    extra = 1


@admin.register(HeroSection)
class HeroSectionAdmin(SingletonAdmin):
    list_display = ('__str__', 'heading_before', 'heading_italic', 'heading_after', 'is_active')
    readonly_fields = ('image_preview',)
    inlines = [HeroTagInline]
    fieldsets = (
        ('Heading', {'fields': ('eyebrow', 'heading_before', 'heading_italic', 'heading_after', 'description')}),
        ('Background Image', {'fields': ('background_image', 'image_preview')}),
        ('Buttons', {'fields': (
            'primary_button_text', 'primary_button_link',
            'secondary_button_text', 'secondary_button_link',
        )}),
        ('Status', {'fields': ('is_active',)}),
    )

    @admin.display(description='Image preview')
    def image_preview(self, obj):
        if obj and obj.background_image:
            return format_html('<img src="{}" style="height:120px;border-radius:8px;">', obj.background_image.url)
        return 'No image uploaded'
    


class MarqueeItemInline(admin.TabularInline):
    model = MarqueeItem
    extra = 1


@admin.register(MarqueeSetting)
class MarqueeSettingAdmin(SingletonAdmin):
    list_display = ('__str__', 'speed', 'is_active')
    inlines = [MarqueeItemInline]


@admin.register(AboutSection)
class AboutSectionAdmin(SingletonAdmin):
    list_display = ('__str__', 'heading_normal', 'heading_highlight', 'is_active')
    readonly_fields = ('main_preview', 'side_preview', 'bottom_preview')
    fieldsets = (
        ('Heading', {'fields': ('eyebrow', 'heading_normal', 'heading_highlight')}),
        ('Paragraphs', {'fields': ('paragraph_one', 'paragraph_two')}),
        ('Button', {'fields': ('button_text', 'button_link')}),
        ('Images', {'fields': (
            'image_main', 'main_preview',
            'image_side', 'side_preview',
            'image_bottom', 'bottom_preview',
        )}),
        ('Status', {'fields': ('is_active',)}),
    )

    def _preview(self, image):
        if image:
            return format_html('<img src="{}" style="height:110px;border-radius:6px;">', image.url)
        return 'No image uploaded'

    @admin.display(description='Main preview')
    def main_preview(self, obj):
        return self._preview(obj.image_main) if obj else '-'

    @admin.display(description='Side preview')
    def side_preview(self, obj):
        return self._preview(obj.image_side) if obj else '-'

    @admin.display(description='Bottom preview')
    def bottom_preview(self, obj):
        return self._preview(obj.image_bottom) if obj else '-'
    


class ServiceCardInline(admin.TabularInline):
    model = ServiceCard
    extra = 1
    fields = ('order', 'title', 'description', 'image', 'thumb', 'is_active')
    readonly_fields = ('thumb',)

    @admin.display(description='Preview')
    def thumb(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;">', obj.image.url)
        return '-'


@admin.register(ServicesSection)
class ServicesSectionAdmin(SingletonAdmin):
    list_display = ('__str__', 'eyebrow', 'heading', 'is_active')
    inlines = [ServiceCardInline]
    


@admin.register(ProjectsSection)
class ProjectsSectionAdmin(SingletonAdmin):
    list_display = ('__str__', 'eyebrow', 'heading', 'is_active')


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'title', 'category', 'order', 'has_video', 'is_active')
    list_display_links = ('thumb', 'title')
    list_editable = ('order', 'is_active')
    list_filter = ('category',)
    ordering = ('order',)

    @admin.display(description='Image')
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;">', obj.image.url)
        return '-'

    @admin.display(boolean=True, description='Video')
    def has_video(self, obj):
        return bool(obj.video_url)
    


@admin.register(BehindScenesSection)
class BehindScenesSectionAdmin(SingletonAdmin):
    list_display = ('__str__', 'heading_bold', 'heading_light', 'is_active')
    readonly_fields = ('lt_preview', 'lb_preview', 'c_preview', 'rt_preview', 'rb_preview')
    fieldsets = (
        ('Heading', {'fields': ('heading_bold', 'heading_light')}),
        ('Left column: top image', {'fields': ('left_top_image', 'lt_preview', 'left_top_caption')}),
        ('Left column: bottom image', {'fields': ('left_bottom_image', 'lb_preview', 'left_bottom_caption')}),
        ('Big centre image', {'fields': ('center_image', 'c_preview', 'center_title', 'center_subtitle')}),
        ('Right column: top image', {'fields': ('right_top_image', 'rt_preview', 'right_top_caption')}),
        ('Right column: bottom image', {'fields': ('right_bottom_image', 'rb_preview', 'right_bottom_caption')}),
        ('Status', {'fields': ('is_active',)}),
    )

    def _pv(self, image):
        if image:
            return format_html('<img src="{}" style="height:110px;border-radius:6px;">', image.url)
        return 'No image uploaded'

    @admin.display(description='Preview')
    def lt_preview(self, obj):
        return self._pv(obj.left_top_image) if obj else '-'

    @admin.display(description='Preview')
    def lb_preview(self, obj):
        return self._pv(obj.left_bottom_image) if obj else '-'

    @admin.display(description='Preview')
    def c_preview(self, obj):
        return self._pv(obj.center_image) if obj else '-'

    @admin.display(description='Preview')
    def rt_preview(self, obj):
        return self._pv(obj.right_top_image) if obj else '-'

    @admin.display(description='Preview')
    def rb_preview(self, obj):
        return self._pv(obj.right_bottom_image) if obj else '-'
    


class ProcessStepInline(admin.TabularInline):
    model = ProcessStep
    extra = 1
    fields = ('order', 'title', 'description', 'icon', 'is_active')


@admin.register(ProcessSection)
class ProcessSectionAdmin(SingletonAdmin):
    list_display = ('__str__', 'eyebrow', 'heading', 'is_active')
    inlines = [ProcessStepInline]
    


@admin.register(UpcomingSection)
class UpcomingSectionAdmin(SingletonAdmin):
    list_display = ('__str__', 'heading', 'is_active')


class CastGroupInline(admin.TabularInline):
    model = CastGroup
    extra = 1
    fields = ('order', 'label', 'names')


@admin.register(UpcomingProject)
class UpcomingProjectAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'title', 'release_date', 'release_status', 'order', 'is_active')
    list_display_links = ('thumb', 'title')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
    inlines = [CastGroupInline]

    @admin.display(description='Image')
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;">', obj.image.url)
        return '-'
    


class WhyPointInline(admin.TabularInline):
    model = WhyPoint
    extra = 1
    fields = ('order', 'title', 'description', 'is_active')


@admin.register(WhyChooseSection)
class WhyChooseSectionAdmin(SingletonAdmin):
    list_display = ('__str__', 'eyebrow', 'heading', 'is_active')
    readonly_fields = ('image_preview',)
    fieldsets = (
        ('Heading', {'fields': ('eyebrow', 'heading')}),
        ('Image', {'fields': ('image', 'image_preview')}),
        ('Status', {'fields': ('is_active',)}),
    )
    inlines = [WhyPointInline]

    @admin.display(description='Image preview')
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="height:140px;border-radius:6px;">', obj.image.url)
        return 'No image uploaded'
    
@admin.register(ContactSection)
class ContactSectionAdmin(SingletonAdmin):
    list_display = ('__str__', 'heading', 'phone_display', 'email', 'is_active')
    readonly_fields = ('bg_preview',)
    fieldsets = (
        ('Heading', {'fields': ('eyebrow', 'heading', 'subheading')}),
        ('Background Image', {'fields': ('background_image', 'bg_preview')}),
        ('Contact Details', {'fields': (
            'phone_icon', 'phone_label', 'phone_display', 'phone_number',
            'email_icon', 'email_label', 'email',
            'address_icon', 'address_label', 'address',
        )}),
        ('Map', {'fields': ('map_embed_url', 'map_link')}),
        ('Form Text', {'classes': ('collapse',), 'fields': (
            'f_name_label', 'f_name_placeholder',
            'f_phone_label', 'f_phone_placeholder',
            'f_email_label', 'f_email_placeholder',
            'f_service_label', 'f_service_placeholder',
            'f_details_label', 'f_details_placeholder',
            'button_text',
        )}),
        ('Where enquiries go (Email and WhatsApp)', {'fields': ('notify_email', 'whatsapp_number')}),
        ('Thank You Message', {'fields': ('success_title', 'success_message', 'success_button_text')}),
        ('Status', {'fields': ('is_active',)}),
    )

    @admin.display(description='Image preview')
    def bg_preview(self, obj):
        if obj and obj.background_image:
            return format_html('<img src="{}" style="height:120px;border-radius:8px;">', obj.background_image.url)
        return 'No image uploaded'


@admin.register(ContactService)
class ContactServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)


@admin.register(ProjectEnquiry)
class ProjectEnquiryAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'name', 'phone', 'email', 'service', 'email_sent', 'is_read')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'email_sent', 'service', 'created_at')
    search_fields = ('name', 'phone', 'email', 'details')
    date_hierarchy = 'created_at'
    readonly_fields = ('name', 'phone', 'email', 'service', 'details', 'created_at', 'email_sent')

    def has_add_permission(self, request):
        return False
    
class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1
    fields = ('order', 'title', 'link', 'is_active')


class FooterServiceInline(admin.TabularInline):
    model = FooterService
    extra = 1
    fields = ('order', 'title', 'link', 'is_active')


class FooterSocialInline(admin.TabularInline):
    model = FooterSocial
    extra = 1
    fields = ('order', 'name', 'icon', 'url', 'is_active')


@admin.register(FooterSection)
class FooterSectionAdmin(SingletonAdmin):
    list_display = ('__str__', 'brand_name', 'is_active')
    readonly_fields = ('logo_preview',)
    inlines = [FooterLinkInline, FooterServiceInline, FooterSocialInline]
    fieldsets = (
        ('Brand', {'fields': ('logo', 'logo_preview', 'brand_name', 'brand_tagline', 'description', 'follow_label')}),
        ('Column Titles', {'fields': ('navigate_title', 'services_title', 'contact_title')}),
        ('Contact Column (leave empty to use Contact Section)', {
            'fields': ('phone_display', 'phone_number', 'email', 'address', 'map_link')
        }),
        ('Bottom Bar', {'fields': ('copyright_text',)}),
        ('Status', {'fields': ('is_active',)}),
    )

    @admin.display(description='Logo preview')
    def logo_preview(self, obj):
        if obj and obj.logo:
            return format_html('<img src="{}" style="height:80px;width:80px;border-radius:50%;object-fit:cover;">', obj.logo.url)
        return 'No logo uploaded (Site Settings logo will be used)'