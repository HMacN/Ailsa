import unittest

from controller.AilsaController import AilsaController


class ControllerTests(unittest.TestCase):
    def test_registers_view(self):
        given_view = AilsaViewStub()
        controller = AilsaController()

        controller.register_view(given_view)

        registered_view = controller.get_view()

        self.assertEqual(registered_view, given_view)


class AilsaViewStub:
    pass
