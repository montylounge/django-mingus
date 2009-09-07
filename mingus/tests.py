from django.test.client import Client
import unittest


class MingusClientTests(unittest.TestCase):
    fixtures = ['mammals.json', 'birds']

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_HomePage(self):
        '''Test if the homepage renders.'''
        c = Client()
        response = c.get('/')
        self.failUnlessEqual(response.status_code, 200)

    def test_About(self):
        'Test if the about page renders.'
        c = Client()
        response = c.get('/about/')
        self.failUnlessEqual(response.status_code, 200)

    def test_Contact(self):
        'Test if the contact page renders.'
        c = Client()
        response = c.get('/contact/')

        self.failUnlessEqual(response.status_code, 200)

    def test_ContactSubmit(self):
        '''Test submitting the contact form. Expect to return to the form sent template.

        The field 'fonzie_kungfu' is the honeypot field to protect you from
        spam. This feature is provided by django-honeypot.

        '''
        c = Client()
        response = c.post('/contact/', {'name': 'charles', 'email': 'foo@foo.com',
                    'body': 'hello.', 'fonzie_kungfu': ''},
                    follow=True)
        self.failUnlessEqual(response.status_code, 200)
        self.assertEquals(response.template[0].name, 'contact_form/contact_form_sent.html')


    def test_ContactSubmit_WithHoneyPot(self):
        '''Test the @honeypot decorator which exists to reduce spam.

        HoneyPot will return a 400 response if the honeypot field is
        submited with a value.

        '''
        c = Client()
        response = c.post('/contact/', {'name': 'charles', 'email':
                    'foo@foo.com', 'body': 'hello.', 'fonzie_kungfu': 'evil'},
                    follow=True)
        self.failUnlessEqual(response.status_code, 400)


    def test_QuoteList(self):
        '''Test quote list page renders.'''

        c = Client()
        response = c.get('/quotes/')
        self.failUnlessEqual(response.status_code, 200)

    def test_QuoteDetail(self):
        '''Test quote list page renders.'''

        from quoteme.models import Quote

        quote = Quote.objects.get()

        c = Client()
        response = c.get(quote.get_absolute_url())
        self.failUnlessEqual(response.status_code, 200)


    def test_RSS(self):
        '''Test the latest posts feed displays.'''

        c = Client()
        response = c.get('/feeds/latest/')
        self.failUnlessEqual(response.status_code, 200)

    def test_SpringsteenFeed(self):
        '''Test the latest springsteen feed for findjango integration displays.'''

        c = Client()
        response = c.get('/api/springsteen/posts/')
        self.failUnlessEqual(response.status_code, 200)






