.. _vcheck.classes:

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

   >>> mod = vcheck.CheckMod(vcheck)
