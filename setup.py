#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from distutils.core import setup

setup(name='urtdsc',
      version='0.3',
      description='Urban Terror Demo-Screenshot C0nc4t3n4t0r',
      author='Stanislav N. aka pztrn',
      author_email='pztrn@pztrn.ru',
      url='http://dev.pztrn.ru/projects/urtdsc',
      packages=['urtdsc'],
      requires=["pyqt"],
      package_dir={'urtdsc': 'src'},
      py_modules=['config', 'lib', 'AboutWindow', 'AllScreensDialog', 'MainWindow'],
      data_files=[  ("share/urtdsc/", ["src/noscreenshot.png"]),
                    ("share/urtdsc/", ["src/translations/urtdsc-ru_RU.qm"]),
                    ("share/applications/", ["src/urtdsc.desktop"]),
                    ("bin", ["src/urtdsc"]),
      ],
)
