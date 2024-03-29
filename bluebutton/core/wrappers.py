###############################################################################
# Copyright 2015 University of Florida. All rights reserved.
# This file is part of the BlueButton.py project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

"""
Classes and functions that make ported code look more like original JavaScript
"""

import datetime
import json


class FixedOffset(datetime.tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset, name):
        self.__offset = datetime.timedelta(minutes=offset)
        self.__name = name

    @classmethod
    def UTC(cls):
        return cls(0, 'UTC')

    @classmethod
    def from_string(cls, tz):
        stripped = str(tz).strip()

        if not stripped or 'Z' == stripped:
            return cls.UTC()

        hour = int(stripped[1:3])
        minutes = hour*60 + int(stripped[3:5])
        if stripped[0] == '-':
            minutes *= -1

        return cls(minutes, stripped)

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return datetime.timedelta(0)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            utc = (o - o.utcoffset()).replace(tzinfo=FixedOffset.UTC())
            if utc.hour == 0 and utc.minute == 0 and utc.second == 0:
                return self.default(datetime.date(utc.year, utc.month, utc.day))
            return utc.isoformat().replace('+00:00', 'Z')
        elif isinstance(o, datetime.date):
            return o.strftime("%m/%d/%Y")
        elif isinstance(o, ObjectWrapper):
            return o.__dict__

        return json.JSONEncoder.default(self, o)


class ObjectWrapper(object):
    def __init__(self, **kwargs):
        for keyword, value in kwargs.iteritems():
            setattr(self, keyword, value)

    def __setattr__(self, key, value):
        val = value
        if callable(value):
            method = value.__get__(self, self.__class__)
            val = method
        object.__setattr__(self, key, val)

    def json(self):
        return json.dumps(self, cls=JSONEncoder)


class ListWrapper(list):
    def json(self):
        return json.dumps(self, cls=JSONEncoder)


def parse_number(s):
    """
    Somewhat mimics JavaScript's parseFloat() functionality
    """
    if not s:
        return None
    value = float(s)
    return int(value) if value == int(value) else value

def is_number(s):
    #Return None for 0 even though 0 may be valid. (0 cancer cells from histology slide)
    if not s:
        return None
    try:
        float(s)
        return True
    except:
        return False