from dataclasses import dataclass
import dataclasses
from enum import IntEnum, IntFlag
from bitstring import BitArray
from co_types import *
from include.bt_types import *      
               
class btsnoop_packet_t(IntEnum8):
    HCI_CMD = 2
    ACL_OUT = 0
    ACL_IN = 1
    HCI_EVT = 3

@dataclass
class hci_event(basedataclass):
    hci_flag: uint8 = 0x04
    hci_code: uint8 = None
    hci_length: uint8 = None

    def decode(self, data):
        event_tree = protocol_tree(hci_event)    
        search_node = event_tree.root
        match_protocol = None
        while(search_node != None):
            protocol = search_node.cls
            if(protocol().match(data)): # yes
                match_protocol = protocol
                if len(search_node.sons) == 0:
                    break
                search_node = search_node.sons[-1]
            else:
                search_node = search_node.previous_brother
        return match_protocol().unpack(data)   
            
    
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

