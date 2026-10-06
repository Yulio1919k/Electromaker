from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

DATOS = {'username': 'ana', 'email': 'Ana@Mail.com', 'password1': 'Clave-segura-91',
         'password2': 'Clave-segura-91', 'newsletter': 'no'}


class AuthTests(TestCase):
    def test_paginas_cargan(self):
        for name in ('home', 'login', 'register'):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_registro_e_inicio_con_correo(self):
        self.assertRedirects(self.client.post(reverse('register'), DATOS), reverse('home'))
        self.assertTrue(get_user_model().objects.filter(email='ana@mail.com').exists())
        self.client.post(reverse('logout'))
        r = self.client.post(reverse('login'), {'username': 'ANA@mail.com', 'password': 'Clave-segura-91'})
        self.assertRedirects(r, reverse('home'))

    def test_clave_incorrecta(self):
        self.client.post(reverse('register'), DATOS)
        self.client.post(reverse('logout'))
        r = self.client.post(reverse('login'), {'username': 'ana@mail.com', 'password': 'mala'})
        self.assertEqual(r.status_code, 200)

    def test_correo_duplicado(self):
        self.client.post(reverse('register'), DATOS)
        self.client.post(reverse('logout'))
        r = self.client.post(reverse('register'), {**DATOS, 'username': 'otra'})
        self.assertContains(r, 'already exists')


from django.core.management import call_command


class SeccionesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed')

    def test_paginas(self):
        for name in ('platforms', 'projects', 'blog', 'videos'):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_filtro_dificultad(self):
        r = self.client.get(reverse('projects'), {'difficulty': 'Expert'})
        self.assertContains(r, 'Ewatch')
        self.assertNotContains(r, 'Murdrum')

    def test_paginacion(self):
        self.assertContains(self.client.get(reverse('projects'), {'page': 2}), 'Raspberry Pi Cloud Drive')

    def test_busqueda_blog(self):
        r = self.client.get(reverse('blog'), {'q': 'Hailo'})
        self.assertContains(r, 'Hailo-8 vs')
        self.assertNotContains(r, 'Maker Faire')

    def test_videos_por_tag(self):
        r = self.client.get(reverse('videos_tag', args=['potw']))
        self.assertContains(r, 'PicoScope')
        self.assertNotContains(r, 'Maker Faire')
