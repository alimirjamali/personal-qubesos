# vim: fileencoding=utf-8

import os
import setuptools
import setuptools.command.install
import sys

exclude=[]

# don't import: import * is unreliable and there is no need, since this is
# compile time and we have source files
def get_console_scripts():
    if sys.version_info[0:2] >= (3, 4):
        for filename in os.listdir('./qubesadmintt/tools'):
            basename, ext = os.path.splitext(os.path.basename(filename))
            if basename in ['__init__', 'dochelpers', 'xcffibhelpers']\
                    or ext != '.py':
                continue
            yield basename.replace('_', '-'), 'qubesadmintt.tools.{}'.format(
                basename)

# create simple scripts that run much faster than "console entry points"
class CustomInstall(setuptools.command.install.install):
    def run(self):
        bin = os.path.join(os.path.expanduser('~'), "bin")
        try:
            os.makedirs(bin)
        except:
            pass
        for file, pkg in get_console_scripts():
           path = os.path.join(bin, file)
           with open(path, "w") as f:
               f.write(
"""#!/usr/bin/python3
from {} import main
import sys
if __name__ == '__main__':
	sys.exit(main())
""".format(pkg))

           os.chmod(path, 0o755)
        setuptools.command.install.install.run(self)

if __name__ == '__main__':
    setuptools.setup(
        name='qubesadmintt',
        version=open('version').read().strip(),
        author='Ali Mirjamali',
        author_email='ali@mirjamali.com',
        description='Qubes Admin API Tweak Tools',
        license='LGPL2.1+',
        url='https://www.github.com/alimirjamali/personal-qubesos/',
        packages=['qubesadmintt', 'qubesadmintt.tools'],
        cmdclass={
           'install': CustomInstall
        },

        )

