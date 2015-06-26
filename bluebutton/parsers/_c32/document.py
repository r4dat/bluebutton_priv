###############################################################################
# Copyright 2015 Kansas Healthcare Collaborative. All rights reserved.
# This file is part of the BlueButton.py project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

'''/*
 * Parse_r for the C32 document section
 */
'''

def document(c32):

    parse_date = documents.parse_date
    parse_name = documents.parse_name
    parse_address = documents.parse_address


    doc = c32.section('document')

    date = parse_date(doc.tag('effectiveTime').attr('value'))
    title = core.strip_whitespace(doc.tag('title').val())

    author = doc.tag('author')
    el = author.tag('assignedPerson').tag('name')
    name_dict = parse_name(el)
    # Sometimes C32s include names that are just like <name>String</name>
    # and we still want to get something out in that case
    if (not name_dict.prefix and not name_dict.given.length and not name_dict.family):
        name_dict.family = el.val()
    
    
    el = author.tag('addr')
    address_dict = parse_address(el)
    
    el = author.tag('telecom')
    work_phone = el.attr('value')
    
    documentation_of_list = wrappers.ListWrapper()
    performers = doc.tag('documentationOf').elsByTag('performer')
    for p in performers:
    el = p.tag('assignedPerson').tag('name')
    performer_name_dict = parse_name(el)
    performer_phone = p.tag('telecom').attr('value')
    performer_addr = parse_address(el.tag('addr'))
    documentation_of_list.append(wrappers.ObjectWrapper(
        name=performer_name_dict,
        phone=wrappers.ObjectWrapper(
            work=performer_phone
        ),
        address=performer_addr
    ))

    el = doc.tag('encompassingEncounter')
    location_name = core.strip_whitespace(el.tag('name').val())
    location_addr_dict = parse_address(el.tag('addr'))
    
    encounter_date = None
    el = el.tag('effectiveTime')
    if not el.is_empty():
        encounter_date = parse_date(el.attr('value'))
    

    data = wrappers.ObjectWrapper(
        date=date,
        title=title,
        author=wrappers.ObjectWrapper(
            name=name_dict,
            address=address_dict,
            phone=wrappers.ObjectWrapper(
                work=work_phone
            )
        ),
        documentation_of=documentation_of_list,
        location=wrappers.ObjectWrapper(
            name=location_name,
            address=location_addr_dict,
            encounter_date=encounter_date
        )
    )

    return data

