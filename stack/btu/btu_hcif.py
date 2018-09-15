import sys
sys.path.append('../../')
sys.path.append('../')

from enum import IntEnum, IntFlag
from hci_usb import *
from hci_def import *
from binascii import hexlify
import logging
import logging.config

logging.config.fileConfig('../../logging.conf')
logger_btu = logging.getLogger(__name__)

class btu():
    
    def __init__(self):
        self.transport = hci_usb()
        self.process_event_thread = Thread(target=self.process_event, daemon=True).start()
        
    def process_event(self):
        
        while True:
            for x in self.transport.rx_evt_queue:
                logger_btu.debug('hci event {}'.format(hexlify(x)))
                evt = hci_event().decode(b'\x04' + x)
                logger_btu.info(evt)
                #if evt in l2cap_events:'''
                self.transport.rx_evt_queue.remove(x)
            for x in self.transport.rx_acl_queue:
                pass
                
    def btu_hcif_send_cmd(self, controller_id=None, p_buf=None):
        logger_btu.info('hci cmd {}'.format(hexlify(p_buf)))
        self.transport.tx_queue.append(p_buf)

if __name__ == '__main__':
    
    btu = btu()   
    btu.btu_hcif_send_cmd(p_buf=b'\x01\x03\0x0c\x00')
    while(1):
        continue

