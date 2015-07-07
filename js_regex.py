# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 12:19:08 2015

@author: RobR
"""
import re
out=open(r'C:\Users\robrutherford\Documents\bluebutton_priv\bluebutton\parsers\_c32\imm_out.py','w')

with open(r'C:\Users\robrutherford\Documents\bluebutton_priv\bluebutton\parsers\_c32\immunizations.py') as f:
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
        
        #dat = re.sub('for \(var i.*performers.*\{','for el in performers:',dat)
        out.write(dat)
        
out.close