###############################################################################
# Copyright 2015 Kansas Healthcare Collaborative. All rights reserved.
# This file is part of the BlueButton.py project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

"""
Parser for the c32 problems section
"""

from ...core import wrappers
from ... import core
from ... import documents

def problems(c32):
  
    parse_date = documents.parse_date
    data = wrappers.ListWrapper()
    
  
    problems = c32.section('problems')
  
    for entry in problems.entries():

        el = entry.tag('effectivetime')
        start_date = parse_date(el.tag('low').attr('value')),
        end_date = parse_date(el.tag('high').attr('value'))

        el = entry.template('2.16.840.1.113883.10.20.1.28').tag('value')
        name = el.attr('displayName'),
        code = el.attr('code'),
        code_system = el.attr('codeSystem'),
        code_system_name = el.attr('codeSystemName')

        # pre-c32 ccds put the problem name in this "originaltext" field, and some vendors
        # continue doing this with their c32, even though it's not technically correct
        if not name:
            el = entry.template('2.16.840.1.113883.10.20.1.28').tag('originaltext')
            if not el.is_empty():
                name = core.strip_whitespace(el.val())

        el = entry.template('2.16.840.1.113883.10.20.1.28').tag('translation')
        translation_name = el.attr('displayName'),
        translation_code = el.attr('code'),
        translation_code_system = el.attr('codeSystem'),
        translation_code_system_name = el.attr('codeSystemName')

        el = entry.template('2.16.840.1.113883.10.20.1.50')
        status = el.tag('value').attr('displayName')

        age = None
        el = entry.template('2.16.840.1.113883.10.20.1.38')
        if not el.is_empty():
            age = wrappers.parse_number(el.tag('value').attr('value'))

        data.append(wrappers.ObjectWrapper(
            date_range=wrappers.ObjectWrapper(
                start=start_date,
                end=end_date
            ),
            name=name,
            status=status,
            age=age,
            code=code,
            code_system=code_system,
            code_system_name=code_system_name,
            translation=wrappers.ObjectWrapper(
                name=translation_name,
                code=translation_code,
                code_system=translation_code_system,
                code_system_name=translation_code_system_name
            ),
            comment=comment
        ))

    return data
