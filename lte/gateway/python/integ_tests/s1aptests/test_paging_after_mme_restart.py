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

import time
import unittest

import gpp_types
import s1ap_types
import s1ap_wrapper
from s1ap_utils import MagmadUtil


class TestPagingAfterMmeRestart(unittest.TestCase):
    """Test case validates resumption ueip_imsi map after mme restart"""

    def setUp(self):
        """Initialize"""
        self._s1ap_wrapper = s1ap_wrapper.TestWrapper(
            stateless_mode=MagmadUtil.stateless_cmds.ENABLE,
        )

    def tearDown(self):
        """Cleanup"""
        self._s1ap_wrapper.cleanup()

    def test_paging_after_mme_restart(self):
        """Test case validates resumption ueip_imsi map after mme restart

        Step1 : UE attaches to network
        Step2 : UE moves to idle state
        Step3 : Issue command to restart mme service
        Step4 : Initiate DL data to make MME to send Paging message
        Step5 : In response to Paging message, UE sends Service Request message
        Step6 : Expecting normal flow of DL data
        """
        self._s1ap_wrapper.configUEDevice(1)
        req = self._s1ap_wrapper.ue_req
        ue_id = req.ue_id
        print(
            '************************* Running End to End attach for UE id ',
            ue_id,
        )
        # Now actually complete the attach
        self._s1ap_wrapper.s1_util.attach(
            ue_id,
            s1ap_types.tfwCmd.UE_END_TO_END_ATTACH_REQUEST,
            s1ap_types.tfwCmd.UE_ATTACH_ACCEPT_IND,
            s1ap_types.ueAttachAccept_t,
        )

        # Wait on EMM Information from MME
        self._s1ap_wrapper._s1_util.receive_emm_info()

        # Delay to ensure S1APTester sends attach complete before sending UE
        # context release
        time.sleep(0.5)

        print(
            '************************* Sending UE context release request ',
            'for UE id ',
            ue_id,
        )
        # Send UE context release request to move UE to idle mode
        ue_cntxt_rel_req = s1ap_types.ueCntxtRelReq_t()
        ue_cntxt_rel_req.ue_Id = ue_id
        ue_cntxt_rel_req.cause.causeVal = (
            gpp_types.CauseRadioNetwork.USER_INACTIVITY.value
        )
        self._s1ap_wrapper.s1_util.issue_cmd(
            s1ap_types.tfwCmd.UE_CNTXT_REL_REQUEST, ue_cntxt_rel_req,
        )
        response = self._s1ap_wrapper.s1_util.get_response()
        self.assertEqual(
            response.msg_type, s1ap_types.tfwCmd.UE_CTX_REL_IND.value,
        )
        wait_time = 0.3
        time.sleep(wait_time)
        print('************************* Restarting MME service on', 'gateway')
        wait_for_restart = 20
        self._s1ap_wrapper.magmad_util.restart_services(
            ["mme"], wait_for_restart,
        )

        print(
            '************************* Running UE downlink (UDP) for UE id ',
            ue_id,
        )
        with self._s1ap_wrapper.configDownlinkTest(
            req, duration=1, is_udp=True,
        ) as test:
            response = self._s1ap_wrapper.s1_util.get_response()
            self.assertTrue(response, s1ap_types.tfwCmd.UE_PAGING_IND.value)
            print('************************ Received Paging Indication')

            # Send service request to reconnect UE
            ser_req = s1ap_types.ueserviceReq_t()
            ser_req.ue_Id = ue_id
            ser_req.ueMtmsi = s1ap_types.ueMtmsi_t()
            ser_req.ueMtmsi.pres = False
            ser_req.rrcCause = s1ap_types.Rrc_Cause.TFW_MT_ACCESS.value
            self._s1ap_wrapper.s1_util.issue_cmd(
                s1ap_types.tfwCmd.UE_SERVICE_REQUEST, ser_req,
            )
            # Ignore PAGING_IND and wait for INT_CTX_SETUP_IND
            response = self._s1ap_wrapper.s1_util.get_response()
            while response.msg_type == s1ap_types.tfwCmd.UE_PAGING_IND.value:
                print(
                    "Received Paging Indication for ue-id", ue_id,
                )
                response = self._s1ap_wrapper.s1_util.get_response()

            self.assertEqual(
                response.msg_type, s1ap_types.tfwCmd.INT_CTX_SETUP_IND.value,
            )
            test.verify()

        time.sleep(0.5)
        # Now detach the UE
        self._s1ap_wrapper.s1_util.detach(
            ue_id, s1ap_types.ueDetachType_t.UE_NORMAL_DETACH.value,
            wait_for_s1_ctxt_release=True,
        )
        time.sleep(0.5)


if __name__ == '__main__':
    unittest.main()
