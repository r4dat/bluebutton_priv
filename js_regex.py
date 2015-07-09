# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 12:19:08 2015

@author: RobR
"""
import re
out=open(r'C:\Users\robrutherford\Documents\bluebutton_priv\bluebutton\parsers\_c32\vit_out.py','w')

with open(r'C:\Users\robrutherford\Documents\bluebutton_priv\bluebutton\parsers\_c32\vitals.js') as f:
    for line in f:
        dat = line
        # Fix C style comments.
        dat = re.sub('//','#',dat)

        # Fix C style long comment.
        dat = re.sub('\/\*','\'\'\'',dat)
        dat = re.sub('\*\/','\'\'\'',dat)

        # Def function
        dat = re.sub('.*\.([a-z]*).*(c32).*','def \\1(\\2):',dat)

        # Fix initial boolean syntax.
        dat = re.sub('if \(\!([a-z]*)\) \{','if not \\1:',dat)

        #Remove '  var '
        dat = re.sub('  var ','    ',dat)
        
        #Replace parseDate,Name,Address with parse_*
        dat = re.sub('(parse)([A-Z][a-z]*)','\\1_\\2',dat).lower()
        
        #Replace Core.stripWhitespace with pythonized shim.
        dat = re.sub('(Core\.strip)(W[a-z]*)','\\1_\\2',dat).lower()
        
        dat = re.sub('documentation_of_list = \[\]','documentation_of_list = wrappers.ListWrapper()',dat)
        
        dat = re.sub(';','',dat)

        # Replace JS funcs with python shim funcs.
        dat = re.sub('el.boolattr','el.bool_attr',dat)
        dat = re.sub('elsbytag','els_by_tag',dat)
        dat = re.sub('parse_float','wrappers.parse_number',dat)

        #Replace JS for item in collection syntax with python version.
        dat = re.sub('([a-z]*\.entries\(\)).* \{','for entry in \\1:',dat)

        # Replace null with None
        dat = re.sub('null','None',dat)

        # Fix camelCase keys.
        dat = re.sub('codesystem','codeSystem',dat)
        dat = re.sub('displayname','displayName',dat)
        dat = re.sub('ratequantity','rateQuantity',dat)
        dat = re.sub('codesystemname','codeSystemName',dat)
        dat=re.sub('originaltext','originalText',dat)


        #dat = re.sub('for \(var i.*performers.*\{','for el in performers:',dat)
        dat = re.sub('\: ','=',dat)
        out.write(dat)
        
out.close