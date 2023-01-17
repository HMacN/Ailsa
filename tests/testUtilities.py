import unittest

from util.Starter import Starter
from mocks.MockSubscriber import MockSubscriber
from util.IdentifiedObject import IdentifiedObject
from util.publisher_subscriber.Publisher import Publisher


class UtilitiesTests(unittest.TestCase):

    def test_publisher_initialises_empty(self):
        publisher = Publisher()

        self.assertEqual(publisher.get_subscribers(), set())

    def test_publisher_get_set_subscriber(self):
        expected_subscriber = MockSubscriber()
        expected_set_of_subscribers = {expected_subscriber}
        publisher = Publisher()

        publisher.add_subscriber(expected_subscriber)
        found_set_of_subscribers = publisher.get_subscribers()

        self.assertEqual(expected_set_of_subscribers, found_set_of_subscribers)

    def test_publisher_get_set_multiple_subscribers(self):
        sub_1 = MockSubscriber()
        sub_2 = MockSubscriber()
        sub_3 = MockSubscriber()
        expected_set_of_subscribers = {sub_1, sub_2, sub_3}
        pub = Publisher()

        pub.add_subscriber(sub_1)
        pub.add_subscriber(sub_2)
        pub.add_subscriber(sub_3)
        found_set_of_subscribers = pub.get_subscribers()

        self.assertEqual(expected_set_of_subscribers, found_set_of_subscribers)

    def test_publisher_get_subscribers_when_empty(self):
        expected_set_of_subscribers = set()
        publisher = Publisher()

        found_set_of_subscribers = publisher.get_subscribers()

        self.assertEqual(expected_set_of_subscribers, found_set_of_subscribers)

    def test_publisher_remove_subscriber(self):
        sub_1 = MockSubscriber()
        sub_2 = MockSubscriber()
        sub_3 = MockSubscriber()
        expected_set_of_subscribers = {sub_1, sub_3}
        pub = Publisher()

        pub.add_subscriber(sub_1)
        pub.add_subscriber(sub_2)
        pub.add_subscriber(sub_3)
        pub.remove_subscriber(sub_2)
        found_set_of_subscribers = pub.get_subscribers()

        self.assertEqual(expected_set_of_subscribers, found_set_of_subscribers)

    def test_publisher_handles_removing_subscriber_that_was_not_added(self):
        sub_1 = MockSubscriber()
        sub_2 = MockSubscriber()
        sub_3 = MockSubscriber()
        expected_set_of_subscribers = {sub_1, sub_2}
        pub = Publisher()

        pub.add_subscriber(sub_1)
        pub.add_subscriber(sub_2)
        pub.remove_subscriber(sub_3)
        found_set_of_subscribers = pub.get_subscribers()

        self.assertEqual(expected_set_of_subscribers, found_set_of_subscribers)

    def test_publisher_handles_removing_subscriber_when_empty(self):
        sub_1 = MockSubscriber()
        expected_set_of_subscribers = set()
        pub = Publisher()

        pub.remove_subscriber(sub_1)
        found_set_of_subscribers = pub.get_subscribers()

        self.assertEqual(expected_set_of_subscribers, found_set_of_subscribers)

    def test_publisher_notifies_subscribers(self):
        sub_1 = MockSubscriber()
        sub_2 = MockSubscriber()
        sub_3 = MockSubscriber()
        pub = Publisher()

        pub.add_subscriber(sub_1)
        pub.add_subscriber(sub_2)
        pub.add_subscriber(sub_3)
        pub.notify_all()

        self.assertTrue(sub_1.is_notified())
        self.assertTrue(sub_2.is_notified())
        self.assertTrue(sub_3.is_notified())

    def test_publisher_handles_notifying_all_when_empty(self):
        sub_1 = MockSubscriber()
        pub = Publisher()

        pub.notify_all()

        self.assertFalse(sub_1.is_notified())

    def test_publisher_can_notify_individual_subscriber(self):
        sub_1 = MockSubscriber()
        sub_2 = MockSubscriber()
        sub_3 = MockSubscriber()
        pub = Publisher()

        pub.add_subscriber(sub_1)
        pub.add_subscriber(sub_2)
        pub.add_subscriber(sub_3)
        pub.notify(sub_2)

        self.assertFalse(sub_1.is_notified())
        self.assertTrue(sub_2.is_notified())
        self.assertFalse(sub_3.is_notified())

    def test_publisher_handles_notifying_subscriber_that_was_not_added(self):
        sub_1 = MockSubscriber()
        sub_2 = MockSubscriber()
        sub_3 = MockSubscriber()
        pub = Publisher()

        pub.add_subscriber(sub_1)
        pub.add_subscriber(sub_3)
        pub.notify(sub_2)

        self.assertFalse(sub_1.is_notified())
        self.assertFalse(sub_2.is_notified())
        self.assertFalse(sub_3.is_notified())

    def test_publisher_handles_notifying_subscriber_when_empty(self):
        sub_1 = MockSubscriber()
        pub = Publisher()

        pub.notify(sub_1)

        self.assertFalse(sub_1.is_notified())

    def test_identified_object_returns_data(self):
        horizontal_distance_to_origin = 16
        vertical_distance_to_origin = 17
        bounding_box_width = 3
        bounding_box_height = 4
        object_name = "Name"

        ident = IdentifiedObject(horizontal_distance_to_origin,
                                 vertical_distance_to_origin,
                                 bounding_box_width,
                                 bounding_box_height,
                                 object_name)

        self.assertEqual(horizontal_distance_to_origin, ident.get_horizontal_distance_to_origin())
        self.assertEqual(vertical_distance_to_origin, ident.get_vertical_distance_to_origin())
        self.assertEqual(bounding_box_width, ident.get_bounding_box_width())
        self.assertEqual(bounding_box_height, ident.get_bounding_box_height())
        self.assertEqual(object_name, ident.get_object_name())

    def test_startup_object_assigns_view_to_controller(self):
        startup = Starter()

