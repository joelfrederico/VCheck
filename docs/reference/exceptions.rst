.. _vcheck.exceptions:

**********
Exceptions
**********

.. currentmodule:: vcheck

VCheck use the custom :class:`VersionError` exceptions, which are used to raise exceptions particular to the VCheck process:

.. autosummary::
   :toctree: generated/

   VersionError

They have two useful, a `msg` and an `errno` that can be accessed:

.. admonition:: Example

   Version-checking VCheck itself:

   >>> ve = vcheck.VersionError('Repo for module is dirty '  \
                                '(changes have been made); ' \
                                'version not well-defined.', \
                                errno=vcheck.VersionError.DIRTY)
   >>> ve.msg
   >>> ve.errno
