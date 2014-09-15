from django import forms
from django.contrib import admin

from .models import Timeline, TimelineItem

class TimelineItemForm(forms.ModelForm):
    '''
    For bonus points, you might want to add an AdminImageWidget like the one
    described here: http://djangosnippets.org/snippets/934/
    
    And then:

    photo = forms.ImageField(required=False, widget=AdminImageWidget())
    '''
    class Meta:
        model = TimelineItem

class TimelineItemInline(admin.StackedInline):
    model = TimelineItem
    extra = 1
    form = TimelineItemForm
    fieldsets = (
        (None, {'fields': (('date', 'date_display'), ('title', 'description'), 'photo', 'embed_link', ('media_credit', 'media_caption')),}),
    )

class TimelineAdmin(admin.ModelAdmin):
    save_on_top = True
    filter_horizontal = ('categories',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        TimelineItemInline,
    ]
    fieldsets = (
        (None, {'fields': (('pubdate', 'is_live'), ('name', 'slug'), 'description', ('teaser_photo', 'teaser_photo_credit'), 'teaser_photo_caption', 'categories', 'custom_template'),}),
    )
    
admin.site.register(Timeline, TimelineAdmin)
