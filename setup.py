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
      data_files=[  ("share/urtdsc/noscreenshot.png", ["src/noscreenshot.png"]),
                    ("share/urtdsc/urtdsc-ru_RU.qm", ["src/translations/urtdsc-ru_RU.qm"]),
                    ("bin", ["src/urtdsc"]),
      ],
)
