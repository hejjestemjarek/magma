/*
Copyright 2022 The Magma Authors.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package sas

import (
	"magma/dp/cloud/go/services/dp/active_mode_controller/action_generator/action"
	"magma/dp/cloud/go/services/dp/storage"
)

type DeregistrationRequestGenerator struct{}

func (*DeregistrationRequestGenerator) GenerateActions(_ *storage.DetailedCbsd) []action.Action {
	return []action.Action{}
}

func (*DeregistrationRequestGenerator) GenerateRequests(cbsd *storage.DetailedCbsd) []*storage.MutableRequest {
	payload := &DeregistrationRequest{
		CbsdId: cbsd.Cbsd.CbsdId.String,
	}
	req := makeRequest(Deregistration, payload)
	return []*storage.MutableRequest{req}
}

type DeregistrationRequest struct {
	CbsdId string `json:"cbsdId"`
}
