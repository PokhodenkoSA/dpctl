#!/bin/bash

# SPDX-FileCopyrightText: 2020 Intel Corporation
#
# SPDX-License-Identifier: MIT

# #shellcheck disable=SC2010
# LATEST_VERSION=$(ls -1 /opt/intel/oneapi/compiler/ | grep -v latest | sort | tail -1)
# # shellcheck source=/dev/null
# source /opt/intel/oneapi/compiler/"$LATEST_VERSION"/env/vars.sh

# #shellcheck disable=SC2010
# LATEST_VERSION=$(ls -1 /opt/intel/oneapi/tbb/ | grep -v latest | sort | tail -1)
# # shellcheck source=/dev/null
# source /opt/intel/oneapi/tbb/"$LATEST_VERSION"/env/vars.sh

export ONEAPI_ROOT=/opt/intel/oneapi

conda build conda-recipe -c intel -c defaults -c conda-forge
