###############################################################################
# Copyright 2015 Kansas Healthcare Collaborative. All rights reserved.
# This file is part of the BlueButton.py project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

"""
Parser for the C32 allergies section
"""
from ...documents import parse_date
from ...core import wrappers
from ... import documents
from ... import core

def procedures(c32):
  
    parse_date = documents.parse_date
    parse_name = documents.parse_name
    parse_address = documents.parse_address
    data = wrappers.ListWrapper()

  
    procedures = c32.section('procedures')
  
    for entry in procedures.entries():
        el = entry.tag('effectivetime')
        date = parse_date(el.attr('value'))

        el = entry.tag('code')
        name = el.attr('displayName'),
        code = el.attr('code'),
        code_system = el.attr('codeSystem')

        if not name:
            name = core.strip_whitespace(entry.tag('originalText').val())

        # 'specimen' tag not always present
        # el = entry.tag('specimen').tag('code')
        # var specimen_name = el.attr('displayName'),
        #     specimen_code = el.attr('code'),
        #     specimen_code_system = el.attr('codeSystem')
        specimen_name = None,
        specimen_code = None,
        specimen_code_system = None

        el = entry.tag('performer').tag('addr')
        organization = el.tag('name').val(),
        phone = el.tag('telecom').attr('value')

        performer_dict = parse_address(el)
        performer_dict.organization = organization
        performer_dict.phone = phone

        # participant => device
        el = entry.tag('participant').tag('code')
        device_name = el.attr('displayName'),
        device_code = el.attr('code'),
        device_code_system = el.attr('codeSystem')

        data.append(wrappers.ObjectWrapper(
            date=date,
            name=name,
            code=code,
            code_system=code_system,
            specimen=wrappers.ObjectWrapper(
                name=specimen_name,
                code=specimen_code,
                code_system=specimen_code_system
            ),
            performer=performer_dict,
            device=wrappers.ObjectWrapper(
                name=device_name,
                code=device_code,
                code_system=device_code_system
            )
        ))

    return data