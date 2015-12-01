import unittest
import vcheck


class CheckMod_test(unittest.TestCase):
    def mod_test(self):
        import os as _os
        cmod = vcheck.CheckMod(_os)

        self.assertEqual(cmod.mod, _os)
