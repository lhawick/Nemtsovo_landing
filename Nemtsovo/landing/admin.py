from django.urls import reverse
from django.utils.html import format_html
from .models import *
from django.contrib.contenttypes.admin import GenericTabularInline
from django.forms import TextInput
from adminsortable2.admin import SortableAdminBase, SortableGenericInlineAdminMixin, SortableAdminMixin
from image_cropping import ImageCroppingMixin


class AttachmentInline(ImageCroppingMixin, SortableGenericInlineAdminMixin, GenericTabularInline):
    model = Attachment
    extra = 5


@admin.register(House)
class HouseAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "start_price", 'order')
    inlines = [AttachmentInline]
    search_fields = ("name", "description", "start_price")
    save_on_top = True


class AdditionalInfoItemInline(admin.StackedInline):
    model = AdditionalInfoItem
    extra = 5
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 200})}
    }


@admin.register(AdditionalInfo)
class AdditionalInfoAdmin(admin.ModelAdmin):
    list_display = ("inner_name", "displayed_name")
    search_fields = ("inner_name", 'displayed_name')
    inlines = [AdditionalInfoItemInline]
    save_on_top = True


@admin.register(WellnessTreatment)
class WellnessTreatmentAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "start_price", 'order')
    inlines = [AttachmentInline]
    search_fields = ("name", "description", "start_price")
    save_on_top = True


@admin.register(Action)
class ActionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("name", 'get_price_or_display_free', 'order')
    inlines = [AttachmentInline]
    search_fields = ("name", "description", "start_price")
    save_on_top = True

    @admin.display(description='Начальная цена')
    def get_price_or_display_free(self, obj):
        return obj.start_price if obj.start_price > 0 else "Бесплатно"


@admin.register(OurProduct)
class OurProductAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ("name", "price", "is_available")
    inlines = [AttachmentInline]
    list_filter = ("is_available",)
    search_fields = ('name', 'description', 'price')
    save_on_top = True
    list_editable = ('is_available',)


@admin.register(Event)
class EventAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ("title", "date", 'is_passed')
    inlines = [AttachmentInline]
    list_filter = ["date"]
    ordering = ['-date']
    save_on_top = True
    search_fields = ("title", "description")

    readonly_fields=["public_link"]

    def public_link(self, obj):
        if not obj.pk:
            return "Сохраните объект, чтобы увидеть ссылку"

        url = reverse("events") + f"#event_{obj.pk}"
        return format_html('<a href="{}" target="_blank">{}</a>', url, url)
    
    public_link.short_description = "Ссылка на мероприятие"


@admin.register(News)
class NewsAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ("title", "date")
    inlines = [AttachmentInline]
    list_filter = ["date"]
    ordering = ['-date']
    save_on_top = True
    search_fields = ("title", "description")

    readonly_fields=["public_link"]

    def public_link(self, obj):
        if not obj.pk:
            return "Сохраните объект, чтобы увидеть ссылку"

        url = reverse("news") + f"?news_item={obj.pk}"
        return format_html('<a href="{}" target="_blank">{}</a>', url, url)
    
    public_link.short_description = "Ссылка на новость"


@admin.action(description="Подтвердить выбранные Заявки на бронирование")
def make_approved(model_admin, request, queryset):
    queryset.update(status='b')


@admin.action(description="Закрыть выбранные Заявки на бронирование")
def make_canceled(model_admin, request, queryset):
    queryset.update(status='c')


@admin.action(description="Сделать активными выбранные Заявки на бронирование")
def make_active(model_admin, request, queryset):
    queryset.update(status='a')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('get_booking_name', "fio", 'phone_number', 'desired_dates', 'date_start_fact',
                    'date_end_fact', 'early_late_check', 'status', 'date_create')
    list_editable = ['status']
    readonly_fields = (
        'fio', 'phone_number', 'adults_count', 'childs_count', 'desired_dates', 'is_has_whatsapp', 'date_create',
        'user_comment')
    list_filter = ['status', 'date_create', 'date_start_fact', 'date_end_fact']
    ordering = ['status', '-date_create']
    save_on_top = True
    list_per_page = 10
    actions = [make_approved, make_canceled, make_active]
    exclude = ['is_dayly']
    fieldsets = [
        (
            "Информация из формы бронирования",
            {
                'fields': ['fio', 'phone_number', 'adults_count', 'childs_count', 'desired_dates',
                           'is_early_checkin', 'is_late_checkout', 'is_has_whatsapp', 'date_create', 'user_comment']
            }
        ),
        (
            'Редактирование заявки',
            {
                'fields': ['status', 'date_start_fact', 'date_end_fact']
            }
        )
    ]

    def get_row_css(self, obj, index):
        if obj.status == 'a':
            return 'red red%d' % index
        return ''

    @admin.display(description="Название")
    def get_booking_name(self, obj):
        name = obj.booking_identifier.name

        if obj.is_dayly:
            name += ' (посуточно)'

        return name

    @admin.display(description="Ранний заезд/Поздний выезд")
    def early_late_check(self, obj):
        text = []

        if obj.is_early_checkin:
            text.append("Ранний заезд")
        if obj.is_late_checkout:
            text.append("Поздний выезд")

        return "/".join(text)


@admin.register(OurPet)
class OurPetAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'order')
    inlines = [AttachmentInline]


@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('error_message', 'date', 'is_solved')
    list_filter = ('is_solved', 'date')
    list_editable = ['is_solved']
    readonly_fields = ('error_message', 'stack_trace', 'date', 'additional_info')
    def has_add_permission(self, request):
        return False

@admin.register(PromoBanner)
class PromoBannerAdmin(admin.ModelAdmin):
    readonly_fields = ["image_preview"]
    fields = ("name", "image_preview", "image", "start_at", "end_at", "is_active", "link")
    list_display = ("image_preview", "name", "start_at", "end_at", 'is_active')

    def image_preview(self, obj):
        if not obj or not obj.image:
            return "Нет изображения"
        return format_html(
            '<img src="{}" style="max-height: 150px; max-width: 100%;" />',
            obj.image.url,
        )
    
    image_preview.short_description = 'Предпросмотр'


admin.site.register(BookingIdentifier)
admin.site.register(Period)
