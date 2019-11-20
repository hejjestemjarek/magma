/**
 * Copyright 2004-present Facebook. All Rights Reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 *
 * @flow
 * @format
 */

import RelayEnvironment from '../common/RelayEnvironment.js';
import {commitMutation, graphql} from 'react-relay';
import type {MutationCallbacks} from './MutationCallbacks.js';
import type {
  RemoveServiceMutationMutationResponse,
  RemoveServiceMutationVariables,
} from './__generated__/RemoveServiceMutation.graphql';

const mutation = graphql`
  mutation RemoveServiceMutation($id: ID!) {
    removeService(id: $id)
  }
`;

export default (
  variables: RemoveServiceMutationVariables,
  callbacks?: MutationCallbacks<RemoveServiceMutationMutationResponse>,
  updater?: (store: any) => void,
) => {
  const {onCompleted, onError} = callbacks ? callbacks : {};
  commitMutation(RelayEnvironment, {
    mutation,
    variables,
    updater,
    onCompleted,
    onError,
  });
};
