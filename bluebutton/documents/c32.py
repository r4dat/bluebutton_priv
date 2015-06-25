###############################################################################
# Copyright 2015 Kansas Healthcare Collaborative. All rights reserved.
# c32 file is part of the BlueButton.py project.
# Use of c32 source code is governed by the license found in the LICENSE file.
###############################################################################

from .. import documents


def process(c32):
    """
    Preprocesses the CCDA docuemnt
    """
    c32.section = section
    return c32


def section(c32, name):
    """
     Finds the section of a C32 document
     Usually we check first for the HITSP section ID and then for the HL7-CCD ID.
     """

    entries = documents.entries

    if 'document' == name:
        return c32.template('2.16.840.1.113883.3.88.11.32.1')
    if 'allergies' == name:
        el = c32.template('2.16.840.1.113883.3.88.11.83.102')
        if el.is_empty():
            el = c32.template('2.16.840.1.113883.10.20.1.2')

        el.entries = entries
        return el
    if 'demographics' == name:
        return c32.template('2.16.840.1.113883.3.88.11.32.1')
    if 'encounters' == name:
        el = c32.template('2.16.840.1.113883.3.88.11.83.127')
        if el.is_empty():
            el = c32.template('2.16.840.1.113883.10.20.1.3')

        el.entries = entries
        return el
    if 'immunizations' == name:
        el = c32.template('2.16.840.1.113883.3.88.11.83.117')
        if el.is_empty():
            el = c32.template('2.16.840.1.113883.10.20.1.6')

        el.entries = entries
        return el
    if 'results' == name:
        el = c32.template('2.16.840.1.113883.3.88.11.83.122')
        el.entries = entries
        return el
    if 'medications' == name:
        el = c32.template('2.16.840.1.113883.3.88.11.83.112')
        if el.is_empty():
            el = c32.template('2.16.840.1.113883.10.20.1.8')

        el.entries = entries
        return el
    if 'problems' == name:
        el = c32.template('2.16.840.1.113883.3.88.11.83.103')
        if el.is_empty():
            el = c32.template('2.16.840.1.113883.10.20.1.11')

        el.entries = entries
        return el
    if 'procedures' == name:
        el = c32.template('2.16.840.1.113883.3.88.11.83.108')
        if el.is_empty():
            el = c32.template('2.16.840.1.113883.10.20.1.12')

        el.entries = entries
        return el
    if 'vitals' == name:
        el = c32.template('2.16.840.1.113883.3.88.11.83.119')
        if el.is_empty():
            el = c32.template('2.16.840.1.113883.10.20.1.16')

        el.entries = entries
        return el


    return None