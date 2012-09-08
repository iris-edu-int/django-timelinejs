django-timelinejs
=================

A Django app for feeding data into a [TimelineJS](http://timeline.verite.co/) presentation.

TimelineJS has built-in support for pulling information from GoogleDocs, but we like to keep our data in-house when possible. Because we have reporters and editors who are already familiar with our own CMS, it made sense to build a simple tool for the newsroom to create timelines right in the web admin, complete with photo uploads and customizable date formatting.

This is a slightly modified version of the app we use at The Spokesman-Review to produce [timelines like this](http://www.spokesman.com/timelines/standoff-ruby-ridge/).



Notes
-----

By default, TimelineJS will take a date like "August 1, 2012" and display it as "August 2012." This is handy if you want an quick way to add a timeline item that's specific only to the month, but not if you have timeline items that actually *do* take place on the 1st and you want to display them as such.

So we hacked a little bit on the javascript to allow for custom date formats; this repo includes our `customdates` version of TimelineJS. Using it allows you to set the `date_display` attribute for any TimelineItem to "Year only," "Month/Year," or "Month/Day/Year." But also note that this `customdates` version is several weeks behind official TimelineJS development.



Usage
-----

Add `timelines` to your INSTALLED_APPS and create tables via `syncdb` or South. Then visit the Django admin to whip up a test timeline. The Timeline form takes basic details at the top, and lets you add any number of TimelineItems as inlines below.

Hitting the `timeline_detail_json` URL will generate JSON in a format that TimelineJS expects.

On a public-facing template, include javascript on your page like so:

    <script type="text/javascript" src="js/timeline.customdates.min.js"></script>

And give the timeline a div to live in:

    <div id="timeline"></div>
    <script type="text/javascript">
        $(document).ready(function() {
            var timeline = new VMM.Timeline();
            timeline.init("{% url 'timeline_detail_json' timeline.pk %}");
        });
    </script>



To Do
-----

* Add some starter list and detail templates to this repo. We didn't figure people would want all our HTML and CSS, but we should be able to add some sensible defaults here.
* Update the `customdates` javascript to catch up to new features in the TimelineJS development version.