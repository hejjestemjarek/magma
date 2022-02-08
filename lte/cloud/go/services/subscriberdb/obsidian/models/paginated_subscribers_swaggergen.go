// Code generated by go-swagger; DO NOT EDIT.

package models

// This file was generated by the swagger tool.
// Editing this file might prove futile when you re-run the swagger generate command

import (
	strfmt "github.com/go-openapi/strfmt"

	"github.com/go-openapi/errors"
	"github.com/go-openapi/swag"
	"github.com/go-openapi/validate"
)

// PaginatedSubscribers Page of subscribers
// swagger:model paginated_subscribers
type PaginatedSubscribers struct {

	// next page token
	// Required: true
	NextPageToken PageToken `json:"next_page_token"`

	// subscribers
	// Required: true
	Subscribers map[string]*Subscriber `json:"subscribers"`

	// estimated total number of subscriber entries
	// Required: true
	TotalCount int64 `json:"total_count"`
}

// Validate validates this paginated subscribers
func (m *PaginatedSubscribers) Validate(formats strfmt.Registry) error {
	var res []error

	if err := m.validateNextPageToken(formats); err != nil {
		res = append(res, err)
	}

	if err := m.validateSubscribers(formats); err != nil {
		res = append(res, err)
	}

	if err := m.validateTotalCount(formats); err != nil {
		res = append(res, err)
	}

	if len(res) > 0 {
		return errors.CompositeValidationError(res...)
	}
	return nil
}

func (m *PaginatedSubscribers) validateNextPageToken(formats strfmt.Registry) error {

	if err := m.NextPageToken.Validate(formats); err != nil {
		if ve, ok := err.(*errors.Validation); ok {
			return ve.ValidateName("next_page_token")
		}
		return err
	}

	return nil
}

func (m *PaginatedSubscribers) validateSubscribers(formats strfmt.Registry) error {

	for k := range m.Subscribers {

		if err := validate.Required("subscribers"+"."+k, "body", m.Subscribers[k]); err != nil {
			return err
		}
		if val, ok := m.Subscribers[k]; ok {
			if err := val.Validate(formats); err != nil {
				return err
			}
		}

	}

	return nil
}

func (m *PaginatedSubscribers) validateTotalCount(formats strfmt.Registry) error {

	if err := validate.Required("total_count", "body", int64(m.TotalCount)); err != nil {
		return err
	}

	return nil
}

// MarshalBinary interface implementation
func (m *PaginatedSubscribers) MarshalBinary() ([]byte, error) {
	if m == nil {
		return nil, nil
	}
	return swag.WriteJSON(m)
}

// UnmarshalBinary interface implementation
func (m *PaginatedSubscribers) UnmarshalBinary(b []byte) error {
	var res PaginatedSubscribers
	if err := swag.ReadJSON(b, &res); err != nil {
		return err
	}
	*m = res
	return nil
}