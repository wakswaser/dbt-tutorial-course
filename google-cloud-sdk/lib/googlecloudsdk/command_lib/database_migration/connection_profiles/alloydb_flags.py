# -*- coding: utf-8 -*- #
# Copyright 2022 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Flags and helpers for AlloyDB Connection Profiles related commands."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import arg_parsers

_IP_ADDRESS_PART = r'(25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})'  # Match decimal 0-255
_CIDR_PREFIX_PART = r'([0-9]|[1-2][0-9]|3[0-2])'  # Match decimal 0-32
# Matches either IPv4 range in CIDR notation or a naked IPv4 address.
_CIDR_REGEX = r'{addr_part}(\.{addr_part}){{3}}(\/{prefix_part})?$'.format(
    addr_part=_IP_ADDRESS_PART, prefix_part=_CIDR_PREFIX_PART
)


def AddEnablePublicIpFlag(parser):
  """Adds a --enable-public-ip flag to the given parser."""
  help_text = """\
    If true, the AlloyDB instance will be accessible via public IP.
    """
  parser.add_argument(
      '--enable-public-ip',
      required=False,
      action='store_true',
      dest='enable_public_ip',
      default=False,
      help=help_text,
  )


def AddEnableOutboundPublicIpFlag(parser):
  """Adds a --enable-outbound-public-ip flag to the given parser."""
  help_text = """\
    If true, Enables an outbound public IP address to support a database
    server sending requests out into the internet.
    """
  parser.add_argument(
      '--enable-outbound-public-ip',
      required=False,
      action='store_true',
      dest='enable_outbound_public_ip',
      default=False,
      help=help_text,
  )


def AddAuthorizedNetworkCidrRangesFlag(parser):
  """Adds a --authorized-network-cidr-ranges flag to the given parser."""
  cidr_validator = arg_parsers.RegexpValidator(
      _CIDR_REGEX,
      (
          'Must be specified in CIDR notation, also known as '
          "'slash' notation (e.g. 192.168.100.0/24)."
      ),
  )
  help_text = """\
    Comma-separated list of CIDR ranges that can connect to the AlloyDB instance.
    """
  parser.add_argument(
      '--authorized-network-cidr-ranges',
      required=False,
      type=arg_parsers.ArgList(element_type=cidr_validator),
      metavar='NETWORK',
      default=[],
      help=help_text,
  )


def AddPasswordFlag(parser):
  """Add the password field to the parser."""
  parser.add_argument(
      '--password',
      required=True,
      help="Initial password for the 'postgres' user.")


def AddNetworkFlag(parser):
  """Adds a --network flag to the given parser."""
  help_text = """\
    The VPC network from which the AlloyDB instance is accessible via private
    IP. For example, projects/myProject/global/networks/default. This setting
    cannot be updated after it is set.
    """
  parser.add_argument('--network', help=help_text)


def AddClusterLabelsFlag(parser):
  """Adds a --cluster-labels flag to the given parser."""
  help_text = """\
    The resource labels for an AlloyDB cluster. An object containing a list
    of "key": "value" pairs.
    """
  parser.add_argument(
      '--cluster-labels',
      metavar='KEY=VALUE',
      type=arg_parsers.ArgDict(),
      help=help_text)


def AddPrimaryIdFlag(parser):
  """Adds a --primary-id flag to the given parser."""
  help_text = """\
    The ID of the primary instance for this AlloyDB cluster.
    """
  parser.add_argument('--primary-id', help=help_text, required=True)


def AddCpuCountFlag(parser):
  """Adds a --cpu-count flag to the given parser."""
  help_text = """\
    Whole number value indicating how many vCPUs the machine should
    contain. Each vCPU count corresponds to a N2 high-mem machine:
    (https://cloud.google.com/compute/docs/general-purpose-machines#n2_machines).
  """
  parser.add_argument(
      '--cpu-count',
      help=help_text,
      type=int,
      choices=[2, 4, 8, 16, 32, 64],
      required=True)


def AddDatabaseFlagsFlag(parser):
  """Adds a --database-flags flag to the given parser."""
  help_text = """\
    Comma-separated list of database flags to set on the AlloyDB primary
    instance. Use an equals sign to separate the flag name and value. Flags
    without values, like skip_grant_tables, can be written out without a value,
    e.g., `skip_grant_tables=`. Use on/off values for booleans. View AlloyDB's
    documentation for allowed flags (e.g., `--database-flags
    max_allowed_packet=55555,skip_grant_tables=,log_output=1`).
  """
  parser.add_argument(
      '--database-flags',
      type=arg_parsers.ArgDict(),
      metavar='FLAG=VALUE',
      help=help_text)


def AddPrimaryLabelsFlag(parser):
  """Adds a --primary-labels flag to the given parser."""
  help_text = """\
    The resource labels for an AlloyDB primary instance. An object containing a
    list of "key": "value" pairs.
    """
  parser.add_argument(
      '--primary-labels',
      metavar='KEY=VALUE',
      type=arg_parsers.ArgDict(),
      help=help_text)


def AddDatabaseVersionFlag(parser):
  """Adds a --database-version flag to the given parser."""
  help_text = 'Database engine major version.'
  choices = [
      'POSTGRES_14',
      'POSTGRES_15',
      'POSTGRES_16',
      'POSTGRES_17',
  ]

  parser.add_argument('--database-version', help=help_text, choices=choices)
