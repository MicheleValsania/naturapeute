from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django.utils.html import format_html

from .models import Patient, Therapist, Symptom, Practice, Office, OfficePicture, Synonym, models


class OfficePictureInline(admin.TabularInline):
    model = OfficePicture
    exclude = ["uuid"]



@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    inlines = [OfficePictureInline]
    search_fields = ["therapist__firstname", "therapist__lastname", "city"]


class OfficeInline(admin.StackedInline):
    model = Office
    readonly_fields = ["country"]
    extra = 1


@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ["__str__", "image_tag", "agreements", "slug", "calendly_url"]
    list_filter = ["is_certified", "membership"]
    search_fields = ["firstname", "lastname", "slug", "calendly_url"]
    exclude = ["slug", "services", "invoice_data"]
    inlines = [OfficeInline]

    def image_tag(self, obj):
        return format_html(f'<img src="{obj.photo_url}" style="width: 45px; height:45px;" />')
    image_tag.short_description = 'Photo'

    # formfield_overrides = {
    #     models.ManyToManyField: {'widget': models.fields.forms.widgets.CheckboxSelectMultiple }
    # }


@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ["parent", "__str__"]
    list_display_links = ["__str__"]
    search_fields = ["name", "keywords"]


@admin.register(Synonym)
class SynonymAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ["__str__", "words"]


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass
