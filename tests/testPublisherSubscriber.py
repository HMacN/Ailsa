import unittest

from Mocks.MockSubscriber import MockSubscriber
from controller.Publisher import Publisher


class PublisherSubscriberTests(unittest.TestCase):
    def test_get_set_subscriber(self):
        expected_subscriber = MockSubscriber()
        publisher = Publisher()

        publisher.set_subscriber(expected_subscriber)

        found_subscriber = publisher.get_subscribers()

        self.assertEqual(expected_subscriber, found_subscriber)
