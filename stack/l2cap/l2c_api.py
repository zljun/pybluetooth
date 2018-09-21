from enum import IntEnum, IntFlag
from hci_usb import *
from hci_def import *
  
class l2cap():
    
    def __init__(self):
        self.l2cb = tL2C_CB()
        pass
        
    def ConnectReq(self, psm=psm_t.SDP, p_bd_addr, p_ertm_info=None):
        ''' First, see if we already have a link to the remote 
           assume all ERTM l2cap connection is going over BR/EDR for now '''
  p_lcb = l2cu_find_lcb_by_bd_addr(p_bd_addr, BT_TRANSPORT_BR_EDR);
  if (p_lcb == NULL) {
    /* No link. Get an LCB and start link establishment */
    p_lcb = l2cu_allocate_lcb(p_bd_addr, false, BT_TRANSPORT_BR_EDR);
    /* currently use BR/EDR for ERTM mode l2cap connection */
    if ((p_lcb == NULL) || (!l2cu_create_conn(p_lcb, BT_TRANSPORT_BR_EDR))) {
      L2CAP_TRACE_WARNING(
          "L2CAP - conn not started for PSM: 0x%04x  p_lcb: 0x%08x", psm,
          p_lcb);
      return (0);
    }
  }
        btu.is_acl_connected()
        pass
        self.l2cu.

if __name__ == '__main__':
    pass    

