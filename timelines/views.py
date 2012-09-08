from django.shortcuts import get_object_or_404, render_to_response

from datetime import datetime

from .models import Timeline, TimelineItem

def timeline_detail_json(request, pk, template='timelines/timeline_detail.json', **kwargs):
    '''
    We use a bit of custom code from our CMS to do some caching
    of the JSON response here.
    '''
    timeline = get_object_or_404(Timeline, pk=pk, is_live=True, pubdate__lte=current_time)
    timeline_items = timeline.timelineitem_set.all()
    try:
        timeline_start_date_format = timeline_items[0].verite_date_format
        timeline_start_date_display = timeline_items[0].verite_date_display
    except:
        timeline_start_date_format = None
        timeline_start_date_display = None

    datadict = {
        "timeline": timeline,
        "timeline_start_date_format": timeline_start_date_format,
        "timeline_start_date_display": timeline_start_date_display,
        "timeline_items" : timeline_items
    }

    return render_to_response(template, datadict, mimetype="application/json; charset=utf-8")

'''
TODO: drop in starter templates for these views

def timeline_list(request, template='timelines/timeline_list.html', **kwargs):
    timeline_list = Timeline.live_objects.all()

    return simple.direct_to_template(
        request,
        template = template,
        extra_context = {
            'request': request,
            'timeline_list': timeline_list,
        }
    )

def timeline_detail(request, slug, template='timelines/timeline_detail.html', **kwargs):
    timeline = get_object_or_404(Timeline, slug=slug, is_live=True, pubdate__lte=current_time)

    if timeline.custom_template:
        template = timeline.custom_template

    return simple.direct_to_template(
        request,
        template = template,
        extra_context = {
            'timeline': timeline,
        }
    )
'''