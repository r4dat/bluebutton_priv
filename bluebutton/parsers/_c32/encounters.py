###############################################################################
# copyright 2015 kansas healthcare collaborative. all rights reserved.
# this file is part of the bluebutton.py project.
# use of this source code is governed by the license found in the license file.
###############################################################################

'''/*
 * parser for the c32 encounters section
 */'''


def encounters(c32):
    data[]
    parse_date = documents.parse_date
    parse_name = documents.parse_name
    parse_address = documents.parse_address

    encounters = c32.section('encounters')


    for entry in encounters.entries():
        date = parse_date(entry.tag('effectiveTime').attr('value'))
        if not date:
            date = parse_date(entry.tag('effectiveTime').tag('low').attr('value'))
    
        el = entry.tag('code')
        name = el.attr('displayName')
        code = el.attr('code')
        code_system = el.attr('codeSystem')
        code_system_name = el.attr('codeSystemName')
        code_system_version = el.attr('codeSystemVersion')
    
        # translation
        el = entry.tag('translation')
        translation_name = el.attr('displayName')
        translation_code = el.attr('code')
        translation_code_system = el.attr('codeSystem')
        translation_code_system_name = el.attr('codeSystemName')

        # performer
        el = entry.tag('performer')
        performer_name = el.tag('name').val()
        performer_code = el.attr('code')
        performer_code_system = el.attr('codeSystem')
        performer_code_system_name = el.attr('codeSystemName')

        # participant => location
        el = entry.tag('participant')
        organization = el.tag('name').val()
        location_dict = parse_address(el)
        location_dict.organization = organization
        
        # findings
        findings = []
        findings_els = entry.els_by_tag('entryRelationship')
        for current in findings_els:
            el = current.tag('value')
            findings.append(wrappers.ObjectWrapper(
                name=el.attr('displayName'),
                code=el.attr('code'),
                code_system=el.attr('codeSystem'),
            ))
        
        data.append(wrappers.ObjectWrapper(
            date=date,
            name=name,
            code=code,
            code_system=code_system,
            code_system_name=code_system_name,
            code_system_version=code_system_version,
            findings=findings,
            translation=wrappers.ObjectWrapper(
                name=translation_name,
                code=translation_code,
                code_system=translation_code_system,
                code_system_name=translation_code_system_name
            ),
            performer=wrappers.ObjectWrapper(
                name=performer_name,
                code=performer_code,
                code_system=performer_code_system,
                code_system_name=performer_code_system_name
            ),
            location=location_dict
        ))

    return wrappers.ListWrapper(data)
