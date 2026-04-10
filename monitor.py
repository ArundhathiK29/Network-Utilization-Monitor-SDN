from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.recoco import Timer
import time

log = core.getLogger()

class Monitor(object):
    def __init__(self):
        core.openflow.addListeners(self)
        self.stats = {}
        Timer(5, self.request_stats, recurring=True)

    def request_stats(self):
        for connection in core.openflow._connections.values():
            connection.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))

    def _handle_PortStatsReceived(self, event):
        now = time.time()
        dpid = event.connection.dpid

        if dpid not in self.stats:
            self.stats[dpid] = {}

        for stat in event.stats:
            port = stat.port_no
            rx_bytes = stat.rx_bytes
            tx_bytes = stat.tx_bytes

            if port not in self.stats[dpid]:
                self.stats[dpid][port] = (rx_bytes, tx_bytes, now)
                continue

            old_rx, old_tx, old_time = self.stats[dpid][port]

            time_diff = now - old_time
            rx_rate = (rx_bytes - old_rx) / time_diff
            tx_rate = (tx_bytes - old_tx) / time_diff

            print(f"[Switch {dpid}] Port {port} → RX: {rx_rate:.2f} B/s | TX: {tx_rate:.2f} B/s")

            self.stats[dpid][port] = (rx_bytes, tx_bytes, now)

def launch():
    core.registerNew(Monitor)
