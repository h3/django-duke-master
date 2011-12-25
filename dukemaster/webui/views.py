"""
sentry.web.views
~~~~~~~~~~~~~~~~

:copyright: (c) 2010 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import base64
import datetime
import logging
import re
import time
import warnings
import zlib

from django.conf import settings as dj_settings
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseForbidden, HttpResponseRedirect, Http404, HttpResponseNotModified, \
    HttpResponseGone
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods

from dukemaster.conf import settings
from sentry.utils import get_filters, is_float, get_signature, parse_auth_header, json
from sentry.utils.compat import pickle
from sentry.utils.stacks import get_template_info

@csrf_exempt
@require_http_methods(['POST'])
def store(request):
#    if request.META.get('HTTP_AUTHORIZATION', '').startswith('Dukemaster'):
#        auth_vars = parse_auth_header(request.META['HTTP_AUTHORIZATION'])
#
#        signature = auth_vars.get('duke_signature')
#        timestamp = auth_vars.get('duke_timestamp')
#
#        format = 'json'
#
#        data = request.raw_post_data
#
#        # Signed data packet
#        if signature and timestamp:
#            try:
#                timestamp = float(timestamp)
#            except ValueError:
#                return HttpResponseBadRequest('Invalid timestamp')
#
#            if timestamp < time.time() - 3600: # 1 hour
#                return HttpResponseGone('Message has expired')
#
#            sig_hmac = get_signature(data, timestamp)
#            if sig_hmac != signature:
#                return HttpResponseForbidden('Invalid signature')
#        else:
#            return HttpResponse('Unauthorized', status_code=401)
#    else:
#        # Legacy request (deprecated as of 2.0)
#        key = request.POST.get('key')
#
#        if not key:
#            return HttpResponseForbidden('Invalid credentials')
#
#        if key != settings.KEY:
#           #warnings.warn('A client is sending the `key` parameter, which will be removed in Sentry 2.0', DeprecationWarning)
#            return HttpResponseForbidden('Invalid credentials')
#
#        data = request.POST.get('data')
#        if not data:
#            return HttpResponseBadRequest('Missing data')
#
#        format = request.POST.get('format', 'pickle')
#
#        if format not in ('pickle', 'json'):
#            return HttpResponseBadRequest('Invalid format')
#
#    logger = logging.getLogger('sentry.server')
#
#    try:
#        try:
#            data = base64.b64decode(data).decode('zlib')
#        except zlib.error:
#            data = base64.b64decode(data)
#    except Exception, e:
#        # This error should be caught as it suggests that there's a
#        # bug somewhere in the client's code.
#        logger.exception('Bad data received')
#        return HttpResponseForbidden('Bad data decoding request (%s, %s)' % (e.__class__.__name__, e))
#
#    try:
#        if format == 'pickle':
#            data = pickle.loads(data)
#        elif format == 'json':
#            data = json.loads(data)
#    except Exception, e:
#        # This error should be caught as it suggests that there's a
#        # bug somewhere in the client's code.
#        logger.exception('Bad data received')
#        return HttpResponseForbidden('Bad data reconstructing object (%s, %s)' % (e.__class__.__name__, e))
#
#    # XXX: ensure keys are coerced to strings
#    data = dict((smart_str(k), v) for k, v in data.iteritems())
#
#    if 'timestamp' in data:
#        if is_float(data['timestamp']):
#            try:
#                data['timestamp'] = datetime.datetime.fromtimestamp(float(data['timestamp']))
#            except:
#                logger.exception('Failed reading timestamp')
#                del data['timestamp']
#        elif not isinstance(data['timestamp'], datetime.datetime):
#            if '.' in data['timestamp']:
#                format = '%Y-%m-%dT%H:%M:%S.%f'
#            else:
#                format = '%Y-%m-%dT%H:%M:%S'
#            if 'Z' in data['timestamp']:
#                # support GMT market, but not other timestamps
#                format += 'Z'
#            try:
#                data['timestamp'] = datetime.datetime.strptime(data['timestamp'], format)
#            except:
#                logger.exception('Failed reading timestamp')
#                del data['timestamp']
#
#    GroupedMessage.objects.from_kwargs(**data)
#
    return HttpResponse()
