from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify, striptags, date as dj_date, time as dj_time

from datetime import datetime

current_time = datetime.now

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        ordering = ['name',]
        verbose_name = 'Timeline Category'
        verbose_name_plural = 'Timeline Categories'

    def __unicode__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        self.slug = slugify("%s" % (self.name))
        super(Category, self).save(*args, **kwargs)


class LiveTimelineManager(models.Manager):
    def get_query_set(self):
        qs = super(LiveTimelineManager, self).get_query_set()
        return qs.filter(is_live__exact=True, pubdate__lte=current_time)


class Timeline(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    categories = models.ManyToManyField(Category)
    teaser_photo = models.ImageField(upload_to="timeline_images", blank=True, null=True, help_text="Thumbnail image for lists and teasers.")
    teaser_photo_credit = models.CharField(max_length=255, blank=True)
    teaser_photo_caption = models.TextField(blank=True)
    description = models.TextField()
    pubdate = models.DateTimeField(default=datetime.now, help_text="Page will not be shown until after this date and time.")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_live = models.BooleanField(default=True)
    custom_template = models.CharField(max_length=255, blank=True, null=True, help_text="Custom template to override default.")
    objects = models.Manager()
    live_objects = LiveTimelineManager()

    class Meta:
        ordering = ['-pubdate',]

    def __unicode__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        self.slug = slugify("%s" % (self.name))
        super(Timeline, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('timeline_detail', (), { 'slug' : self.slug })


# Extra flexibility in date display; requires modified timeline.js
DATE_DISPLAY_CHOICES = (
    (1, 'Year only'),
    (2, 'Month/Year'),
    (3, 'Month/Day/Year'),
)

# Because maybe we want to add a "show only top items" feature?
SIGNIFICANCE_CHOICES = (
    (1, 'High'),
    (2, 'Normal'),
)

class TimelineItem(models.Model):
    timeline = models.ForeignKey(Timeline, null=True)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    date_display = models.IntegerField(choices=DATE_DISPLAY_CHOICES, default=3)
    title = models.CharField(max_length=255, blank=True, help_text="Optional headline for this item.")
    description = models.TextField(help_text="To remove a timeline item, delete its description.")
    photo = models.ImageField(upload_to="timeline_images", blank=True, null=True)
    embed_link = models.CharField(max_length=255, blank=True, help_text="Instead of a photo, you can paste in a link to a YouTube or Vimeo video, a Tweet, a Flickr photo, or a SoundCloud song.")
    media_credit = models.CharField(max_length=255, blank=True)
    media_caption = models.TextField(blank=True)
    significance = models.IntegerField(choices=SIGNIFICANCE_CHOICES, default=2, help_text="Relative importance of this event within the timeline.")

    class Meta:
        ordering = ['date',]

    def __unicode__(self):
        return u'%s: %s' % (self.date, self.title)

    @property
    def verite_date_format(self):
        if self.time:
            return '%s,%s,%s,%s,%s,%s' % (self.date.year, self.date.month, self.date.day, self.time.hour, self.time.minute, self.time.second)
        return '%s,%s,%s' % (self.date.year, self.date.month, self.date.day)

    @property
    def verite_date_display(self):
        if self.date_display == 1:
            return dj_date(self.date,"Y")
        if self.date_display == 2:
            return dj_date(self.date,"F Y")
        if self.date_display == 3:
            return dj_date(self.date,"F j, Y")
