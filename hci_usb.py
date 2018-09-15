import time
from datetime import datetime
from time import gmtime, sleep
from enum import IntEnum, IntFlag
from threading import Thread, Lock


import usb.core
import usb.util
import usb.control

USB_WIRELESS_CNTL_INTF_CLASS = 224
class hci_usb_endpoint_t(IntEnum):
    SCO_R = 131
    SCO_W = 3
    ACL_R = 130
    ACL_W = 2
    CMD_CTRL = 0
    EVT_INTR = 129

class hci_usb():
    usb_dev_inuse_list = []

    def __init__(self, id_vendor=0x0A12, id_product=0x0001, bus='AUTO', address='AUTO'):
        self.is_open = False
        self.dev_u = self.get_dev(id_vendor, id_product, bus, address)
        if self.dev_u == None:
            print('Can not open USB interface to device 0x{:04X}-0x{:04X}'.format(id_vendor, id_product))
            return
            
        self.vid = self.dev_u.idVendor
        self.pid = self.dev_u.idProduct
        self.addr = self.dev_u.address
        self.bus = self.dev_u.bus
        try:
            self.dev_u.detach_kernel_driver(0)
        except:
            pass

        self.dev_u.set_configuration(1)
        self.dev_u.set_interface_altsetting(interface=0, alternate_setting=0)
        self.dev_u.set_interface_altsetting(interface=1, alternate_setting=0)
        cfg = self.dev_u.get_active_configuration()
        intf = usb.util.find_descriptor(cfg, bInterfaceNumber=0)
        ep_evt = usb.util.find_descriptor(intf, bEndpointAddress=hci_usb_endpoint_t.EVT_INTR)
        ep_acl = usb.util.find_descriptor(intf, bEndpointAddress=hci_usb_endpoint_t.ACL_R)
        intf = usb.util.find_descriptor(cfg, bInterfaceNumber=1)
        ep_sco = usb.util.find_descriptor(intf, bEndpointAddress=hci_usb_endpoint_t.SCO_R)
        try:
            usb.control.clear_feature(self.dev_u, usb.control.ENDPOINT_HALT, ep_evt)
            usb.control.clear_feature(self.dev_u, usb.control.ENDPOINT_HALT, ep_acl)
            usb.control.clear_feature(self.dev_u, usb.control.ENDPOINT_HALT, ep_sco)
        except:
            print('No usb.control module available for this operation!!!')

        self.tx_queue = []
        self.rx_evt_queue = []
        self.rx_acl_queue = []
        self.rx_sco_queue = []
        self.default_to = 1000

        #start a thread to send HCI command and ACL data
        self.tx_thread = Thread(target = self.tx_thread_loop, daemon=True).start()
  
        # start a thread to receive HCI events
        self.rx_evt_thread = Thread(target = self.rx_evt_thread_loop, daemon=True).start()

        # start a thread to receive ACL data

        self.is_open = True

    def get_dev(self, vid, pid, bus, addr):
        all_devs = usb.core.find(find_all=True)
        candidates = []
        for d in all_devs:
            if (d.idVendor == vid) & (d.idProduct == pid):
                if (bus == 'AUTO') & (addr == 'AUTO'):
                    candidates.append(d)
                elif (bus == 'AUTO') & (d.address == addr):
                    candidates.append(d)
                elif (addr == 'AUTO') & (d.bus == bus):
                    candidates.append(d)
                elif (bus == -1) & (d.address == addr):
                    candidates.append(d)
                elif (d.address == addr) & (d.bus == bus):
                    candidates.append(d)

        for c in candidates:
            already_inuse = False
            for d in self.usb_dev_inuse_list:
                if (d.idVendor == c.idVendor) & (d.idProduct == c.idProduct) & (d.address == c.address) & (d.bus == c.bus):
                    already_inuse = True
                    break

            if not already_inuse:
                self.usb_dev_inuse_list.append(c)
                return c

        if len(candidates) != 0 and (addr != 'AUTO' or bus != 'AUTO'):
            print('USB device is already in use (due to a previous USB bus/address AUTO usage?)')
        if addr == 'AUTO' and bus == 'AUTO':
            print('No free USB device candidate found (too many USB devices listed?)')

    def send(self, msg):
        if type(msg) in [bytearray, bytes]:
            self.tx_queue.append(msg)
            
    def tx_thread_loop(self):
        while True:
            for c in self.tx_queue:
                if c[0] == 0x01:
                    status = self.dev_u.ctrl_transfer(32, 0, 0, 0, c[1:], timeout=self.default_to)
                elif c[0] == 0x02:
                    status = self.dev_u.write(hci_usb_endpoint_t.ACL_W, c[1:], 0, self.default_to)
                else:
                    continue
                self.tx_queue.remove(c)

    def rx_evt_thread_loop(self):
        to = 1000
        while(True):
            try:
                pkt = self.dev_u.read(hci_usb_endpoint_t.EVT_INTR, 1048, to)
            except Exception as e:
                pkt = b''
                pass

            if len(pkt) >0:
                self.rx_evt_queue.append(bytes(pkt))
                    
    def rx_acl_thread_loop(self):
        to = 1000
        try:
            pkt = self.dev_u.read(hci_usb_endpoint_t.ACL_R, 1048, to)
        except Exception as e:
            pkt = b''
            pass
            
        if len(pkt) >0:
            self.rx_acl_queue.append(bytes(pkt))
            
    def rx_sco_thread_loop(self):
        to = 1000
        try:
            pkt = self.dev_u.read(hci_usb_endpoint_t.SCO_R, 1048, to)
        except Exception as e:
            pkt = b''
            pass
            
        if len(pkt) >0:
            self.rx_sco_queue.append(bytes(pkt))

    def close(self):
        self.dev_u.reset()
        self.is_open = False

    def _is_open(self):
        return self.is_open

