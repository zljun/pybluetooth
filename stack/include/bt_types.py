from dataclasses import dataclass
import dataclasses
from enum import IntEnum, IntFlag
from bitstring import BitArray
from co_types import *
import logging
import logging.config

logging.config.fileConfig('../../logging.conf')
logger_bttypes = logging.getLogger(__name__)

class bdaddr_t(bytearray):
    def __repr__(self):
        self.repr = '{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}'.format(self[5],self[4],self[3],self[2],self[1],self[0])
        return self.repr

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return 6  

class psm_t(IntEnum16):
    SDP = 0x0001 #See Bluetooth Service Discovery Protocol (SDP), Bluetooth SIG
    RFCOMM = 0x0003 #See RFCOMM with TS 07.10, Bluetooth SIG
    TCS_BIN = 0x0005 #See Bluetooth Telephony Control Specification / TCS Binary, Bluetooth SIG
    TCS_BIN_CORDLESS = 0x0007 #See Bluetooth Telephony Control Specification / TCS Binary, Bluetooth SIG
    BNEP = 0x000F #See Bluetooth Network Encapsulation Protocol, Bluetooth SIG
    HID_Control = 0x0011 #See Human Interface Device, Bluetooth SIG
    HID_Interrupt = 0x0013 #See Human Interface Device, Bluetooth SIG
    UPnP = 0x0015 #See [ESDP] , Bluetooth SIG
    AVCTP = 0x0017 #See Audio/Video Control Transport Protocol, Bluetooth SIG
    AVDTP = 0x0019 #See Audio/Video Distribution Transport Protocol, Bluetooth SIG
    AVCTP_Browsing = 0x001B #See Audio/Video Remote Control Profile, Bluetooth SIG
    UDI_C_Plane = 0x001D #See the Unrestricted Digital Information Profile [UDI], Bluetooth SIG
    ATT = 0x001F #See Bluetooth Core Specification.​​
    _3DSP = 0x0021 #​​See 3D Synchronization Profile, Bluetooth SIG.
    LE_PSM_IPSP = 0x0023 #​See Internet Protocol Support Profile (IPSP), Bluetooth SIG
    OTS = 0x0025 #See Object Transfer Service (OTS), Bluetooth SIG 


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

class tBT_TRANSPORT(IntEnum8):
    INVALID = 0
    BR_EDR = 1
    LE = 2

# Definitions for packet type masks (BT1.2 and BT2.0 definitions)
class acl_packet_t(IntFlag16):    
    NO_2_DH1 =0x0002
    NO_3_DH1 =0x0004
    DM1 =0x0008
    DH1 =0x0010
    HV1 =0x0020
    HV2 =0x0040
    HV3 =0x0080
    NO_2_DH3 =0x0100
    NO_3_DH3 =0x0200
    DM3 =0x0400
    DH3 =0x0800
    NO_2_DH5 =0x1000
    NO_3_DH5 =0x2000
    DM5 =0x4000
    DH5 =0x8000
    
    NO_1M = (DM1 | DH1 | DM3 | DH3 | DM5 | DH5)

# Page scan repitition modes 
class page_scan_repition_mode_t(IntEnum8):
    R0 =0x00
    R1 =0x01
    R2 =0x02
    
'''   /* Define limits for page scan repetition modes */
    #define HCI_PAGE_SCAN_R1_LIMIT 0x0800
    #define HCI_PAGE_SCAN_R2_LIMIT 0x1000
    
    /* Page scan period modes */
    #define HCI_PAGE_SCAN_PER_MODE_P0 0x00
    #define HCI_PAGE_SCAN_PER_MODE_P1 0x01
    #define HCI_PAGE_SCAN_PER_MODE_P2 0x02
'''    
# Page scan modes 
class page_scan_mode_t(IntEnum8):
    MODE0 = 0x00
    MODE1 =0x01
    MODE2 =0x02
    MODE3 =0x03

@dataclass
class basedataclass:
  def get_field_len(self, x, data=None):
    t = getattr(x, 'type')
    # length of string with terminator     
    if t == str and data !=None:
      terminator_found = False
      m = 0
      for x in data[offset:]:
        if x == 0x00:
          terminator_found = True
          break
        m +=1
      if terminator_found:
        return m
          
    try:
      m = len(t())
    except:
      default = getattr(x, 'default')
      try:
        m = len(default)
      except:
        m = 0
    return m
    
  def __len__(self):
    n = 0
    for x in dataclasses.fields(self): 
      n += self.get_field_len(x)
    return n

  def pack(self):
    data = b''
    logger_bttypes.info('pack {}'.format(type(self)))
    for x in dataclasses.fields(self): 
      default = getattr(x, 'default')
      fieldname = getattr(x, 'name')
      t = getattr(x, 'type')
      L = self.get_field_len(x)      
      value = getattr(self, fieldname)
      logger_bttypes.debug('fieldname={}, L={}, value={}'.format(fieldname, L, value))
      
      if t in [uint8, uint16, uint24, uint32, int8, int16, int32]:
        data += value.to_bytes(L, 'little')
      elif t in [uint16_be, uint32_be]:
        data += value.to_bytes(L, 'big')       
      elif t in [bdaddr_t, bytearray, str]:
        data += bytes(value)
      else:
        continue       

    return data
  
  def unpack1(self, data):
    if len(data) < len(self):
      logger_bttypes.error('data length {} less than expected {}'.format(len(data), len(self)))
      return None

    logger_bttypes.info('unpack {}'.format(type(self)))
    offset = 0  
    for x in dataclasses.fields(self): 
      default = getattr(x, 'default')
      fieldname = getattr(x, 'name')
      t = getattr(x, 'type')
      L = self.get_field_len(x, data)

      
      
      if t in [uint8, uint16, uint24, uint32, int8, int16, int32]:
        value = int.from_bytes(data[offset:offset+L], 'little')
      elif t in [uint16_be, uint32_be]:
        value = int.from_bytes(data[offset:offset+L], 'big')        
      elif t == bdaddr_t:
        value = data[offset:offset+L]
      elif t == str:
        value = str(data[offset:offset+L], 'utf-8')
      elif t in [bytearray]:
        value = data[offset:offset+L]
      else:
        logger_bttypes.warn('type {} not parserable'.format(t))
        continue
      logger_bttypes.debug('fieldname={}, L={}, value={}'.format(fieldname, L, value))
        
      offset += L

      # filed with default value shall be same as unpacked value
      if default != None and default != value:
        logger_bttypes.debug('unpack fail: value({}) !=default({})'.format(value, default))
        return None
      
      setattr(self, fieldname, t(value))  # set field value and type convert  
    logger_bttypes.info('unpack succeed {}'.format(type(self)))
    return self
    
  def unpack(self, data):
    ''''ret = self.unpack1(data, endian, dbg_en)
    return ret'''
    try:
        ret = self.unpack1(data)
        return ret
    except Exception as e:
        print(e)
        return None

  def match(self, data, dbg_en=False):
    if self.unpack(data) == None:
      return False
    else:
      return True
      
  def almost_equal(self, other):
      if other.__class__ != self.__class__:
          return False
          
      for x in dataclasses.fields(self):           
          fieldname = getattr(x, 'name')
          a = getattr(self, fieldname)
          b = getattr(other, fieldname)
          if a==None or b==None or a==b:
              continue
          else:
              return False
      return True

# (current parser, next parser if current pass, next parser if current fail)
class node:
    def __init__(self, c):
        self.name = c.__name__  
        self.cls = c
        self.parent = None
        self.sons = []
        self.elder_brothers = []
        
    def add_son(self, son_node):
        son_node.parent = self
        self.sons.append(son_node)

    def __repr__(self):
        try:
            rep = self.repr
        except:
            self.repr = 'nodename={}'.format(self.name)
            if self.parent != None:
                self.repr += ', parent={}'.format(self.parent.name)
            if len(self.sons) >0:
                self.repr += ', 1st son={}'.format(self.sons[0].name)
            if self.previous_brother != None:
                self.repr += ', brother={}, '.format(self.previous_brother.name)
            rep = self.repr

        return rep
        
class protocol_tree():
    def __init__(self, root_protocol):
        self.root = node(root_protocol)
        self.root.previous_brother = None
        self.nodes = [self.root]
        new_added_nodes = [self.root]        
        for p in new_added_nodes:     
            # sons of new added node p
            previous_brother = None
            for c in p.cls.__subclasses__(): 
                son_node = node(c)
                son_node.previous_brother = previous_brother
                previous_brother = son_node
                p.add_son(son_node)
                new_added_nodes.append(son_node)                
                self.nodes.append(son_node)
                
