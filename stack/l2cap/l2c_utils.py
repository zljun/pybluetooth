from enum import IntEnum, IntFlag
from bt_types import *
from hci_usb import *
from hci_def import *

tL2C_LCB* 

class l2c_utils():
    
    def __init__(self):
        pass
        
    def create_conn(p_lcb, transport=tBT_TRANSPORT.BR_EDR, initiating_phys=None):
        
        btsnd_hcic_create_conn(
      p_lcb->remote_bd_addr, (HCI_PKT_TYPES_MASK_DM1 | HCI_PKT_TYPES_MASK_DH1 |
                              HCI_PKT_TYPES_MASK_DM3 | HCI_PKT_TYPES_MASK_DH3 |
                              HCI_PKT_TYPES_MASK_DM5 | HCI_PKT_TYPES_MASK_DH5),
      page_scan_rep_mode, page_scan_mode, clock_offset, allow_switch);

if __name__ == '__main__':
    pass    

