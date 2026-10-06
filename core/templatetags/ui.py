from django import template
register = template.Library()
ICONS = {'iot': '📡', 'robotics': '🤖', 'audio': '🎵', 'wearables': '⌚', 'camera': '📷', 'software': '💻',
         'ai': '🧠', 'events': '📅', 'news': '📰', 'home automation': '🏠', 'podcast': '🎙️',
         'test & measurement': '📈', 'development kits': '🧰', 'projects': '🔧', 'single board computers': '🖥️'}

@register.filter
def hue(text):
    return sum(ord(c) for c in str(text)) * 7 % 360

@register.filter
def icon(cat):
    return ICONS.get(str(cat).lower(), '⚡')


@register.filter
def initials(name):
    w = str(name).split()
    return (w[0][0] + (w[1][0] if len(w) > 1 else w[0][1:2])).upper() if w else ''
