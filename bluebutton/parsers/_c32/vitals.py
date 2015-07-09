###############################################################################
# Copyright 2015 Kansas Healthcare Collaborative. All rights reserved.
# This file is part of the BlueButton.py project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

"""
Parser for the C32 vitals section
"""

from ...documents import parse_date
from ...core import wrappers
from ... import documents

def vitals(c32):
  
    parse_date = documents.parse_date
    parse_name = documents.parse_name
    parse_address = documents.parse_address
    data = wrappers.ListWrapper()
  
    vitals = c32.section('vitals')
  
    for entry in vitals.entries():
        el = entry.tag('effectivetime')
        entry_date = parse_date(el.attr('value'))
    
        # result
        results = entry.els_by_tag('component')
        results_data = wrappers.ListWrapper()
    
        for result in results:
            # results

            el = result.tag('code')
            name = el.attr('displayName'),
            code = el.attr('code'),
            code_system = el.attr('codeSystem'),
            code_system_name = el.attr('codeSystemName')
      
            el = result.tag('value')
            value = wrappers.parse_number(el.attr('value')),
            unit = el.attr('unit')
      
            results_data.append(wrappers.ObjectWrapper(
                name=name,
                code=code,
                code_system=code_system,
                code_system_name=code_system_name,
                value=value,
                unit=unit
            ))
    
        data.append(wrappers.ObjectWrapper(
            date=entry_date,
            results=results_data
        ))

    return data