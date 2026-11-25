from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import RegisterForm
from .models import Brand, Frame, Customer, Order, Review


def make_customer(phone='9876543210'):
    user = User.objects.create_user(username=phone, password='pass12345',
                                    first_name='Test')
    return Customer.objects.create(user=user, phone=phone, consent=True)


def make_frame():
    brand = Brand.objects.create(name='Ray-Ban')
    return Frame.objects.create(brand=brand, name='Aviator', price=2500,
                                image='frames/test.jpg')


class RegisterTests(TestCase):
    def form(self, phone):
        return RegisterForm({'name': 'Sweeti', 'phone': phone,
                             'password': 'secret123', 'consent': True})

    def test_bad_and_duplicate_phone_rejected(self):
        self.assertFalse(self.form('12345').is_valid())      # too short
        make_customer('9876543210')
        self.assertFalse(self.form('9876543210').is_valid())  # already used
        self.assertTrue(self.form('9123456780').is_valid())   # a good one


class OrderTests(TestCase):
    def test_order_copies_price_and_sets_ready_date(self):
        customer = make_customer()
        frame = make_frame()
        self.client.login(username='9876543210', password='pass12345')
        self.client.post(reverse('order_frame', args=[frame.id]), {'shop': 'CC'})
        order = Order.objects.get()
        self.assertEqual(order.price, frame.price)
        self.assertEqual(order.customer, customer)
        self.assertEqual(order.ready_by, order.created + timedelta(days=2))


class ReviewTests(TestCase):
    def test_review_only_after_pickup_and_auto_published(self):
        customer = make_customer()
        frame = make_frame()
        order = Order.objects.create(customer=customer, frame=frame,
                                     price=frame.price, shop='CC')
        self.client.login(username='9876543210', password='pass12345')
        url = reverse('write_review', args=[order.id])

        self.assertEqual(self.client.get(url).status_code, 404)  # not picked up yet

        order.status = 'PU'
        order.save()
        self.client.post(url, {'rating': 5, 'feedback': 'Great service'})
        review = Review.objects.get()
        self.assertTrue(review.approved)