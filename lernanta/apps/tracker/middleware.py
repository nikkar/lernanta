import datetime
import fnmatch
import logging

from django.conf import settings

from tracker import utils
from tracker.models import PageView

log = logging.getLogger(__name__)


class PageViewTrackerMiddleware:
    def process_request(self, request):
<<<<<<< HEAD
        BotNames = ['Googlebot','Slurp','Twiceler','msnbot','KaloogaBot','YodaoBot','"Baiduspider','googlebot','Speedy Spider','DotBot']
        user_agent = request.META.get('HTTP_USER_AGENT', None)
        
        # makes automated tests work
        if not user_agent:
            return

        # ensure that the request.path begins with any of the prefixes
        for prefix in settings.TRACKING_PREFIXES:
            for botname in BotNames:
                if botname in user_agent:
                    # do not save the page view if the visitor is a known bot
                    return
                if fnmatch.fnmatch(request.path, prefix):
                    ip_address = utils.get_ip(request)
                    pageview = PageView()
                    pageview.session_key = request.session.session_key
                    pageview.ip_address = ip_address
                    pageview.request_url = request.path
                    pageview.referrer_url = utils.u_clean(request.META.get('HTTP_REFERER', 'unknown')[:255])
                    pageview.user_agent = user_agent

                    try:
                        oldpageview = PageView.objects.filter(session_key=request.session.session_key).order_by('-access_time')[0]
                    except IndexError, error:
                        pass
                    else:
                        time_on_page = (datetime.datetime.now() - oldpageview.access_time)
                        if time_on_page.seconds < 3600 and time_on_page.days == 0:
                            oldpageview.time_on_page = time_on_page.seconds
                            oldpageview.save()

=======
        BotNames=['Googlebot','Slurp','Twiceler','msnbot','KaloogaBot','YodaoBot','"Baiduspider','googlebot','Speedy Spider','DotBot']
        user_agent=request.META.get('HTTP_USER_AGENT', None)
        for botname in BotNames:
            if botname in user_agent:
                # do not save the page view if the visitor is a known bot
                return
        
        # ensure that the request.path begins with any of the prefixes
        for prefix in settings.TRACKING_PREFIXES:
            if fnmatch.fnmatch(request.path, prefix):
                ip_address = utils.get_ip(request)
                pageview = PageView()
                pageview.session_key = request.session.session_key
                pageview.ip_address = ip_address
                pageview.request_url = request.path
                pageview.referrer_url = utils.u_clean(request.META.get('HTTP_REFERER', 'unknown')[:255])
                try:
                    oldpageview = PageView.objects.filter(session_key=request.session.session_key).order_by('-access_time')[0]
                except IndexError, error:
                    pass
>>>>>>> p2pu/master
                else:
                    time_on_page = (datetime.datetime.now() - oldpageview.access_time)
                    if time_on_page.seconds < 3600 and time_on_page.days == 0:
                        oldpageview.time_on_page = time_on_page.seconds
                        oldpageview.save()
                break
        else:
            # it did not find any matching prefixes.
            return

        if request.user.is_authenticated():
            now = datetime.datetime.now()
            profile = request.user.get_profile()
            pageview.user = request.user
            try:
                profile.last_active = now
                profile.save()
            except Exception, error:
                logging.error('An error occurred saving user record: %s' % error)

        try:
            pageview.save()
        except Exception, error:
            logging.error('An error occurred saving pageview record: %s' % error)
