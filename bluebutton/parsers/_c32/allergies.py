"""
Parser for the C32 allergies section
"""
from ...documents import parse_date
from ...core import wrappers


def allergies(c32):
    data = []

    allergies = c32.section('allergies')

    for entry in allergies.entries():
        el = entry.tag('effectiveTime')
        start_date = parse_date(el.tag('low').attr('value')),
        end_date = parse_date(el.tag('high').attr('value'))

        el = entry.template('2.16.840.1.113883.3.88.11.83.6').tag('code')
        name = el.attr('displayName'),
        code = el.attr('code'),
        code_system = el.attr('codeSystem'),
        code_system_name = el.attr('codeSystemName')

        # value => reaction_type
        el = entry.template('2.16.840.1.113883.3.88.11.83.6').tag('value')
        reaction_type_name = el.attr('displayName'),
        reaction_type_code = el.attr('code'),
        reaction_type_code_system = el.attr('codeSystem'),
        reaction_type_code_system_name = el.attr('codeSystemName')

        # reaction
        el = entry.template('2.16.840.1.113883.10.20.1.54').tag('value')
        reaction_name = el.attr('displayName'),
        reaction_code = el.attr('code'),
        reaction_code_system = el.attr('codeSystem')

        # an irregularity seen in some c32s
        if not reaction_name:
            el = entry.template('2.16.840.1.113883.10.20.1.54').tag('text')
            if not el.is_empty():
                reaction_name = Core.stripWhitespace(el.val())

        # severity
        el = entry.template('2.16.840.1.113883.10.20.1.55').tag('value')
        var
        severity = el.attr('displayName')

        # participant => allergen
        el = entry.tag('participant').tag('code')
        allergen_name = el.attr('displayName'),
        allergen_code = el.attr('code'),
        allergen_code_system = el.attr('codeSystem'),
        allergen_code_system_name = el.attr('codeSystemName')

        # another irregularity seen in some c32s
        if not allergen_name:
            el = entry.tag('participant').tag('name')
            if not el.is_empty():
                allergen_name = el.val()

        if not allergen_name:
            el = entry.template('2.16.840.1.113883.3.88.11.83.6').tag('originalText')
            if not el.is_empty():
                allergen_name = Core.stripWhitespace(el.val())

        # status
        el = entry.template('2.16.840.1.113883.10.20.1.39').tag('value')
        var
        status = el.attr('displayName')

        data.append(wrappers.ObjectWrapper(
            date_range=wrappers.ObjectWrapper(
                start=start_date,
                end=end_date
            ),
            name=name,
            code=code,
            code_system=code_system,
            code_system_name=code_system_name,
            status=status,
            severity=severity,
            reaction=wrappers.ObjectWrapper(
                name=reaction_name,
                code=reaction_code,
                code_system=reaction_code_system
            ),
            reaction_type=wrappers.ObjectWrapper(
                name=reaction_type_name,
                code=reaction_type_code,
                code_system=reaction_type_code_system,
                code_system_name=reaction_type_code_system_name
            ),
            allergen=wrappers.ObjectWrapper(
                name=allergen_name,
                code=allergen_code,
                code_system=allergen_code_system,
                code_system_name=allergen_code_system_name
            )
        ))

    return wrappers.ListWrapper(data)
