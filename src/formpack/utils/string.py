# coding: utf-8
from __future__ import (unicode_literals, print_function,
                        absolute_import, division)

import random
import re
import string
import unicodedata

from ..constants import (
    EXCEL_SHEET_NAME_SIZE_LIMIT, EXCEL_FORBIDDEN_WORKSHEET_NAME_CHARACTERS
)

try:
    unicode = unicode
    basestring = basestring
except NameError:  # Python 3
    basestring = str
    unicode = str

# str_types = (basestring, bytes)
str_types = (basestring,)


def randstr(n):
    return ''.join(random.choice(string.ascii_lowercase + string.digits)
                   for _ in range(n))


# TODO: use a lib for that such as minibelt or ww
def normalize(str_):
    r"""
        Returns a new string withou non ASCII characters, trying to replace
        them with their ASCII closest counter parts when possible.
        :Example:
            >>> normalize(u"H\xe9ll\xf8 W\xc3\xb6rld")
            'Hell World'
        This version use unicodedata and provide limited yet
        useful results.
    """
    str_ = unicodedata.normalize('NFKD', str_).encode('ascii', 'ignore')
    return str_.decode('ascii')


def slugify(str_, separator=r'-'):
    r"""
    Slugify a unicode string using unicodedata to normalize the string.
    :Example:
        >>> slugify(u"H\xe9ll\xf8 W\xc3\xb6rld")
        'hell-world'
        >>> slugify("Bonjour, tout l'monde !", separator="_")
        'bonjour_tout_lmonde'
        >>> slugify("\tStuff with -- dashes and...   spaces   \n")
        'stuff-with-dashes-and-spaces'
    """

    str_ = normalize(str_)
    str_ = re.sub(r'[^\w\s' + separator + ']', '', str_, flags=re.U)
    str_ = str_.strip().lower()
    return re.sub(r'[' + separator + '\s]+', separator, str_, flags=re.U)


def ellipsize(s, max_len, ellipsis='...'):
    r"""
    If necessary, truncate the string `s` and concatenate the result with
    `ellipsis` such that the final string length does not exceed `max_len`.
    :Example:
        >>> ellipsize('This string has more than 31 characters!', max_len=31)
        'This string has more than 31...'
    """

    in_len = len(s)
    ellipsis_len = len(ellipsis)
    if max_len < ellipsis_len:
        raise Exception(
            '`max_len` cannot be less than the length of `ellipsis`')
    if in_len > max_len:
        slice_end = max_len - ellipsis_len
        return s[:slice_end] + ellipsis
    return s


def unique_name_for_xls(sheet_name, other_sheet_names, base_ellipsis='...'):
    r"""
    Return a sheet name that does not collide with any string in the iterable
    `other_sheet_names` and does not exceed the Excel sheet name length limit.
    Characters that are not allowed in sheet names are replaced with
    underscores.
    :Example:
        >>> unique_name_for_xls(
        ...     'This string has more than 31 characters!',
        ...     ('This string has more than 31...',)
        ... )
        'This string has more tha... (1)'
    """

    sheet_name = sheet_name.translate({
        ord(c): '_' for c in EXCEL_FORBIDDEN_WORKSHEET_NAME_CHARACTERS
    })

    candidate = ellipsize(
        sheet_name, EXCEL_SHEET_NAME_SIZE_LIMIT, base_ellipsis)
    i = 1
    while candidate in other_sheet_names:
        candidate = ellipsize(
            sheet_name, EXCEL_SHEET_NAME_SIZE_LIMIT, '{} ({})'.format(
                base_ellipsis, i)
        )
        i += 1
    return candidate
