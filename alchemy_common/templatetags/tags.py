import socket
import re

from django import template
from hashlib import md5

register = template.Library()


@register.simple_tag
def test():
    return "Success"


@register.simple_tag
def hostname():
    return socket.gethostname()


@register.simple_tag
def build_number():
    return 1


@register.simple_tag
def has_view_perm_for_url(user, url):
    try:
        m = re.search('admin/([A-z_]+)/([A-z_]+)(/([A-z_]+))?/?', url)
        app_name = m.groups()[0]
        model_name = m.groups()[1]
        action_name = m.groups()[3]

        if not action_name:
            action_name = 'view'

        if user.has_perm('{}.{}_{}'.format(app_name, action_name, model_name)):
            return True
    except Exception as error:
        print(error)
        return False
    return False


@register.filter(name='gravatar')
def gravatar(user, size=35):
    if user.is_authenticated:
        email = str(user.email.strip().lower()).encode('utf-8')
        email_hash = md5(email).hexdigest()
        url = "//www.gravatar.com/avatar/{0}?s={1}&d=identicon&r=PG"
        return url.format(email_hash, size)
    return ""


@register.simple_tag
def get_quota_messages():
    messages = []

    return messages
