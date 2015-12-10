.. _vcheck.exceptions:

**********
Exceptions
**********

.. currentmodule:: vcheck

VCheck use the custom :class:`VersionError` exceptions, which are used to raise exceptions particular to the VCheck process:

.. autosummary::
   :toctree: generated/

   VersionError

They have two parts, :attr:`VersionError.msg`

.. admonition:: Example

   Version-checking VCheck itself:

   >>> mod = vcheck.CheckMod(vcheck)
