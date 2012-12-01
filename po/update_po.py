#! /usr/bin/env python
#
# update_po - a gramps tool to update translations
#
# Copyright (C) 2006-2006  Kees Bakker
# Copyright (C) 2006       Brian Matherly
# Copyright (C) 2008       Stephen George
# Copyright (C) 2012
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""
update_po.py for Gramps translations.

Examples: 
   python update_po.py -t

      Tests if 'gettext' and 'python' are well configured.

   python update_po.py -h

      Calls help and command line interface.

   python update_po.py -p

      Generates a new template/catalog (gramps.pot).
      
   python update_po.py -m de.po

      Merges 'de.po' file with 'gramps.pot'.
      
   python update_po.py -k de.po

      Checks 'de.po' file, tests to compile and generates a textual resume.
"""

from __future__ import print_function

import os
import sys
from argparse import ArgumentParser


if sys.platform == 'win32':          
    # GetText Win 32 obtained from http://gnuwin32.sourceforge.net/packages/gettext.htm
    # ....\gettext\bin\msgmerge.exe needs to be on the path
    msgmergeCmd = os.path.join('C:', 'Program Files(x86)', 'gettext', 'bin', 'msgmerge.exe')
    msgfmtCmd = os.path.join('C:', 'Program Files(x86)', 'gettext', 'bin', 'msgfmt.exe')
    msgattribCmd = os.path.join('C:', 'Program Files(x86)', 'gettext', 'bin', 'msgattrib.exe')
    xgettextCmd = os.path.join('C:', 'Program Files(x86)', 'gettext', 'bin', 'xgettext.exe')
    pythonCmd = os.path.join(sys.prefix, 'bin', 'python.exe')
elif sys.platform == 'linux2' or os.name == 'darwin':
    msgmergeCmd = 'msgmerge'
    msgfmtCmd = 'msgfmt'
    msgattribCmd = 'msgattrib'
    xgettextCmd = 'xgettext'
    pythonCmd = os.path.join(sys.prefix, 'bin', 'python')
else:
    print ("ERROR: unknown system, don't know msgmerge, ... commands")
    sys.exit(0)

def tests():
    """
    Testing installed programs.
    We made tests (-t flag) by displaying versions of tools if properly
    installed. Cannot run all commands without 'gettext' and 'python'.
    """
    try:
        print ("\n====='msgmerge'=(merge our translation)================\n")
        os.system('''%(program)s -V''' % {'program': msgmergeCmd})
    except:
        print ('Please, install %(program)s for updating your translation' 
                    % {'program': msgmergeCmd})
        
    try:
        print ("\n==='msgfmt'=(format our translation for installation)==\n")
        os.system('''%(program)s -V''' % {'program': msgfmtCmd})
    except:
        print ('Please, install %(program)s for checking your translation' 
                    % {'program': msgfmtCmd})
        
    try:
        print ("\n===='msgattrib'==(list groups of messages)=============\n")
        os.system('''%(program)s -V''' % {'program': msgattribCmd})
    except:
        print ('Please, install %(program)s for listing groups of messages' 
                    % {'program': msgattribCmd})
        
    
    try:
        print("\n===='xgettext' =(generate a new template)==============\n")
        os.system('''%(program)s -V''' % {'program': xgettextCmd})
    except:
        print ('Please, install %(program)s for generating a new template' 
                    % {'program': xgettextCmd})
    
    try:
        print("\n=================='python'=============================\n")
        os.system('''%(program)s -V''' % {'program': pythonCmd})
    except:
        print ('Please, install python')
        
# See also 'get_string' from Gramps 2.0 (sample with SAX)
def TipsParse(filename, mark):
    """
    Experimental alternative to 'intltool-extract' for 'tips.xml'.
    """

    from xml.etree import ElementTree
    
    tree = ElementTree.parse(filename)
    root = tree.getroot()
        
    '''
    <?xml version="1.0" encoding="UTF-8"?>
      <tips>
        <_tip number="1">
          <b>Working with Dates</b>
            <br/>
        A range of dates can be given by using the format &quot;between 
        January 4, 2000 and March 20, 2003&quot;. You can also indicate 
        the level of confidence in a date and even choose between seven 
        different calendars. Try the button next to the date field in the
        Events Editor.
        </_tip>
        
    char *s = N_("<b>Working with Dates</b><br/>A range of dates can be 
    given by using the format &quot;between January 4, 2000 and March 20,
    2003&quot;. You can also indicate the level of confidence in a date 
    and even choose between seven different calendars. Try the button 
    next to the date field in the Events Editor.");
    
    gramps.pot:
    msgid ""
    "<b>Working with Dates</b><br/>A range of dates can be given by using the "
    "format &quot;between January 4, 2000 and March 20, 2003&quot;. You can also "
    "indicate the level of confidence in a date and even choose between seven "
    "different calendars. Try the button next to the date field in the Events "
    "Editor."
    '''
    
    tips = open('../gramps/data/tips.xml.in.h', 'w')
    marklist = root.iter(mark)
    for key in marklist:
        tip = ElementTree.tostring(key, encoding="UTF-8")
        tip = tip.replace("<?xml version='1.0' encoding='UTF-8'?>", "")
        tip = tip.replace('\n<_tip number="%(number)s">' % key.attrib, "")
        tip = tip.replace("<br />", "<br/>")
        #tip = tip.replace("\n</_tip>\n", "</_tip>\n") # special case tip 7
        #tip = tip.replace("\n<b>", "<b>") # special case tip 18
        tip = tip.replace("</_tip>\n\n", "")
        tip = tip.replace('"', '&quot;')
        tips.write('char *s = N_("%s");\n' % tip)
    tips.close()
    print ('Wrote ../gramps/data/tips.xml.in.h')
    root.clear()
    
def HolidaysParse(filename, mark):
    """
    Experimental alternative to 'intltool-extract' for 'holidays.xml'.
    """

    from xml.etree import ElementTree
    
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    ellist = root.iter()

    '''
    <?xml version="1.0" encoding="utf-8"?>
      calendar>
        <country _name="Bulgaria">
          ..
        <country _name="Jewish Holidays">
          <date _name="Yom Kippur" value="> passover(y)" offset="172"/>
          
    char *s = N_("Bulgaria");
    char *s = N_("Jewish Holidays");
    char *s = N_("Yom Kippur");
    
    gramps.pot:
    msgid "Bulgaria"
    msgid "Jewish Holidays"
    msgid "Yom Kippur"
    '''
    
    holidays = open('../gramps/plugins/lib/holidays.xml.in.h', 'w')
    for key in ellist:
        if key.attrib.get(mark):
            line = key.attrib
            string = line.items
            name = 'char *s = N_("%(_name)s");\n' % line
            holidays.write(name)
    holidays.close()
    print ('Wrote ../gramps/plugins/lib/holidays.xml.in.h')
    root.clear()


def XmlParse(filename, mark):
    """
    Experimental alternative to 'intltool-extract' for 'gramps.xml'.
    """
    
    from xml.etree import ElementTree
    
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    
    '''
    <?xml version="1.0" encoding="UTF-8"?>

    <mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
      <mime-type type="application/x-gramps">
        <_comment>Gramps database</_comment>
          <glob pattern="*.grdb"/>
      </mime-type>
      <mime-type type="application/x-gedcom">
        <_comment>GEDCOM</_comment>
          <glob pattern="*.ged"/>
          <glob pattern="*.gedcom"/>
          <glob pattern="*.GED"/>
          <glob pattern="*.GEDCOM"/>
    
    msgid "Gramps database"
    msgid "GEDCOM"
    '''
    
    mime = open('../data/gramps.xml.in.h', 'w')
    
    for key in root.iter():
        if key.tag == '{http://www.freedesktop.org/standards/shared-mime-info}%s' % mark:
            comment = 'char *s = N_("%s");\n' % key.text
            mime.write(comment)
    
    mime.close()
    print ('Wrote ../data/gramps.xml.in.h')
    root.clear()

        
def DesktopParse(filename):
    """
    Experimental alternative to 'intltool-extract' for 'gramps.desktop'.
    """
    
    '''
    [Desktop Entry]
    _Name=Gramps
    _GenericName=Genealogy System
    _X-GNOME-FullName=Gramps Genealogy System
    _Comment=Manage genealogical information, 
             perform genealogical research and analysis
             
    msgid "Gramps"
    msgid "Genealogy System"
    msgid "Gramps Genealogy System"
    msgid ""
          "Manage genealogical information, 
           perform genealogical research and analysis"
    '''
    
    desktop = open('../data/gramps.desktop.in.h', 'w')
    
    f = open(filename)
    lines = [file.strip() for file in f]
    f.close()
    
    for line in lines:
        if line[0] == '_':
            for i in range(len(line)):
                if line[i] == '=':
                    val = 'char *s = N_("%s");\n' % line[i+1:len(line)]
                    desktop.write(val)
                    
    desktop.close()
    print ('Wrote ../data/gramps.desktop.in.h')
                    

def KeyParse(filename, mark):
    """
    Experimental alternative to 'intltool-extract' for 'gramps.keys'.
    """
    
    '''
    application/x-gramps-xml:
		_description=Gramps XML database
		default_action_type=application
		short_list_application_ids=gramps
		short_list_application_ids_for_novice_user_level=gramps
		short_list_application_ids_for_intermediate_user_level=gramps
		short_list_application_ids_for_advanced_user_level=gramps
		category=Documents/Genealogy
		icon-filename=/usr/share/gramps/gramps.png
		open=gramps %f

    application/x-gedcom:
		_description=GEDCOM
		default_action_type=application
    
    msgid "Gramps XML database"
    msgid "GEDCOM"
    '''
    
    key = open('../data/gramps.keys.in.h', 'w')
    
    f = open(filename)
    lines = [file for file in f]
    f.close()
    
    temp = []
       
    for line in lines:
        for i in range(len(line)):
            if line[i:i+12] == mark:
                temp.append(line.strip())
                
    for t in temp:
        for i in range(len(t)):
            if t[i] == '=':
                val = 'char *s = N_("%s");\n' % t[i+1:len(t)]
                key.write(val)
    
    key.close()
    print ('Wrote ../data/gramps.keys.in.h')
    

def main():
    """
    The utility for handling translation stuff.
    What is need by Gramps, nothing more.
    """
       
    parser = ArgumentParser( 
                         description='This program generates a new template and '
                                      'also provides some common features.', 
                         )
    parser.add_argument("-t", "--test",
            action="store_true", dest="test",  default=True,
            help="test if 'python' and 'gettext' are properly installed")
                        
    parser.add_argument("-x", "--xml",
            action="store_true", dest="xml",  default=False,
            help="extract messages from xml based file formats")
    parser.add_argument("-g", "--glade",
            action="store_true", dest="glade",  default=False,
            help="extract messages from glade file format only")
    parser.add_argument("-c", "--clean",
            action="store_true", dest="clean",  default=False,
            help="remove created files")
    parser.add_argument("-p", "--pot", 
            action="store_true", dest="catalog",  default=False,
            help="create a new catalog")
                    
    update = parser.add_argument_group('Update', 'Maintenance around translations')
    
    # need at least one argument (sv.po, de.po, etc ...)

    # lang.po files maintenance                          
    update.add_argument("-m", "--merge", dest="merge",
            choices=[file for file in os.listdir('.') if file.endswith('.po')],
            help="merge lang.po files with last catalog")
              
    update.add_argument("-k", "--check", dest="check",
            choices=[file for file in os.listdir('.') if file.endswith('.po')],
            help="check lang.po files")
        
     # testing stage
    trans = parser.add_argument_group('Translation', 'Display content of  translations file')
       
    # need one argument (eg, de.po)
              
    trans.add_argument("-u", "--untranslated", dest="untranslated", 
            choices=[file for file in os.listdir('.') if file.endswith('.po')],
            help="list untranslated messages")
    trans.add_argument("-f", "--fuzzy", dest="fuzzy",
            choices=[file for file in os.listdir('.') if file.endswith('.po')],
            help="list fuzzy messages")
    
    
    args = parser.parse_args()
    namespace, extra = parser.parse_known_args()
    #print(args, '\n\t\t###\n', vars(args), '\n\t\t###\n', sys.argv[2:])

    if args.test:
        tests()
       
    if args.xml:
        extract_xml()
        
    if args.glade:
        create_filesfile()
        extract_glade()
        if os.path.isfile('tmpfiles'):
            os.unlink('tmpfiles')
        
    if args.catalog:
        retrieve()
        
    if args.clean:
        clean()
        
    if args.merge:
        merge(sys.argv[2:])
        
    if args.check:
        check(sys.argv[2:])
        
    if args.untranslated:
        untranslated(sys.argv[2:])
        
    if args.fuzzy:
        fuzzy(sys.argv[2:])

def create_filesfile():
    """
    Create a file with all files that we should translate.
    These are all python files not in POTFILES.skip added with those in 
    POTFILES.in
    """
    dir = os.getcwd()
    topdir = os.path.normpath(os.path.join(dir, '..', 'gramps'))
    lentopdir = len(topdir)
    f = open('POTFILES.in')
    infiles = dict(['../' + file.strip(), None] for file in f if file.strip() 
                                                        and not file[0]=='#')
    f.close()
    f = open('POTFILES.skip')
    notinfiles = dict(['../' + file.strip(), None] for file in f if file 
                                                        and not file[0]=='#')
    f.close()
    
    for (dirpath, dirnames, filenames) in os.walk(topdir):
            root, subdir = os.path.split(dirpath)
            if subdir.startswith("."):
                #don't continue in this dir
                dirnames[:] = []
                continue
            for dirname in dirnames:
                # Skip hidden and system directories:
                if dirname.startswith(".") or dirname in ["po", "locale"]:
                    dirnames.remove(dirname)
            #add the files which are python or glade files
            # if the directory does not exist or is a link, do nothing
            if not os.path.isdir(dirpath) or os.path.islink(dirpath):
                continue
            
            for filename in os.listdir(dirpath):
                name = os.path.split(filename)[1]
                if name.endswith('.py') or name.endswith('.glade'):
                    full_filename = os.path.join(dirpath, filename)
                    #Skip the file if in POTFILES.skip
                    if full_filename[lentopdir:] in notinfiles:
                        infiles['../gramps' + full_filename[lentopdir:]] = None
    #now we write out all the files in form ../gramps/filename
    f = open('tmpfiles', 'w')
    for file in sorted(infiles.keys()):
        f.write(file)
        f.write('\n')
    f.close()

def listing(name, extensionlist):
    """
    List files according to extensions.
    Parsing from a textual file (gramps) is faster and easy for maintenance.
    Like POTFILES.in and POTFILES.skip
    """
    
    f = open('tmpfiles')
    files = [file.strip() for file in f if file and not file[0]=='#']
    f.close()
    
    temp = open(name, 'w')
    
    for entry in files:
        for ext in extensionlist:
            if entry.endswith(ext):
                temp.write(entry)
                temp.write('\n')
                break
    
    temp.close()
    
def headers():
    """
    Look at existing C file format headers.
    Generated by 'intltool-extract' but want to get rid of this 
    dependency (perl, just a set of tools).
    """
    headers = []

    # in.h; extract_xml
    if os.path.isfile('''../gramps/data/tips.xml.in.h'''):
        headers.append('''../gramps/data/tips.xml.in.h''')
    if os.path.isfile('''../gramps/plugins/lib/holidays.xml.in.h'''):
        headers.append('''../gramps/plugins/lib/holidays.xml.in.h''')
    if os.path.isfile('''../data/gramps.xml.in.h'''):
        headers.append('''../data/gramps.xml.in.h''')
    if os.path.isfile('''../data/gramps.desktop.in.h'''):
        headers.append('''../data/gramps.desktop.in.h''')
    if os.path.isfile('''../data/gramps.keys.in.h'''):
        headers.append('''../data/gramps.keys.in.h''')
    
    return headers

def extract_xml():
    """
    Extract translation strings from XML based, keys, mime and desktop
    files. Own XML files parsing and custom translation marks.
    """
  
    TipsParse('../gramps/data/tips.xml.in', '_tip')
    HolidaysParse('../gramps/plugins/lib/holidays.xml.in', '_name')
    XmlParse('../data/gramps.xml.in', '_comment')
    DesktopParse('../data/gramps.desktop.in')
    KeyParse('../data/gramps.keys.in', '_description')
    
def create_template():
    """
    Create a new file for template, if it does not exist.
    """
    template = open('gramps.pot', 'w')
    template.close()
    
def extract_glade():
    """
    Extract messages from a temp file with all .glade
    """
    if not os.path.isfile('gramps.pot'):
        create_template()

    listing('glade.txt', ['.glade'])
    os.system('''%(xgettext)s --add-comments -j -L Glade '''
              '''--from-code=UTF-8 -o gramps.pot --files-from=glade.txt'''
             % {'xgettext': xgettextCmd}
             )

def retrieve():
    """
    Extract messages from all files used by Gramps (python, glade, xml)
    """
    extract_xml()
    
    if not os.path.isfile('gramps.pot'):
        create_template()
        
    create_filesfile()
    listing('python.txt', ['.py', '.py.in'])
    
    os.system('''%(xgettext)s -j --directory=./ -d gramps '''
              '''-L Python -o gramps.pot --files-from=python.txt '''
              '''--keyword=_ --keyword=ngettext '''
              '''--keyword=sgettext --from-code=UTF-8''' % {'xgettext': xgettextCmd}
             )
    
    extract_glade()
    
    # C format header (.h extension)
    for h in headers():
        print ('xgettext for %s' % h)
        os.system('''%(xgettext)s --add-comments -j -o gramps.pot '''
                  '''--keyword=N_ --from-code=UTF-8 %(head)s''' 
                  % {'xgettext': xgettextCmd, 'head': h}
                  )
    clean()

def clean():
    """
    Remove created files (C format headers, temp listings)
    """
    for h in headers():
        if os.path.isfile(h):
            os.unlink(h)
            print ('Remove %(head)s' % {'head': h})

    if os.path.isfile('python.txt'):
        os.unlink('python.txt')
        print ("Remove 'python.txt'")

    if os.path.isfile('glade.txt'):
        os.unlink('glade.txt')
        print ("Remove 'glade.txt'")

    if os.path.isfile('tmpfiles'):
        os.unlink('tmpfiles')
        print ("Remove 'tmpfiles'")

def merge(arg):
    """
    Merge messages with 'gramps.pot'
    """
    
    arg = arg[0]
    
    print ('Merge %(lang)s with current template' % {'lang': arg})
    os.system('''%(msgmerge)s --no-wrap %(lang)s gramps.pot -o updated_%(lang)s''' \
                % {'msgmerge': msgmergeCmd, 'lang': arg})
    print ("Updated file: 'updated_%(lang)s'." % {'lang': arg})

def check(arg):
    """
    Check the translation file
    """
    
    arg = arg[0]
    
    print ("Checked file: '%(lang.po)s'. See '%(txt)s.txt'." \
                % {'lang.po': arg, 'txt': arg[:-3]})
    os.system('''%(python)s ./check_po --skip-fuzzy ./%(lang.po)s > %(lang)s.txt''' \
                % {'python': pythonCmd, 'lang.po': arg, 'lang': arg[:-3]})
    os.system('''%(msgfmt)s -c -v %(lang.po)s''' 
                        % {'msgfmt': msgfmtCmd, 'lang.po': arg})

def untranslated(arg):
    """
    List untranslated messages
    """
    
    arg = arg[0]
    
    os.system('''%(msgattrib)s --untranslated %(lang.po)s''' % {'msgattrib': msgattribCmd, 'lang.po': arg})

def fuzzy(arg):
    """
    List fuzzy messages
    """

    arg = arg[0]
    
    os.system('''%(msgattrib)s --only-fuzzy --no-obsolete %(lang.po)s''' % {'msgattrib': msgattribCmd, 'lang.po': arg})

if __name__ == "__main__":
	main()