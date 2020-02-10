// Copyright (c) 2004-present Facebook All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

package graphhttp

import (
	"fmt"
	"net/http"

	"github.com/facebookincubator/symphony/graph/exporter"
	"github.com/facebookincubator/symphony/graph/graphql"
	"github.com/facebookincubator/symphony/graph/importer"
	"github.com/facebookincubator/symphony/graph/viewer"
	"github.com/facebookincubator/symphony/pkg/actions"
	"github.com/facebookincubator/symphony/pkg/actions/executor"
	"github.com/facebookincubator/symphony/pkg/log"

	"github.com/gorilla/mux"
)

type routerConfig struct {
	tenancy viewer.Tenancy
	logger  log.Logger
	orc8r   struct{ client *http.Client }
	actions struct{ registry *executor.Registry }
}

func newRouter(cfg routerConfig) (*mux.Router, error) {
	router := mux.NewRouter()
	router.Use(
		func(h http.Handler) http.Handler {
			return viewer.TenancyHandler(h, cfg.tenancy)
		},
		func(h http.Handler) http.Handler {
			return actions.Handler(h, cfg.logger, cfg.actions.registry)
		},
	)
	handler, err := importer.NewHandler(cfg.logger)
	if err != nil {
		return nil, fmt.Errorf("creating import handler: %w", err)
	}
	router.PathPrefix("/import/").
		Handler(http.StripPrefix("/import", handler)).
		Name("import")

	if handler, err = exporter.NewHandler(cfg.logger); err != nil {
		return nil, fmt.Errorf("creating export handler: %w", err)
	}
	router.PathPrefix("/export/").
		Handler(http.StripPrefix("/export", handler)).
		Name("export")

	if handler, err = graphql.NewHandler(cfg.logger, cfg.orc8r.client); err != nil {
		return nil, fmt.Errorf("creating graphql handler: %w", err)
	}
	router.PathPrefix("/").
		Handler(handler).
		Name("root")

	return router, nil
}
