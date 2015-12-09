.. _vcheck.functions:

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

   >>> if vcheck.vcheck(vcheck, version=0): print('Not version 0')
   Not version 0
   >>> vcheck.check_warn(vcheck, version=0)
   >>> vcheck.check_raise(vcheck, version=0)
