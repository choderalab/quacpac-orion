from unittest import TestCase

from datarecord import OERecord
from floe.test import CubeTestRunner

from am1bcc_charge.mycube import MyCube


class MyCubeTest(TestCase):

    def setUp(self):
        super().setUp()
        # Here we create the counter cube and test runner
        self.cube = AM1BCCCharge("Charge")
        self.runner = CubeTestRunner(self.cube)

        # keep everything as default
        # self.runner.set_parameters(switch=True)

        # This method *must* be called prior to using the cube
        self.runner.start()
