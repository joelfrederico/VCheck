.. _vcheck.classes:

.. testsetup:: *

   import vcheck
   import unittest.mock as mock
   patcher = mock.patch('vcheck.vcheck')
   patcher.start()
   inst = vcheck.vcheck
   inst.return_value = True

*******
Classes
*******

.. currentmodule:: vcheck

VCheck provides a class :class:`CheckMod` which processes and organizes the version information of a module for quick access and processing:

.. autosummary::
   :toctree: generated/

   CheckMod

It is the backbone of VCheck, and is fairly simple to use.

.. admonition:: Example

   Version-checking VCheck itself:

   >>> vcheck.vcheck(vcheck, version='v1.0.0')
   True
