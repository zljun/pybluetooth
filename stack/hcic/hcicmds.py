if __name__ == '__main__':
    import sys
    sys.path.append('../../')
    sys.path.append('../')
#endif
from dataclasses import dataclass
import dataclasses
from enum import IntEnum, IntFlag
from co_types import *
from include.bt_types import *  
from hci_def import *
from btm.btm_acl import *

class hci_cmd_opcode_t(IntEnum16):
    RESET = 0x0c03
    INQUIRY = 0x0401
    INQUIRY_CANCEL = 0x0402
    CREATE_CONNECTION = 0x0405
    LE_SET_EXT_SCAN_ENABLE = 0x2042    
    
@dataclass
class hci_cmd(basedataclass):
    hci_flag: uint8 = 0x01
    hci_opcode: uint16 = None
    hci_length: uint8 = None

@dataclass
class hci_reset(hci_cmd):
    hci_opcode: uint16 = hci_cmd_opcode_t.RESET
    hci_length: uint8 = 0x00 
    
@dataclass
class hci_inquiry(hci_cmd):
    hci_opcode: uint16 = hci_cmd_opcode_t.INQUIRY
    hci_length: uint8 = 5
    lap: bytearray = b'\x33\x8b\x9e'
    inquiry_time: uint8 = None
    max_reponses: uint8 = None

@dataclass
class hci_inquiry_cancel(hci_cmd):
    hci_opcode: uint16 = hci_cmd_opcode_t.INQUIRY_CANCEL
    hci_length: uint8 = 0
    
@dataclass
class hci_write_inquiry_tx_power_level(hci_cmd):
    hci_opcode: uint16 = 0x0059
    hci_length: uint8 = 0


@dataclass
class hci_create_connection(hci_cmd):
    hci_opcode: uint16 = hci_cmd_opcode_t.CREATE_CONNECTION
    hci_length: uint8 = 13
    peer_addr: bdaddr_t = None
    acl_packet_types: uint16 = None
    page_scan_repetition_mode: uint8=None
    page_scan_mode: uint8=None
    clock_offset: uint16=None
    allow_role_switch: uint8=None

@dataclass
class hci_sniff_mode(hci_cmd):
    hci_opcode: uint16 = 0x0803
    hci_length: uint8 = 10
    handle: uint16 = None
    max_interval: uint16 = None
    min_interval: uint16 = None
    attempt: uint16 = None
    timeout: uint16 = None
    
@dataclass
class hci_exit_sniff_mode(hci_cmd):
    hci_opcode: uint16 = 0x0804
    hci_length: uint8 = 2
    handle: uint16 = None
    
@dataclass
class hci_le_set_ext_scan_enable(hci_cmd):
    hci_opcode: uint16 = hci_cmd_opcode_t.LE_SET_EXT_SCAN_ENABLE
    hci_length: uint8 = 6
    scanning: uint8 = None
    filter_dup: uint8 = None
    scan_duration: uint16 = None
    scan_interval: uint16 = None

if __name__ == '__main__': 
    #b'\x20\x47\xda\xa0\xb6\xaf'
    p = hci_create_connection(peer_addr=bdaddr_t(b'\xaf\xb6\xa0\xda\x47\x20'), 
                            acl_packet_types=acl_packet_t.NO_1M, 
                            page_scan_repetition_mode=page_scan_repition_mode_t.R0, 
                            page_scan_mode=page_scan_mode_t.MODE0, 
                            clock_offset=0, 
                            allow_role_switch=False).pack()
    b = btu()   
    b.btu_hcif_send_cmd(p_buf=p);
    while(1):
        continue

