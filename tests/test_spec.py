import ConfigParser
import os

import pytest
from cli import exceptions
from cli import spec
from cli.spec import ValueArgument


@pytest.mark.parametrize("res_args, options, req_args, nonreq_args", [
    [{'host': spec.ValueArgument(),
      'command0': 'virsh',
      'ssh-user': spec.ValueArgument()},
     {
         'host': {'help': 'help', 'required': True},
         'ssh-user': {'help': 'help2', 'required': True},
         'ssh-key': {'help': 'help3', 'default': 'id_rsa'}
     }, ['host', 'ssh-user'], ['ssh-key']],
])
def test_required_option_exception(res_args,
                                   options,
                                   req_args,
                                   nonreq_args):

    with pytest.raises(exceptions.IRConfigurationException) as ex_info:
        spec.override_default_values(res_args, options)

    for arg in req_args:
        assert arg in ex_info.value.message

    for arg in nonreq_args:
        assert arg not in ex_info.value.message


@pytest.mark.parametrize("res_args, options, expected_args", [
    # data set #1
    [{'host': None,
      'command0': 'virsh',
      'from-file': {
          'virsh': {
              'host': 'earth',
          }
      },
      'ssh-user': 'root',
      'ssh-key': None},
     {'virsh': {
         'host': {'help': 'help', 'required': True},
         'ssh-user': {'help': 'help2', 'required': True},
         'ssh-key': {'help': 'help3', 'required': True, 'default': 'id_rsa'}
     }},
     {'host': 'earth',
      'command0': 'virsh',
      'from-file': {
          'virsh': {
              'host': 'earth',
          }
      },
      'ssh-user': 'id_rsa'}],

    # todo(yfried): enable this in the future
    # [{'host': None,
    #   'command0': 'virsh',
    #   'from-file': {
    #       'virsh': {
    #           'host': 'earth',
    #       }
    #   },
    #   'ssh-user': None,
    #   'ssh-key': None},
    #  {'virsh': {
    #      'opt1': {'requires_only': ['host']},
    #      'host': {'help': 'help', 'required': True},
    #      'ssh-user': {'help': 'help2', 'required': True},
    #      'ssh-key': {'help': 'help3', 'required': True, 'default': 'id_rsa'}
    #  }},
    #  {'host': 'earth',
    #   'command0': 'virsh',
    #   'from-file': {
    #       'virsh': {
    #           'host': 'earth',
    #       }
    #   },
    #   'ssh-user': 'id_rsa'}]
])
def test_required_options_are_set(res_args,
                                  options,
                                  expected_args):
    actual_args = spec.override_default_values(res_args, options)
    cmp(actual_args, expected_args)


@pytest.mark.parametrize('test_value', [
  'test string', 1, 0.1
])
def test_value_argument_compare(test_value):
    val = ValueArgument(test_value)

    # verify several equality checks
    assert val == test_value
    assert val in [test_value, ]

    # negative case
    val = ValueArgument(0)
    assert val != test_value
    assert val not in [test_value, ]
