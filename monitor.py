from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.recoco import Timer
import time

log = core.getLogger()

class Monitor(object):
    def __init__(self):
        core.openflow.addListeners(self)

        # For monitoring
        self.stats = {}

        # For learning switch logic
        self.mac_to_port = {}

        # Start stats request every 5 sec
        Timer(5, self.request_stats, recurring=True)

    # 🔷 Request stats
    def request_stats(self):
        for connection in core.openflow._connections.values():
            connection.send(of.ofp_stats_request(
                body=of.ofp_port_stats_request()
            ))

    # 🔷 MONITORING LOGIC
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

    # 🔷 CUSTOM FORWARDING LOGIC (VERY IMPORTANT)
    def _handle_PacketIn(self, event):
        packet = event.parsed
        dpid = event.connection.dpid
        in_port = event.port

        if not packet.parsed:
            return

        # Initialize MAC table
        if dpid not in self.mac_to_port:
            self.mac_to_port[dpid] = {}

        # Learn source MAC
        self.mac_to_port[dpid][packet.src] = in_port

        # Decide output port
        if packet.dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][packet.dst]
        else:
            out_port = of.OFPP_FLOOD

        # Create flow rule
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, in_port)
        msg.actions.append(of.ofp_action_output(port=out_port))

        event.connection.send(msg)


def launch():
    core.registerNew(Monitor)
