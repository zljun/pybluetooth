
L2CAP_MIN_MTU = 48 # Minimum acceptable MTU is 48 bytes

'''
 * Timeout values (in milliseconds).
'''
L2CAP_LINK_ROLE_SWITCH_TIMEOUT_MS =(10 * 1000)  ## 10 seconds */
L2CAP_LINK_CONNECT_TIMEOUT_MS =(60 * 1000)      ## 30 seconds */
L2CAP_LINK_CONNECT_EXT_TIMEOUT_MS =(120 * 1000) ## 120 seconds */
L2CAP_ECHO_RSP_TIMEOUT_MS =(30 * 1000)          ## 30 seconds */
L2CAP_LINK_FLOW_CONTROL_TIMEOUT_MS =(2 * 1000)  ## 2 seconds */
L2CAP_LINK_DISCONNECT_TIMEOUT_MS =(30 * 1000)   ## 30 seconds */
L2CAP_CHNL_CONNECT_TIMEOUT_MS =(60 * 1000)      ## 60 seconds */
L2CAP_CHNL_CONNECT_EXT_TIMEOUT_MS =(120 * 1000) ## 120 seconds */
L2CAP_CHNL_CFG_TIMEOUT_MS =(30 * 1000)          ## 30 seconds */
L2CAP_CHNL_DISCONNECT_TIMEOUT_MS =(10 * 1000)   ## 10 seconds */
L2CAP_DELAY_CHECK_SM4_TIMEOUT_MS =(2 * 1000)    ## 2 seconds */
L2CAP_WAIT_INFO_RSP_TIMEOUT_MS =(3 * 1000)      ## 3 seconds */
L2CAP_BLE_LINK_CONNECT_TIMEOUT_MS =(30 * 1000)  ## 30 seconds */
L2CAP_FCR_ACK_TIMEOUT_MS =200                   ## 200 milliseconds */

''' Define the possible L2CAP channel states. The names of
 * the states may seem a bit strange, but they are taken from
 * the Bluetooth specification.'''
class tL2C_CHNL_STATE(Int8Enum):
    CST_CLOSED = 0,                  ## Channel is in closed state */
    CST_ORIG_W4_SEC_COMP = 1,        ## Originator waits security clearence */
    CST_TERM_W4_SEC_COMP = 2,        ## Acceptor waits security clearence */
    CST_W4_L2CAP_CONNECT_RSP = 3,    ## Waiting for peer conenct response */
    CST_W4_L2CA_CONNECT_RSP = 4,     ## Waiting for upper layer connect rsp */
    CST_CONFIG = 5,                  ## Negotiating configuration */
    CST_OPEN = 6,                    ## Data transfer state */
    CST_W4_L2CAP_DISCONNECT_RSP = 7, ## Waiting for peer disconnect rsp */
    CST_W4_L2CA_DISCONNECT_RSP = 8   ## Waiting for upper layer disc rsp */

'''' Define the possible L2CAP link states
'''
class tL2C_LINK_STATE(Int8Enum):
    LST_DISCONNECTED = 0,
    LST_CONNECT_HOLDING = 1,
    LST_CONNECTING_WAIT_SWITCH = 2,
    LST_CONNECTING = 3,
    LST_CONNECTED = 4,
    LST_DISCONNECTING = 5


/* Define a channel control block (CCB). There may be many channel control
 * blocks between the same two Bluetooth devices (i.e. on the same link).
 * Each CCB has unique local and remote CIDs. All channel control blocks on
 * the same physical link and are chained together.
*/
typedef struct t_l2c_ccb {
  bool in_use;                /* true when in use, false when not */
  tL2C_CHNL_STATE chnl_state; /* Channel state */
  tL2CAP_LE_CFG_INFO
      local_conn_cfg; /* Our config for ble conn oriented channel */
  tL2CAP_LE_CFG_INFO
      peer_conn_cfg;       /* Peer device config ble conn oriented channel */
  bool is_first_seg;       /* Dtermine whether the received packet is the first
                              segment or not */
  BT_HDR* ble_sdu;         /* Buffer for storing unassembled sdu*/
  uint16_t ble_sdu_length; /* Length of unassembled sdu length*/
  struct t_l2c_ccb* p_next_ccb; /* Next CCB in the chain */
  struct t_l2c_ccb* p_prev_ccb; /* Previous CCB in the chain */
  struct t_l2c_linkcb* p_lcb;   /* Link this CCB is assigned to */

  uint16_t local_cid;  /* Local CID */
  uint16_t remote_cid; /* Remote CID */

  alarm_t* l2c_ccb_timer; /* CCB Timer Entry */

  tL2C_RCB* p_rcb;      /* Registration CB for this Channel */
  bool should_free_rcb; /* True if RCB was allocated on the heap */

#define IB_CFG_DONE 0x01
#define OB_CFG_DONE 0x02
#define RECONFIG_FLAG 0x04 /* True after initial configuration */
#define CFG_DONE_MASK (IB_CFG_DONE | OB_CFG_DONE)

  uint8_t config_done; /* Configuration flag word */
  uint8_t local_id;    /* Transaction ID for local trans */
  uint8_t remote_id;   /* Transaction ID for local */

#define CCB_FLAG_NO_RETRY 0x01     /* no more retry */
#define CCB_FLAG_SENT_PENDING 0x02 /* already sent pending response */
  uint8_t flags;

  tL2CAP_CFG_INFO our_cfg;          /* Our saved configuration options */
  tL2CAP_CH_CFG_BITS peer_cfg_bits; /* Store what peer wants to configure */
  tL2CAP_CFG_INFO peer_cfg;         /* Peer's saved configuration options */

  fixed_queue_t* xmit_hold_q; /* Transmit data hold queue */
  bool cong_sent;             /* Set when congested status sent */
  uint16_t buff_quota;        /* Buffer quota before sending congestion */

  tL2CAP_CHNL_PRIORITY ccb_priority;  /* Channel priority */
  tL2CAP_CHNL_DATA_RATE tx_data_rate; /* Channel Tx data rate */
  tL2CAP_CHNL_DATA_RATE rx_data_rate; /* Channel Rx data rate */

  /* Fields used for eL2CAP */
  tL2CAP_ERTM_INFO ertm_info;
  tL2C_FCRB fcrb;
  uint16_t tx_mps; /* TX MPS adjusted based on current controller */
  uint16_t max_rx_mtu;
  uint8_t fcr_cfg_tries;          /* Max number of negotiation attempts */
  bool peer_cfg_already_rejected; /* If mode rejected once, set to true */
  bool out_cfg_fcr_present; /* true if cfg response shoulkd include fcr options
                               */

#define L2CAP_CFG_FCS_OUR 0x01  /* Our desired config FCS option */
#define L2CAP_CFG_FCS_PEER 0x02 /* Peer's desired config FCS option */
#define L2CAP_BYPASS_FCS (L2CAP_CFG_FCS_OUR | L2CAP_CFG_FCS_PEER)
  uint8_t bypass_fcs;

#if (L2CAP_NON_FLUSHABLE_PB_INCLUDED == TRUE)
  bool is_flushable; /* true if channel is flushable */
#endif

#if (L2CAP_NUM_FIXED_CHNLS > 0)
  uint16_t fixed_chnl_idle_tout; /* Idle timeout to use for the fixed channel */
#endif
  uint16_t tx_data_len;

  /* Number of LE frames that the remote can send to us (credit count in
   * remote). Valid only for LE CoC */
  uint16_t remote_credit_count;
} tL2C_CCB;


'''' Define a link control block. There is one link control block between
 * this device and any other device (i.e. BD ADDR).
'''
class tL2C_LCB():
  bool in_use; /* true when in use, false when not */
  tL2C_LINK_STATE link_state;

  alarm_t* l2c_lcb_timer; /* Timer entry for timeout evt */
  uint16_t handle;        /* The handle used with LM */

  tL2C_CCB_Q ccb_queue; /* Queue of CCBs on this LCB */

  tL2C_CCB* p_pending_ccb;  /* ccb of waiting channel during link disconnect */
  alarm_t* info_resp_timer; /* Timer entry for info resp timeout evt */
  RawAddress remote_bd_addr; /* The BD address of the remote */

  uint8_t link_role; /* Master or slave */
  uint8_t id;
  uint8_t cur_echo_id;              /* Current id value for echo request */
  tL2CA_ECHO_RSP_CB* p_echo_rsp_cb; /* Echo response callback */
  uint16_t idle_timeout;            /* Idle timeout */
  bool is_bonding;                  /* True - link active only for bonding */

  uint16_t link_flush_tout; /* Flush timeout used */

  uint16_t link_xmit_quota; /* Num outstanding pkts allowed */
  uint16_t sent_not_acked;  /* Num packets sent but not acked */

  bool partial_segment_being_sent; /* Set true when a partial segment */
                                   /* is being sent. */
  bool w4_info_rsp;                /* true when info request is active */
  uint8_t info_rx_bits;            /* set 1 if received info type */
  uint32_t peer_ext_fea;           /* Peer's extended features mask */
  list_t* link_xmit_data_q;        /* Link transmit data buffer queue */

  uint8_t peer_chnl_mask[L2CAP_FIXED_CHNL_ARRAY_SIZE];

  BT_HDR* p_hcit_rcv_acl;   /* Current HCIT ACL buf being rcvd */
  uint16_t idle_timeout_sv; /* Save current Idle timeout */
  uint8_t acl_priority;     /* L2C_PRIORITY_NORMAL or L2C_PRIORITY_HIGH */
  tL2CA_NOCP_CB* p_nocp_cb; /* Num Cmpl pkts callback */

#if (L2CAP_NUM_FIXED_CHNLS > 0)
  tL2C_CCB* p_fixed_ccbs[L2CAP_NUM_FIXED_CHNLS];
  uint16_t disc_reason;
#endif

  tBT_TRANSPORT transport;
  uint8_t initiating_phys;  // LE PHY used for connection initiation
  tBLE_ADDR_TYPE ble_addr_type;
  uint16_t tx_data_len; /* tx data length used in data length extension */
  fixed_queue_t* le_sec_pending_q; /* LE coc channels waiting for security check
                                      completion */
  uint8_t sec_act;
#define L2C_BLE_CONN_UPDATE_DISABLE \
  0x1                              /* disable update connection parameters */
#define L2C_BLE_NEW_CONN_PARAM 0x2 /* new connection parameter to be set */
#define L2C_BLE_UPDATE_PENDING                  \
  0x4 /* waiting for connection update finished \
         */
#define L2C_BLE_NOT_DEFAULT_PARAM \
  0x8 /* not using default connection parameters */
  uint8_t conn_update_mask;

  uint16_t min_interval; /* parameters as requested by peripheral */
  uint16_t max_interval;
  uint16_t latency;
  uint16_t timeout;
  uint16_t min_ce_len;
  uint16_t max_ce_len;

#if (L2CAP_ROUND_ROBIN_CHANNEL_SERVICE == TRUE)
  /* each priority group is limited burst transmission */
  /* round robin service for the same priority channels */
  tL2C_RR_SERV rr_serv[L2CAP_NUM_CHNL_PRIORITY];
  uint8_t rr_pri; /* current serving priority group */
#endif


'''' Define the L2CAP control structure
'''
class tL2C_CB():
  uint16_t controller_xmit_window; /* Total ACL window for all links */

  uint16_t round_robin_quota;   /* Round-robin link quota */
  uint16_t round_robin_unacked; /* Round-robin unacked */
  bool check_round_robin;       /* Do a round robin check */

  bool is_cong_cback_context;

  tL2C_LCB lcb_pool[MAX_L2CAP_LINKS];    /* Link Control Block pool */
  tL2C_CCB ccb_pool[MAX_L2CAP_CHANNELS]; /* Channel Control Block pool */
  tL2C_RCB rcb_pool[MAX_L2CAP_CLIENTS];  /* Registration info pool */

  tL2C_CCB* p_free_ccb_first; /* Pointer to first free CCB */
  tL2C_CCB* p_free_ccb_last;  /* Pointer to last  free CCB */

  uint8_t
      desire_role; /* desire to be master/slave when accepting a connection */
  bool disallow_switch;     /* false, to allow switch at create conn */
  uint16_t num_lm_acl_bufs; /* # of ACL buffers on controller */
  uint16_t idle_timeout;    /* Idle timeout */

  list_t* rcv_pending_q;       /* Recv pending queue */
  alarm_t* receive_hold_timer; /* Timer entry for rcv hold */

  tL2C_LCB* p_cur_hcit_lcb;  /* Current HCI Transport buffer */
  uint16_t num_links_active; /* Number of links active */

#if (L2CAP_NON_FLUSHABLE_PB_INCLUDED == TRUE)
  uint16_t non_flushable_pbf; /* L2CAP_PKT_START_NON_FLUSHABLE if controller
                                 supports */
  /* Otherwise, L2CAP_PKT_START */
  bool is_flush_active; /* true if an HCI_Enhanced_Flush has been sent */
#endif

#if (L2CAP_CONFORMANCE_TESTING == TRUE)
  uint32_t test_info_resp; /* Conformance testing needs a dynamic response */
#endif

#if (L2CAP_NUM_FIXED_CHNLS > 0)
  tL2CAP_FIXED_CHNL_REG
      fixed_reg[L2CAP_NUM_FIXED_CHNLS]; /* Reg info for fixed channels */
#endif

  uint16_t num_ble_links_active; /* Number of LE links active */
  bool is_ble_connecting;
  RawAddress ble_connecting_bda;
  uint16_t controller_le_xmit_window; /* Total ACL window for all links */
  tL2C_BLE_FIXED_CHNLS_MASK l2c_ble_fixed_chnls_mask;  // LE fixed channels mask
  uint16_t num_lm_ble_bufs;         /* # of ACL buffers on controller */
  uint16_t ble_round_robin_quota;   /* Round-robin link quota */
  uint16_t ble_round_robin_unacked; /* Round-robin unacked */
  bool ble_check_round_robin;       /* Do a round robin check */
  tL2C_RCB ble_rcb_pool[BLE_MAX_L2CAP_CLIENTS]; /* Registration info pool */

  tL2CA_ECHO_DATA_CB* p_echo_data_cb; /* Echo data callback */

#if (L2CAP_HIGH_PRI_CHAN_QUOTA_IS_CONFIGURABLE == TRUE)
  uint16_t high_pri_min_xmit_quota; /* Minimum number of ACL credit for high
                                       priority link */
#endif /* (L2CAP_HIGH_PRI_CHAN_QUOTA_IS_CONFIGURABLE == TRUE) */

  uint16_t dyn_psm;

  uint16_t le_dyn_psm; /* Next LE dynamic PSM value to try to assign */
  bool le_dyn_psm_assigned[LE_DYNAMIC_PSM_RANGE]; /* Table of assigned LE PSM */


/* Define a structure that contains the information about a connection.
 * This structure is used to pass between functions, and not all the
 * fields will always be filled in.
*/
typedef struct {
  RawAddress bd_addr;    /* Remote BD address */
  uint8_t status;        /* Connection status */
  uint16_t psm;          /* PSM of the connection */
  uint16_t l2cap_result; /* L2CAP result */
  uint16_t l2cap_status; /* L2CAP status */
  uint16_t remote_cid;   /* Remote CID */
} tL2C_CONN_INFO;

typedef void(tL2C_FCR_MGMT_EVT_HDLR)(uint8_t, tL2C_CCB*);

/* Necessary info for postponed TX completion callback
*/
typedef struct {
  uint16_t local_cid;
  uint16_t num_sdu;
  tL2CA_TX_COMPLETE_CB* cb;
} tL2C_TX_COMPLETE_CB_INFO;

/* The offset in a buffer that L2CAP will use when building commands.
*/
#define L2CAP_SEND_CMD_OFFSET 0

/* Number of ACL buffers to use for high priority channel
*/
#if (L2CAP_HIGH_PRI_CHAN_QUOTA_IS_CONFIGURABLE == FALSE)
#define L2CAP_HIGH_PRI_MIN_XMIT_QUOTA_A (L2CAP_HIGH_PRI_MIN_XMIT_QUOTA)
#else
#define L2CAP_HIGH_PRI_MIN_XMIT_QUOTA_A (l2cb.high_pri_min_xmit_quota)
#endif


