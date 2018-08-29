from dataclasses import dataclass
import dataclasses
from enum import IntEnum, IntFlag
from bitstring import BitArray
from co_types import *

class lmp_version(IntEnum16):
   V1_0b = 0
   V1_1 = 1
   V2_0b = 2
   V2_0_EDR = 3
   V2_1_EDR = 4
   V3_0_HS = 5
   V4_0 = 6
   V4_1 = 7
   V4_2 = 8
   V5_0 = 9

   def __str__(self):
        for x in lmp_version.__members__:
            if lmp_version.__members__[x] == self:
                return x
        return 'unknown'

class lmp_manufacture(IntEnum16):
    Ericsson = 0
    Nokia = 1
    Intel_Corp = 2
    IBM = 3
    Toshiba_Corp = 4
    _3COM = 5
    Microsoft = 6
    Lucent = 7
    Motorola = 8
    Infineon = 9
    Qualcomm_CSR = 10
    Silicon_Wave = 11
    Digianswer = 12
    Texas_Instruments = 13
    Parthus = 14
    Broadcom_Corporation = 15
    Qualcomm = 29 
    Renesas = 54
    MediaTek = 70
    Marvell = 72
    Apple = 76
    Harman = 87
    Nordic = 89
    Realtek = 93
    RDA = 97
    MindTree = 106
    ShangHai_Super_Smart = 114
    Vimicro = 129
    Quintic = 142
    Airoha = 148
    Bestechnic = 688

    def __str__(self):
        for x in lmp_manufacture.__members__:
            if lmp_manufacture.__members__[x] == self:
                return x
        return 'unknown'       
               
class power_mode_t(IntEnum8):
    ACTIVE = 0
    HOLD = 1
    SNIFF = 2

# both ACL in and out use 2 in btsnoop file, so use btsnp_packet_t to determine
class hci_flag_t(IntEnum8):
    HCI_CMD = 1
    ACL_OUT = 2
    ACL_IN = 3
    HCI_EVT = 4

class btsnoop_packet_t(IntEnum8):
    HCI_CMD = 2
    ACL_OUT = 0
    ACL_IN = 1
    HCI_EVT = 3
    
class hci_cmd_opcode_t(IntEnum16):
    LE_SET_EXT_SCAN_ENABLE = 0x2042    
    
@dataclass
class hci_cmd():
    hci_flag: uint8 = 0x01
    hci_opcode: uint16 = None
    hci_length: uint8 = None

@dataclass
class hci_reset(hci_cmd):
    hci_opcode: uint16 = 0x0c03
    hci_length: uint8 = 0x00 
    
@dataclass
class hci_inquiry(hci_cmd):
    hci_opcode: uint16 = 0x0401
    hci_length: uint8 = 5
    lap: bytearray = b'\x33\x8b\x9e'
    inquiry_time: uint8 = None
    max_reponses: uint8 = None

@dataclass
class hci_inquiry_cancel(hci_cmd):
    hci_opcode: uint16 = 0x0402
    hci_length: uint8 = 0
    
@dataclass
class hci_write_inquiry_tx_power_level(hci_cmd):
    hci_opcode: uint16 = 0x0059
    hci_length: uint8 = 0


@dataclass
class hci_create_connection(hci_cmd):
    hci_opcode: uint16 = 0x0405
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

@dataclass
class hci_event():
    hci_flag: uint8 = 0x04
    hci_code: uint8 = None
    hci_length: uint8 = None
    
@dataclass
class hci_cmd_status(hci_event):
    hci_code: uint8 = 0x0f
    hci_length: uint8 = 0x04
    hci_status: uint8 = None
    hci_num_packet: uint8 = None
    hci_opcode: uint16 = None       

@dataclass
class hci_cmd_complete(hci_event):
    hci_code: uint8 = 0x0e
    hci_length: uint8 = None
    hci_num_packet: uint8 = None
    hci_opcode: uint16 = None
    hci_status: uint8 = None

@dataclass
class hci_inquiry_complete(hci_event):
    hci_code: uint8 = 0x01
    hci_length: uint8 = 1
    status: uint8 = None

@dataclass
class hci_inquiry_result(hci_event):
    hci_code: uint8 = 0x02
    n_responses: uint8 = None
    bd_addr: bdaddr_t = None
    page_scan_rep_mode: uint8 = None
    reserve1: uint8 = None
    reserve2: uint8 = None
    class_of_device: uint24 = None
    clock_offset: uint16 = None
    
@dataclass
class hci_inquiry_result_rssi(hci_event):
    hci_code: uint8 = 0x22
    n_responses: uint8 = None
    bd_addr: bdaddr_t = None
    page_scan_rep_mode: uint8 = None
    reserve1: uint8 = None
    reserve2: uint8 = None
    class_of_device: uint24 = None
    clock_offset: uint16 = None
    rssi: int8 = None

@dataclass
class hci_ext_inquiry_result(hci_event):
    hci_code: uint8 = 0x2F
    n_responses: uint8 = 0x01
    bd_addr: bdaddr_t = None
    page_scan_rep_mode: uint8 = None
    reserve: uint8 = None
    class_of_device: uint24 = None
    clock_offset: uint16 = None
    rssi: int8 = None
    eir: bytearray = None

@dataclass
class hci_connection_complete(hci_event):
    hci_code: uint8 = 0x03
    hci_status: uint8 = None
    connection_handle: uint16 = None
    peer_addr: bdaddr_t = None
    link_type: uint8 = None
    encrypt_mode: uint8 = None    

@dataclass
class hci_mode_change(hci_event):
    hci_code: uint8 = 0x14
    hci_length: uint8 = 6
    hci_status: uint8 = None
    connection_handle: uint16 = None
    mode: uint8 = None
    interval: uint16 = None    

@dataclass
class hci_sync_connection_complete(hci_event):
    hci_code: uint8 = 0x2c
    hci_length: uint8 = 17
    hci_status: uint8 = None
    connection_handle: uint16 = None
    peer_addr: bdaddr_t = None
    link_type: uint8 = None
    T: uint8 = None
    W: uint8 = None
    rx_packet_len: uint16 = None
    tx_packet_len: uint16 = None
    air_mode: uint8 = None

@dataclass
class hci_disconnection_complete(hci_event):
    hci_code: uint8 = 0x05
    hci_status: uint8 = None
    connection_handle: uint16 = None
    reason: uint8 = None
    
@dataclass
class hci_remote_name_request_complete(hci_event):
    hci_code: uint8 = 0x07
    hci_status: uint8 = None
    peer_addr: bdaddr_t = None
    name: str = None
    
@dataclass
class hci_read_remote_version_complete(hci_event):
    hci_code: uint8 = 0x0c
    hci_status: uint8 = None
    handle: uint16 = None
    lmp_version: uint8 = None
    lmp_manufacture: uint16 = None
    lmp_subversion: uint16 = None

@dataclass
class hci_le_event(hci_event):
    hci_code: uint8 = 0x3E
    sub_event_code: uint8 = None    

@dataclass
class hci_le_ext_adv_report_event(hci_le_event):
    sub_event_code: uint8 = 0x0D
    n_reports: uint8 = None
    event_type: uint16 = None
    addr_type: uint8 = None
    bdaddr: bdaddr_t = None
    primary_phy: uint8 = None
    secondary_phy: uint8 = None
    sid: uint8 = None
    tx_power: int8 = None
    rssi: int8 = None
    adv_interval: uint16 = None
    direct_addr_type: uint8 = None
    direct_addr: bdaddr_t = None
    adv_data_len: uint8 = None
    adv_data: bytearray = None

