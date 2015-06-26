###############################################################################
# Copyright 2015 Kansas Healthcare Collaborative. All rights reserved.
# This file is part of the BlueButton.py project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

'''/*
 * Parser for the C32 encounters section
 */'''

Parsers.C32.encounters = function (c32) {
  
  var parseDate = Documents.parseDate;
  var parseName = Documents.parseName;
  var parseAddress = Documents.parseAddress;
  var data = [], el;
  
  var encounters = c32.section('encounters');
  
  encounters.entries().each(function(entry) {
    
    var date = parseDate(entry.tag('effectiveTime').attr('value'));
    if (!date) {
      date = parseDate(entry.tag('effectiveTime').tag('low').attr('value'));
    }
    
    el = entry.tag('code');
    var name = el.attr('displayName'),
        code = el.attr('code'),
        code_system = el.attr('codeSystem'),
        code_system_name = el.attr('codeSystemName'),
        code_system_version = el.attr('codeSystemVersion');
    
    // translation
    el = entry.tag('translation');
    var translation_name = el.attr('displayName'),
        translation_code = el.attr('code'),
        translation_code_system = el.attr('codeSystem'),
        translation_code_system_name = el.attr('codeSystemName');
    
    // performer
    el = entry.tag('performer');
    var performer_name = el.tag('name').val(),
        performer_code = el.attr('code'),
        performer_code_system = el.attr('codeSystem'),
        performer_code_system_name = el.attr('codeSystemName');
    
    // participant => location
    el = entry.tag('participant');
    var organization = el.tag('name').val(),
        location_dict = parseAddress(el);
    location_dict.organization = organization;

    // findings
    var findings = [];
    var findingEls = entry.elsByTag('entryRelationship');
    for (var i = 0; i < findingEls.length; i++) {
      el = findingEls[i].tag('value');
      findings.push({
        name: el.attr('displayName'),
        code: el.attr('code'),
        code_system: el.attr('codeSystem')
      });
    }
    
    data.push({
      date: date,
      name: name,
      code: code,
      code_system: code_system,
      code_system_name: code_system_name,
      code_system_version: code_system_version,
      findings: findings,
      translation: {
        name: translation_name,
        code: translation_code,
        code_system: translation_code_system,
        code_system_name: translation_code_system_name
      },
      performer: {
        name: performer_name,
        code: performer_code,
        code_system: performer_code_system,
        code_system_name: performer_code_system_name
      },
      location: location_dict
    });
  });
  
  return data;
};