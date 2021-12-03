// Code generated by go-swagger; DO NOT EDIT.

package wifi_networks

// This file was generated by the swagger tool.
// Editing this file might prove futile when you re-run the swagger generate command

import (
	"fmt"
	"io"

	"github.com/go-openapi/runtime"

	strfmt "github.com/go-openapi/strfmt"

	models "magma/orc8r/cloud/api/v1/go/models"
)

// GetWifiNetworkIDWifiReader is a Reader for the GetWifiNetworkIDWifi structure.
type GetWifiNetworkIDWifiReader struct {
	formats strfmt.Registry
}

// ReadResponse reads a server response into the received o.
func (o *GetWifiNetworkIDWifiReader) ReadResponse(response runtime.ClientResponse, consumer runtime.Consumer) (interface{}, error) {
	switch response.Code() {
	case 200:
		result := NewGetWifiNetworkIDWifiOK()
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		return result, nil
	default:
		result := NewGetWifiNetworkIDWifiDefault(response.Code())
		if err := result.readResponse(response, consumer, o.formats); err != nil {
			return nil, err
		}
		if response.Code()/100 == 2 {
			return result, nil
		}
		return nil, result
	}
}

// NewGetWifiNetworkIDWifiOK creates a GetWifiNetworkIDWifiOK with default headers values
func NewGetWifiNetworkIDWifiOK() *GetWifiNetworkIDWifiOK {
	return &GetWifiNetworkIDWifiOK{}
}

/*GetWifiNetworkIDWifiOK handles this case with default header values.

Wifi configuration of the network
*/
type GetWifiNetworkIDWifiOK struct {
	Payload *models.NetworkWifiConfigs
}

func (o *GetWifiNetworkIDWifiOK) Error() string {
	return fmt.Sprintf("[GET /wifi/{network_id}/wifi][%d] getWifiNetworkIdWifiOK  %+v", 200, o.Payload)
}

func (o *GetWifiNetworkIDWifiOK) GetPayload() *models.NetworkWifiConfigs {
	return o.Payload
}

func (o *GetWifiNetworkIDWifiOK) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	o.Payload = new(models.NetworkWifiConfigs)

	// response payload
	if err := consumer.Consume(response.Body(), o.Payload); err != nil && err != io.EOF {
		return err
	}

	return nil
}

// NewGetWifiNetworkIDWifiDefault creates a GetWifiNetworkIDWifiDefault with default headers values
func NewGetWifiNetworkIDWifiDefault(code int) *GetWifiNetworkIDWifiDefault {
	return &GetWifiNetworkIDWifiDefault{
		_statusCode: code,
	}
}

/*GetWifiNetworkIDWifiDefault handles this case with default header values.

Unexpected Error
*/
type GetWifiNetworkIDWifiDefault struct {
	_statusCode int

	Payload *models.Error
}

// Code gets the status code for the get wifi network ID wifi default response
func (o *GetWifiNetworkIDWifiDefault) Code() int {
	return o._statusCode
}

func (o *GetWifiNetworkIDWifiDefault) Error() string {
	return fmt.Sprintf("[GET /wifi/{network_id}/wifi][%d] GetWifiNetworkIDWifi default  %+v", o._statusCode, o.Payload)
}

func (o *GetWifiNetworkIDWifiDefault) GetPayload() *models.Error {
	return o.Payload
}

func (o *GetWifiNetworkIDWifiDefault) readResponse(response runtime.ClientResponse, consumer runtime.Consumer, formats strfmt.Registry) error {

	o.Payload = new(models.Error)

	// response payload
	if err := consumer.Consume(response.Body(), o.Payload); err != nil && err != io.EOF {
		return err
	}

	return nil
}