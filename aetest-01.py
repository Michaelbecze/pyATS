import logging
from dotenv import load_dotenv
from pyats import aetest
from genie.testbed import load
from genie.utils import Dq

load_dotenv() 
log = logging.getLogger(__name__)

EXPECTED_EIGRP = 2
EXPECTED_CDP = 3


class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect(self, testbed):
        testbed.connect(log_stdout=False)

    @aetest.subsection
    def loop_devices(self, testbed):
        aetest.loop.mark(EIGRP_Neighbor, device_name=list(testbed.devices))


class EIGRP_Neighbor(aetest.Testcase):
    @aetest.setup
    def setup(self, testbed, device_name):
        self.device = testbed.devices[device_name]

    @aetest.test
    def eigrp_neighbor_count(self):
        out = self.device.parse("show ip eigrp neighbors")
        neighbors = out.q.get_values("eigrp_nbr")
        uptimes = out.q.get_values("uptime")
        count = len(neighbors)

        for addr, up in zip(neighbors, uptimes):
            print(f"{self.device.name}: neighbor {addr}, uptime {up}")

        if count != EXPECTED_EIGRP:
            self.failed(f"{self.device.name}: expected {EXPECTED_EIGRP} EIGRP neighbors, found {count}")

class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect(self, testbed):
        testbed.disconnect()


if __name__ == "__main__":
    aetest.main(testbed=load("testbed.yml"))
