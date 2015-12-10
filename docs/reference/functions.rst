.. _vcheck.functions:

.. testsetup:: *

   import vcheck
   import unittest.mock as mock
   patcher = mock.patch('vcheck.vcheck')
   patcher.start()
   inst = vcheck.vcheck
   inst.return_value = True

**************
Core Functions
**************

.. currentmodule:: vcheck

VCheck provides several functions for quickly checking the version of
a given module:

.. autosummary::
   :toctree: generated/

   check_raise
   check_warn
   vcheck

It is possible to raise an error with :func:`check_raise`, a warning
with :func:`check_warn`, or to obtain a boolean with :func:`vcheck`:

.. admonition:: Example

   Version-checking VCheck:

   >>> if vcheck.vcheck(vcheck, version='0'): print('Not version 0')
   Not version 0
   >>> vcheck.check_warn(vcheck, version='0')  # doctest: +SKIP
   __main__:1: UserWarning: VersionError: Repo for module vcheck is dirty (changes have been made); version not well-defined.
   >>> vcheck.check_raise(vcheck, version='0')
   Traceback (most recent call last):
        ...
   vcheck.versionerror.VersionError: Repo for module vcheck is dirty (changes have been made); version not well-defined.
