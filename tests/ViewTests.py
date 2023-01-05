import unittest

from view.AilsaView import AilsaView


class ViewTests(unittest.TestCase):

    def test_registers_controller(self):

        given_controller = AilsaControllerStub()
        view = AilsaView()

        view.register_controller(given_controller)

        registered_controller = view.get_controller()

        self.assertEqual(given_controller, registered_controller)


class AilsaControllerStub:
    pass
