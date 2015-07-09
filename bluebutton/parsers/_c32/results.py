###############################################################################
# Copyright 2015 Kansas Healthcare Collaborative. All rights reserved.
# This file is part of the BlueButton.py project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

"""
Parser for the C32 results section
"""

from ...documents import parse_date
from ...core import wrappers
from ... import documents

def results(c32):
  
    parse_date = documents.parse_date
    parse_name = documents.parse_name
    parse_address = documents.parse_address
    data = wrappers.ListWrapper()

    results = c32.section('results')
  
    for entry in results.entries():
        el = entry.tag('effectivetime')
        panel_date = parse_date(entry.tag('effectivetime').attr('value'))
        if not panel_date:
            panel_date = parse_date(entry.tag('effectivetime').tag('low').attr('value'))

        # panel
        el = entry.tag('code')
        panel_name = el.attr('displayName'),
        panel_code = el.attr('code'),
        panel_code_system = el.attr('codeSystem'),
        panel_code_system_name = el.attr('codeSystemname')

        # observation
        tests = entry.els_by_tag('observation')
        tests_data = wrappers.ListWrapper()

        for observation in tests:
        # sometimes results organizers contain non-results. we only want tests
            if (observation.template('2.16.840.1.113883.10.20.1.31').val()):
                date = parse_date(observation.tag('effectivetime').attr('value'))

                el = observation.tag('code')
                name = el.attr('displayName'),
                code = el.attr('code'),
                code_system = el.attr('codeSystem'),
                code_system_name = el.attr('codeSystemname')

                if not name:
                    name = core.strip_whitespace(observation.tag('text').val())


                el = observation.tag('translation')
                translation_name = el.attr('displayName'),
                translation_code = el.attr('code'),
                translation_code_system = el.attr('codeSystem'),
                translation_code_system_name = el.attr('codeSystemname')

                el = observation.tag('value')
                value = el.attr('value'),
                unit = el.attr('unit')
                # we could look for xsi:type="pq" (physical quantity) but it seems better
                # not to trust that that field has been used correctly...
                if value and wrappers.parse_number(value):
                    value = wrappers.parse_number(value)

                if not value:
                  value = el.val() # look for free-text values

                el = observation.tag('referencerange')
                reference_range_text = core.strip_whitespace(el.tag('observationrange').tag('text').val()),
                reference_range_low_unit = el.tag('observationrange').tag('low').attr('unit'),
                reference_range_low_value = el.tag('observationrange').tag('low').attr('value'),
                reference_range_high_unit = el.tag('observationrange').tag('high').attr('unit'),
                reference_range_high_value = el.tag('observationrange').tag('high').attr('value')

                tests_data.append(wrappers.ObjectWrapper(
                date=date,
                name=name,
                value=value,
                unit=unit,
                code=code,
                code_system=code_system,
                code_system_name=code_system_name,
                translation=wrappers.ObjectWrapper(
                    name=translation_name,
                    code=translation_code,
                    code_system=translation_code_system,
                    code_system_name=translation_code_system_name
                    ),
                reference_range=wrappers.ObjectWrapper(
                    text=reference_range_text,
                    low_unit=reference_range_low_unit,
                    low_value=reference_range_low_value,
                    high_unit=reference_range_high_unit,
                    high_value=reference_range_high_value
                    )
            ))

        data.append(wrappers.ObjectWrapper(
            name=panel_name,
            code=panel_code,
            code_system=panel_code_system,
            code_system_name=panel_code_system_name,
            date=panel_date,
            tests=tests_data
            ))

    return data

