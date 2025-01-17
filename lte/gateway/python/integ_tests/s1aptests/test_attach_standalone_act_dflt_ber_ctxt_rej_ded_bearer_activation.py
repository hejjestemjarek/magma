"""
Copyright 2020 The Magma Authors.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import ipaddress
import time
import unittest

import s1ap_types
import s1ap_wrapper
from integ_tests.s1aptests.s1ap_utils import SessionManagerUtil
from lte.protos.policydb_pb2 import FlowMatch


class TestAttachStandaloneActDfltBerCtxtRejDedBearerActivation(
    unittest.TestCase,
):
    def setUp(self):
        self._s1ap_wrapper = s1ap_wrapper.TestWrapper()
        self._sessionManager_util = SessionManagerUtil()

    def tearDown(self):
        self._s1ap_wrapper.cleanup()

    def test_attach_standalone_act_dflt_ber_ctxt_rej_ded_bearer_activation(
        self,
    ):
        """ Attach + PDN connectivity req + activate default
        EPS bearer reject for secondary PDN
        + initiate RAR for the secondary PDN + detach"""

        self._s1ap_wrapper.configUEDevice(1)
        req = self._s1ap_wrapper.ue_req

        # APN of the secondary PDN
        ims = {
            "apn_name": "ims",  # APN-name
            "qci": 5,  # qci
            "priority": 15,  # priority
            "pre_cap": 0,  # preemption-capability
            "pre_vul": 0,  # preemption-vulnerability
            "mbr_ul": 200000000,  # MBR UL
            "mbr_dl": 100000000,  # MBR DL
        }
        # UL Flow description #1
        ulFlow1 = {
            "ipv4_dst": "192.168.129.42",  # IPv4 destination address
            "tcp_dst_port": 5002,  # TCP dest port
            "ip_proto": FlowMatch.IPPROTO_TCP,  # Protocol Type
            "direction": FlowMatch.UPLINK,  # Direction
        }

        # UL Flow description #2
        ulFlow2 = {
            "ipv4_dst": "192.168.129.42",  # IPv4 destination address
            "tcp_dst_port": 5001,  # TCP dest port
            "ip_proto": FlowMatch.IPPROTO_TCP,  # Protocol Type
            "direction": FlowMatch.UPLINK,  # Direction
        }

        # UL Flow description #3
        ulFlow3 = {
            "ipv4_dst": "192.168.129.64",  # IPv4 destination address
            "tcp_dst_port": 5003,  # TCP dest port
            "ip_proto": FlowMatch.IPPROTO_TCP,  # Protocol Type
            "direction": FlowMatch.UPLINK,  # Direction
        }

        # UL Flow description #4
        ulFlow4 = {
            "ipv4_dst": "192.168.129.42",  # IPv4 destination address
            "tcp_dst_port": 5004,  # TCP dest port
            "ip_proto": FlowMatch.IPPROTO_TCP,  # Protocol Type
            "direction": FlowMatch.UPLINK,  # Direction
        }

        # DL Flow description #1
        dlFlow1 = {
            "ipv4_src": "192.168.129.42",  # IPv4 source address
            "tcp_src_port": 5001,  # TCP source port
            "ip_proto": FlowMatch.IPPROTO_TCP,  # Protocol Type
            "direction": FlowMatch.DOWNLINK,  # Direction
        }

        # DL Flow description #2
        dlFlow2 = {
            "ipv4_src": "192.168.129.64",  # IPv4 source address
            "tcp_src_port": 5002,  # TCP source port
            "ip_proto": FlowMatch.IPPROTO_TCP,  # Protocol Type
            "direction": FlowMatch.DOWNLINK,  # Direction
        }

        # DL Flow description #3
        dlFlow3 = {
            "ipv4_src": "192.168.129.64",  # IPv4 source address
            "tcp_src_port": 5003,  # TCP source port
            "ip_proto": FlowMatch.IPPROTO_TCP,  # Protocol Type
            "direction": FlowMatch.DOWNLINK,  # Direction
        }
        # DL Flow description #4
        dlFlow4 = {
            "ipv4_src": "192.168.129.42",  # IPv4 source address
            "tcp_src_port": 5004,  # TCP source port
            "ip_proto": FlowMatch.IPPROTO_TCP,  # Protocol Type
            "direction": FlowMatch.DOWNLINK,  # Direction
        }

        # Flow list to be configured
        flow_list = [
            ulFlow1,
            ulFlow2,
            ulFlow3,
            ulFlow4,
            dlFlow1,
            dlFlow2,
            dlFlow3,
            dlFlow4,
        ]

        # QoS
        qos = {
            "qci": 1,  # qci value [1 to 9]
            "priority": 15,  # Range [0-255]
            "max_req_bw_ul": 10000000,  # MAX bw Uplink
            "max_req_bw_dl": 15000000,  # MAX bw Downlink
            "gbr_ul": 1000000,  # GBR Uplink
            "gbr_dl": 2000000,  # GBR Downlink
            "arp_prio": 15,  # ARP priority
            "pre_cap": 1,  # pre-emption capability
            "pre_vul": 1,  # pre-emption vulnerability
        }

        policy_id = "ims-voice"

        # APN list to be configured
        apn_list = [ims]

        self._s1ap_wrapper.configAPN(
            "IMSI" + "".join([str(i) for i in req.imsi]), apn_list,
        )
        print(
            "************************* Running End to End attach for UE id ",
            req.ue_id,
        )
        # Attach
        attach = self._s1ap_wrapper.s1_util.attach(
            req.ue_id,
            s1ap_types.tfwCmd.UE_END_TO_END_ATTACH_REQUEST,
            s1ap_types.tfwCmd.UE_ATTACH_ACCEPT_IND,
            s1ap_types.ueAttachAccept_t,
        )

        addr = attach.esmInfo.pAddr.addrInfo
        default_ip = ipaddress.ip_address(bytes(addr[:4]))

        # Wait on EMM Information from MME
        self._s1ap_wrapper._s1_util.receive_emm_info()
        print("Sleeping for 5 seconds")
        time.sleep(5)
        # Verify if flow rules are created
        # No dedicated bearers, so flow list will be empty
        dl_flow_rules = {
            default_ip: [],
        }
        # 1 UL flow for the default bearer
        num_ul_flows = 1
        self._s1ap_wrapper.s1_util.verify_flow_rules(
            num_ul_flows, dl_flow_rules,
        )

        print("Sleeping for 5 seconds")
        time.sleep(5)
        # Trigger Activate Default EPS Bearer Context Reject indication
        # so that s1ap tester sends Activate default EPS bearer context reject
        # instead of Activate default EPS bearer context accept
        def_ber_rej = s1ap_types.ueActvDfltEpsBearerCtxtRej_t()
        def_ber_rej.ue_Id = req.ue_id
        def_ber_rej.bearerId = attach.esmInfo.epsBearerId
        def_ber_rej.cause = s1ap_types.TFW_EMM_CAUSE_PROT_ERR_UNSP

        self._s1ap_wrapper._s1_util.issue_cmd(
            s1ap_types.tfwCmd.
            UE_STANDALONE_ACTV_DEFAULT_EPS_BEARER_CNTXT_REJECT,
            def_ber_rej,
        )
        print(
            "Sent STANDALONE_ACTV_DEFAULT_EPS_BEARER_CNTXT_REJECT indication",
        )
        print("Sleeping for 5 seconds")
        time.sleep(5)
        # Send PDN Connectivity Request
        apn = "ims"
        self._s1ap_wrapper.sendPdnConnectivityReq(req.ue_id, apn)
        # Receive PDN CONN RSP/Activate default EPS bearer context request
        response = self._s1ap_wrapper.s1_util.get_response()
        self.assertEqual(
            response.msg_type, s1ap_types.tfwCmd.UE_PDN_CONN_RSP_IND.value,
        )
        act_def_bearer_req = response.cast(s1ap_types.uePdnConRsp_t)

        print(
            "************************* Sending Activate default EPS bearer "
            "context reject for UE id %d and bearer %d"
            % (req.ue_id, act_def_bearer_req.m.pdnInfo.epsBearerId),
        )

        print("Sleeping for 5 seconds")
        time.sleep(5)

        # Dedicated bearer will not be established as the secondary PDN
        # establishment failed
        print(
            "********************** Sending RAR for IMSI",
            "".join([str(i) for i in req.imsi]),
        )
        self._sessionManager_util.send_ReAuthRequest(
            "IMSI" + "".join([str(i) for i in req.imsi]),
            policy_id,
            flow_list,
            qos,
        )

        print("Sleeping for 5 seconds")
        time.sleep(5)
        # Verify that ovs rules are not created for the secondary pdn and
        # dedicated bearer as UE rejected the establishment of secondary pdn

        self._s1ap_wrapper.s1_util.verify_flow_rules(
            num_ul_flows, dl_flow_rules,
        )

        print("Sleeping for 5 seconds")
        time.sleep(5)
        # Now detach the UE
        print(
            "************************* Running UE detach (switch-off) for ",
            "UE id ",
            req.ue_id,
        )
        self._s1ap_wrapper.s1_util.detach(
            req.ue_id,
            s1ap_types.ueDetachType_t.UE_SWITCHOFF_DETACH.value,
            False,
        )


if __name__ == "__main__":
    unittest.main()
