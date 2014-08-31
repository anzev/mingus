#!/usr/bin/python
# -*- coding: utf-8 -*-

#    mingus - Music theory Python package, generate_wiki_docs module.
#    Copyright (C) 2008, 2009, Bart Spaans
#    Copyright (C) 2011, Carlo Stemberger
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Script for updating the automatically generated documentation.

This module builds the reference documentation for mingus.
"""

import mingus
from mingus.core import *
from mingus.containers import *
from mingus.extra import *
from mingus.midi import *
import types
import inspect
import sys
import os
import inspect

class Documize(object):

    """Generate documents from modules."""

    functions = []
    classes = []
    attributes = []

    def __init__(self, module_string=''):
        self.set_module(module_string)

    def format_code_examples(self, text):
        pass

    def generate_module_wikidocs(self):
        self.reset()
        res = '#summary Reference documentation for `{0}`.\n'.format(
                self.module_string)
        res += '----\n= {0} =\n{1}\n----\n'.format(self.module_string,
                self.module.__doc__)

        # Gather all the documentation
        for element in dir(self.module):
            e = eval('{0}.{1}'.format(self.module_string, element))
            if not callable(e):
                self.generate_non_callable_docs(element, e)
            else:
                self.generate_callable_wikidocs(element, e)

        # Order it
        self.functions.sort()
        self.classes.sort()
        self.attributes.sort()

        # Present attributes
        if len(self.attributes) != 0:
            res += '== Attributes ==\n'
            for a in self.attributes:
                res += a
            res += '----\n'

        # Present functions
        if len(self.functions) != 0:
            res += '== Functions ==\n'
            for f in self.functions:
                res += f
            res += '----\n'
        res += '[mingusIndex Back to Index]\n'
        return res

    def generate_non_callable_docs(self, element_string, evaled):
        if element_string[0] != '_' and type(evaled) != types.ModuleType:
            t = str(type(evaled))
            t = t.split("'")
            res = '=== `{0}` ===\n'.format(element_string)
            res += '  * *Type*: {0}\n'.format(t[1])
            res += '  * *Value*: `{0}`\n\n'.format(repr(evaled))
            self.attributes.append(res)

    def generate_callable_wikidocs(self, element_string, evaled):
        if type(evaled) in [types.FunctionType, types.MethodType]:
            self.functions.append(self.generate_function_wikidocs(
                element_string, evaled))
        elif type(evaled) == types.ClassType:
            print 'CLASS'
        else:
            # print "Unknown callable object %s " % element_string
            pass

    def generate_function_wikidocs(self, func_string, func):
        res = '=== `{0}('.format(func_string)
        argspec = inspect.getargspec(func)
        args = argspec[0]
        defaults = argspec[3]
        def_values = []

        # Get the arguments
        for n in range(0, len(args)):
            try:
                if defaults != None and len(defaults) >= len(args) - n:
                    def_values.append((args[n], defaults[n - (len(args)
                                       - len(defaults))]))
                res += '{0}, '.format(args[n])
            except:
                res += '{0}, '.format(args[n])
        if res[-1] != '(':
            res = res[:-2]
        res += ')` ===\n'

        # Add default values (wiki doesn't allow '=' in headers)
        if len(def_values) != 0:
            res += '  * *Default values*: '
            for n in def_values:
                res += '{0} = {1}, '.format(n[0], repr(n[1]))
            res = res[:-2] + '\n'

        # Add docstring
        if func.__doc__ != None:
            # Remove indentation
            doc = inspect.cleandoc(func.__doc__)

            # Add wiki syntax for code
            l = []
            brackets = False
            for line in doc.splitlines():
                if line.startswith('>>>') and brackets == False:
                    l.append('{{{')
                    l.append(line)
                    brackets = True
                elif line == '' and brackets == True:
                    l.append('}}}')
                    l.append(line)
                    brackets = False
                else:
                    l.append(line)
            if brackets == True:
                l.append('}}}')
                brackets = False
            doc = '\n'.join(l)

            res += '{0}\n\n'.format(doc)
        return res

    def reset(self):
        self.functions = []
        self.classes = []
        self.attributes = []

    def set_module(self, module_string):
        if module_string != '':
            self.module_string = module_string
            self.module = eval(module_string)
            self.reset()

    def output_wiki(self):
        return self.generate_module_wikidocs()


def generate_package_wikidocs(package_string, file_prefix='ref',
        file_suffix='.wiki'):
    d = Documize()
    package = eval(package_string)
    print '\nGenerating documentation for package {0}'.format(package_string)
    for element in dir(package):
        if not callable(element):
            fullname = '{0}.{1}'.format(package_string, element)
            if (type(eval(fullname)) == types.ModuleType or
                    type(eval(fullname)) == types.ClassType):
                d.set_module(fullname)
                wikiname = file_prefix
                for parts in fullname.split('.'):
                    wikiname += parts.capitalize()
                wikiname += file_suffix
                print 'Writing {0}...'.format(wikiname),
                result = d.output_wiki()
                try:
                    f = open(os.path.join(sys.argv[1], wikiname), 'w')
                    try:
                        f.write(result)
                        print 'OK'
                    except:
                        print "ERROR. Couldn't write to file."
                    f.close()
                except:
                    print "ERROR. Couldn't open file for writing."

def main():
    print 'mingus version 0.5, Copyright (C) 2008-2011, Bart Spaans\n'
    print 'mingus comes with ABSOLUTELY NO WARRANTY. This is free'
    print 'software and you are welcome to redistribute it under'
    print 'certain conditions.'
    if len(sys.argv) == 1:
        print '\n\nUsage:', sys.argv[0], 'OUTPUT-DIRECTORY'
        sys.exit(1)
    elif not os.path.isdir(sys.argv[1]):
        print '\n\nError: not a valid directory:', sys.argv[1]
        sys.exit(1)
    generate_package_wikidocs('mingus.core', 'ref', '.wiki')
    generate_package_wikidocs('mingus.midi', 'ref', '.wiki')
    generate_package_wikidocs('mingus.containers', 'ref', '.wiki')
    generate_package_wikidocs('mingus.extra', 'ref', '.wiki')

if __name__ == '__main__':
    main()
