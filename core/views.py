from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm

ALT_LOGIN = ('Forgotten password? &nbsp;·&nbsp; Not a member yet? '
             '<a href="/register/">Create an account</a>')
ALT_REGISTER = 'Already a member? <a href="/login/">Sign in</a>'


def _home_ctx():
    return {'projects': Project.objects.select_related('platform')[:3], 'posts': Post.objects.all()[:3],
            'platforms': Platform.objects.all()[:6]}


def home(request):
    return render(request, 'home.html', _home_ctx())


class SignInView(LoginView):
    authentication_form = LoginForm
    template_name = 'home.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx.update(_home_ctx(), login_form=ctx['form'], open_modal='login')
        return ctx


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user, backend='core.backends.EmailBackend')
        return redirect('home')
    return render(request, 'home.html', {**_home_ctx(), 'register_form': form, 'open_modal': 'register'})


from django.core.paginator import Paginator
from django.db.models import Q

from .models import Platform, Post, Project

VIDEO_TITLES = {'potw': 'Product of the Week', 'educator': 'Electromaker Educator',
                'podcast': 'The Electromaker Podcast'}


def _listing(request, qs, title, filters, label, upload=False):
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q))
    fl = []
    for name, param, field, options in filters:
        value = request.GET.get(param, '')
        if value:
            qs = qs.filter(**{field: value})
        fl.append({'label': name, 'name': param, 'options': options, 'value': value})
    page = Paginator(qs, 9).get_page(request.GET.get('page'))
    rest = request.GET.copy()
    rest.pop('page', None)
    return render(request, 'listing.html', {
        'title': title, 'filters': fl, 'label': label, 'upload': upload, 'q': q, 'page': page,
        'pages': list(page.paginator.get_elided_page_range(page.number, on_each_side=1, on_ends=1)),
        'rest': rest.urlencode()})


def _distinct(model, field):
    return model.objects.order_by(field).values_list(field, flat=True).distinct()


def platforms(request):
    return render(request, 'platforms.html', {'platforms': Platform.objects.all()})


def projects(request):
    filters = [('Category', 'category', 'category', _distinct(Project, 'category')),
               ('Difficulty', 'difficulty', 'difficulty', [d for d, _ in Project.DIFFICULTY]),
               ('Platform', 'platform', 'platform__name', Platform.objects.values_list('name', flat=True))]
    return _listing(request, Project.objects.select_related('platform'), 'Project Hub', filters,
                    'project hub', upload=True)


def blog(request):
    filters = [('Category', 'category', 'category', _distinct(Post, 'category')),
               ('Platform', 'platform', 'platform__name', Platform.objects.values_list('name', flat=True)),
               ('Type', 'type', 'kind', _distinct(Post, 'kind'))]
    return _listing(request, Post.objects.select_related('platform'), 'Blog', filters, 'blogs')


def videos(request, tag=None):
    qs = Post.objects.filter(tag=tag) if tag else Post.objects.exclude(tag='')
    filters = [('Platform', 'platform', 'platform__name', Platform.objects.values_list('name', flat=True))]
    return _listing(request, qs.select_related('platform'), VIDEO_TITLES.get(tag, 'Videos'), filters, 'videos')


import random
import textwrap
from xml.sax.saxutils import escape

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404

from .templatetags.ui import hue, icon, initials


PCB = '#0f7a4f'


def _bg(h, w, hh, rnd):
    """Fondo con degradado y pistas de circuito."""
    out = (f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="hsl({h},55%,16%)"/>'
           f'<stop offset="1" stop-color="hsl({(h + 50) % 360},60%,34%)"/></linearGradient></defs>'
           f'<rect width="{w}" height="{hh}" fill="url(#g)"/>')
    for _ in range(10):
        x, y = rnd.randrange(0, w, 20), rnd.randrange(0, hh, 20)
        x2, y2 = x + rnd.choice([40, 80, 120]), y + rnd.choice([-40, 0, 40])
        out += (f'<polyline points="{x},{y} {x2},{y} {x2},{y2}" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="3"/>'
                f'<circle cx="{x2}" cy="{y2}" r="4" fill="#1ee494" fill-opacity=".55"/>')
    return out


def _chip(x, y, w, h, label='', fill='#222'):
    pins = ''.join(f'<rect x="{x - 7}" y="{y + 8 + i * 12}" width="7" height="5" fill="#d9c27a"/>'
                   f'<rect x="{x + w}" y="{y + 8 + i * 12}" width="7" height="5" fill="#d9c27a"/>'
                   for i in range(max(2, int((h - 10) // 12))))
    return (pins + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="#555"/>'
            f'<text x="{x + w / 2}" y="{y + h / 2 + 4}" font-size="11" fill="#9fe" text-anchor="middle" font-family="monospace">{label}</text>')


def _scene(cat):
    c = cat.lower()
    if c == 'ai':
        return (_chip(140, 60, 120, 100, 'AI', '#14202b') +
                '<circle cx="200" cy="110" r="46" fill="none" stroke="#1ee494" stroke-width="3" stroke-dasharray="6 5"/>'
                '')
    if c == 'robotics':
        return ('<rect x="150" y="50" width="100" height="84" rx="14" fill="#dfe8ef"/><circle cx="178" cy="88" r="13" fill="#10365d"/>'
                '<circle cx="222" cy="88" r="13" fill="#10365d"/><circle cx="178" cy="88" r="5" fill="#1ee494"/><circle cx="222" cy="88" r="5" fill="#1ee494"/>'
                '<rect x="180" y="112" width="40" height="8" rx="3" fill="#10365d"/><line x1="200" y1="50" x2="200" y2="30" stroke="#dfe8ef" stroke-width="4"/>'
                '<circle cx="200" cy="26" r="6" fill="#ef5b5b"/><rect x="165" y="140" width="70" height="34" rx="8" fill="#b8c7d4"/>')
    if c == 'audio':
        bars = ''.join(f'<rect x="{110 + i * 14}" y="{110 - h}" width="8" height="{2 * h}" rx="3" fill="#1ee494"/>'
                       for i, h in enumerate([10, 24, 40, 28, 52, 34, 20, 44, 30, 16, 8]))
        return bars + '<circle cx="330" cy="70" r="26" fill="#ffd900" stroke="#e7bd00" stroke-width="6"/><line x1="330" y1="70" x2="338" y2="52" stroke="#222" stroke-width="3"/>'
    if c == 'wearables':
        return ('<rect x="180" y="20" width="40" height="40" fill="#222"/><rect x="180" y="160" width="40" height="40" fill="#222"/>'
                '<rect x="150" y="56" width="100" height="108" rx="24" fill="#111" stroke="#9aa" stroke-width="4"/>'
                '<circle cx="200" cy="110" r="34" fill="none" stroke="#1ee494" stroke-width="3"/><line x1="200" y1="110" x2="200" y2="88" stroke="#fff" stroke-width="3"/>'
                '<line x1="200" y1="110" x2="216" y2="118" stroke="#fff" stroke-width="3"/>')
    if c == 'camera':
        return ('<rect x="130" y="60" width="140" height="100" rx="12" fill="#1c1c1c" stroke="#777" stroke-width="3"/><rect x="170" y="48" width="50" height="16" rx="4" fill="#333"/>'
                '<circle cx="200" cy="110" r="36" fill="#0b2a44" stroke="#aaa" stroke-width="5"/><circle cx="200" cy="110" r="18" fill="#1b6fa8"/>'
                '<circle cx="190" cy="100" r="5" fill="#fff" fill-opacity=".7"/><circle cx="252" cy="76" r="4" fill="#ef5b5b"/>')
    if c == 'home automation':
        return ('<polygon points="130,110 200,50 270,110" fill="#e8eef3"/><rect x="144" y="110" width="112" height="60" fill="#c9d6e0"/>'
                '<rect x="188" y="130" width="24" height="40" fill="#10365d"/><circle cx="200" cy="40" r="0"/>'
                '<circle cx="300" cy="60" r="16" fill="#ffd900"/><rect x="293" y="76" width="14" height="10" fill="#aaa"/>')
    if c == 'test & measurement':
        return ('<rect x="110" y="40" width="180" height="130" rx="8" fill="#20262c" stroke="#6b7a86" stroke-width="3"/>'
                '<rect x="122" y="52" width="156" height="90" fill="#04120c"/>'
                '<polyline points="122,97 146,60 170,134 194,60 218,134 242,60 266,134 278,97" fill="none" stroke="#1ee494" stroke-width="3"/>'
                '<circle cx="140" cy="157" r="7" fill="#aaa"/><circle cx="170" cy="157" r="7" fill="#aaa"/><circle cx="260" cy="157" r="7" fill="#ffd900"/>')
    if c == 'software':
        return ('<rect x="100" y="40" width="200" height="130" rx="8" fill="#10151b" stroke="#6b7a86" stroke-width="2"/><rect x="100" y="40" width="200" height="20" rx="8" fill="#26303a"/>'
                '<circle cx="114" cy="50" r="4" fill="#ef5b5b"/><circle cx="128" cy="50" r="4" fill="#ffd900"/><circle cx="142" cy="50" r="4" fill="#1ee494"/>'
                '<text x="114" y="86" font-size="13" fill="#1ee494" font-family="monospace">$ boot esp32-s3</text><text x="114" y="108" font-size="13" fill="#cfe" font-family="monospace">Linux 7.2 ready_</text>'
                '<text x="114" y="130" font-size="13" fill="#9ab" font-family="monospace">wifi: connected</text>')
    if c in ('events', 'news'):
        return ('<rect x="125" y="45" width="150" height="130" rx="10" fill="#f3f6f9"/><rect x="125" y="45" width="150" height="32" rx="10" fill="#ef5b5b"/>'
                '<rect x="150" y="34" width="8" height="22" rx="3" fill="#333"/><rect x="242" y="34" width="8" height="22" rx="3" fill="#333"/>'
                '<text x="200" y="145" font-size="52" font-weight="700" fill="#10365d" text-anchor="middle" font-family="Trebuchet MS,Arial">23</text>')
    if c == 'podcast':
        return ('<rect x="180" y="40" width="40" height="80" rx="20" fill="#dfe8ef"/><path d="M158 100 a42 42 0 0 0 84 0" fill="none" stroke="#dfe8ef" stroke-width="5"/>'
                '<line x1="200" y1="142" x2="200" y2="170" stroke="#dfe8ef" stroke-width="5"/><line x1="176" y1="170" x2="224" y2="170" stroke="#dfe8ef" stroke-width="5"/>'
                '<path d="M120 80 a24 24 0 0 0 0 40 M280 80 a24 24 0 0 1 0 40" fill="none" stroke="#1ee494" stroke-width="4"/>')
    if c == 'iot':
        return (f'<rect x="130" y="90" width="140" height="80" rx="8" fill="{PCB}" stroke="#7fd" stroke-width="2"/>' + _chip(166, 108, 50, 44, 'ESP', '#222') +
                '<circle cx="250" cy="130" r="8" fill="#ffd900"/>'
                '<path d="M160 76 a60 60 0 0 1 80 0 M175 62 a38 38 0 0 1 50 0 M188 48 a18 18 0 0 1 24 0" fill="none" stroke="#1ee494" stroke-width="4" stroke-linecap="round"/>')
    # placas / kits / proyectos / SBC
    pins = ''.join(f'<rect x="{138 + i * 10}" y="52" width="6" height="12" fill="#222"/>' for i in range(11))
    return (f'<rect x="120" y="60" width="160" height="110" rx="8" fill="{PCB}" stroke="#7fd" stroke-width="2"/>' + pins +
            _chip(150, 84, 60, 50, 'MCU', '#1d1d1d') + '<rect x="228" y="90" width="38" height="26" fill="#cfd8dc" stroke="#889"/>'
            '<circle cx="136" cy="156" r="5" fill="#d9c27a"/><circle cx="264" cy="156" r="5" fill="#d9c27a"/>'
            '<circle cx="236" cy="146" r="6" fill="#ef5b5b"/><circle cx="252" cy="146" r="6" fill="#1ee494"/>')


PLATFORM_GLYPHS = {
    'chip': ('Espressif', 'Microchip', 'Infineon Technologies', 'Nordic Semiconductor', 'STMicroelectronics', 'Texas Instruments', 'NVIDIA'),
    'cloud': ('Amazon Alexa', 'Balena', 'Blues', 'Particle', 'Google'),
    'phone': ('Android',),
    'robot': ('Elephant Robotics', 'DFRobot'),
}


def _platform_svg(o):
    h = hue(o.name)
    kind = next((k for k, v in PLATFORM_GLYPHS.items() if o.name in v), 'board')
    g = {
        'chip': '<rect x="64" y="46" width="72" height="72" rx="8" fill="#fff" fill-opacity=".92"/><rect x="82" y="64" width="36" height="36" rx="4" fill="hsl(%d,55%%,30%%)"/>' % h +
                ''.join(f'<rect x="{72 + i * 20}" y="34" width="6" height="12" fill="#fff"/><rect x="{72 + i * 20}" y="118" width="6" height="12" fill="#fff"/>' for i in range(3)),
        'cloud': '<path d="M62 118 a24 24 0 0 1 4-48 a34 34 0 0 1 66 8 a20 20 0 0 1 2 40 z" fill="#fff" fill-opacity=".92"/>',
        'phone': '<rect x="76" y="34" width="48" height="90" rx="10" fill="#fff" fill-opacity=".92"/><circle cx="100" cy="112" r="5" fill="hsl(%d,55%%,30%%)"/>' % h,
        'robot': '<rect x="66" y="52" width="68" height="56" rx="12" fill="#fff" fill-opacity=".92"/><circle cx="86" cy="80" r="8" fill="hsl(%d,55%%,30%%)"/><circle cx="114" cy="80" r="8" fill="hsl(%d,55%%,30%%)"/><line x1="100" y1="52" x2="100" y2="36" stroke="#fff" stroke-width="4"/>' % (h, h),
        'board': '<rect x="56" y="54" width="88" height="62" rx="8" fill="#fff" fill-opacity=".92"/><rect x="72" y="68" width="30" height="30" rx="3" fill="hsl(%d,55%%,30%%)"/><circle cx="124" cy="72" r="5" fill="hsl(%d,55%%,30%%)"/><circle cx="124" cy="92" r="5" fill="hsl(%d,55%%,30%%)"/>' % (h, h, h),
    }[kind]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><rect width="200" height="200" rx="26" fill="hsl({h},55%,35%)"/>'
            f'<g transform="translate(100,100) scale(1.35) translate(-100,-82)">{g}</g></svg>')


def thumb(request, kind, pk):
    """Ilustración SVG generada al vuelo para proyectos, entradas y plataformas."""
    if kind == 'platform':
        svg = _platform_svg(get_object_or_404(Platform, pk=pk))
    else:
        o = get_object_or_404({'post': Post, 'project': Project}.get(kind) or Http404, pk=pk)
        h, rnd = hue(o.title), random.Random(pk * 31 + len(o.title))
        tag = 'electro<tspan fill="#1ee494" font-weight="700">BLOG</tspan>' if kind == 'post' else escape(o.difficulty.upper())
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240">{_bg(h, 400, 240, rnd)}'
               f'<g transform="translate(0,10)">{_scene(o.category)}</g>'
               f'<text x="34" y="30" font-size="12" letter-spacing="2" fill="#fff" fill-opacity=".8" font-family="Trebuchet MS,Arial">{escape(o.category.upper())}</text>'
               f'<text x="366" y="222" font-size="14" fill="#fff" text-anchor="end" font-family="Trebuchet MS,Arial">{tag}</text></svg>')
    return HttpResponse(svg, content_type='image/svg+xml', headers={'Cache-Control': 'max-age=3600'})
