import unittest
import vcheck
import git

# ================================
# Hexsha for repo head
# ================================
current_hexsha   = 'b39035318052f36e8347c54b2dba4195a03c7847'

# ================================
# Hexsha for repo tags
# ================================
current_hexshas  = [ 'b56a895c7a5996f13341023033ab324ada6ee2bc',
                     '093f93188ce93e2ab5e2453c1423bcf87542c08b',
                     '1109ccbc8ffa750db7f0a71523d18833d54904a5'
                     ]
# ================================
# Hexsha guaranteed not present
# ================================
unpresent_hexsha = '0ff92d0c2b192ffcc136108d6c339d742da3d5f0'

# ================================
# Versions for repo tags
# ================================
current_versions  = [ 'v0.0.0', 'v0.0.1', 'v1.0.0' ]

# ================================
# Version guaranteed not present
# ================================
unpresent_version = ['v2.0.0']

# ================================
# Module to check
# ================================
import vcheck.versionerror as mod2check


class checkmod_test(unittest.TestCase):
    def setUp(self):
        # ================================
        # Create patchers
        # ================================
        self.gitRepo_patcher   = mock.patch('git.Repo', autospec=True)
        self.gitTagRef_patcher = mock.patch('git.TagReference', autospec=True)

        # ================================
        # Start patchers
        # ================================
        self.gitRepo_patcher.start()
        self.gitTagRef_patcher.start()

        # ================================
        # Add cleanup
        # ================================
        self.addCleanup(self.gitRepo_patcher.stop)
        self.addCleanup(self.gitTagRef_patcher.stop)
        self.addCleanup(self._clearcmod)

        self.gitRepoInst = git.Repo()

        self.mockrepo_real()

    def tearDown(self):
        pass

    def mockrepo_real(self, is_dirty=False, on_version_ind=None, current_hexshas=current_hexshas, current_versions=current_versions):
        inst = self.gitRepoInst
        # ================================
        # Set whether dirty or real
        # ================================
        inst.is_dirty.return_value = is_dirty

        # ================================
        # Mock repo has versions/tags
        # ================================
        if on_version_ind is not None:
            inst.head.object.hexsha = current_hexshas[on_version_ind]
        else:
            inst.head.object.hexsha = current_hexsha

        inst.tags = []
        for i in current_versions:
            inst.tags.append(git.TagReference('a', 'b'))

        for i, tag in enumerate(inst.tags):
            tag.object.hexsha = current_hexshas[i]
            tag.name = current_versions[i]

        # ================================
        # Reset self.cmod instance
        # ================================
        self._cmod = None

    @property
    def cmod(self):
        if self._cmod is None:
            self._cmod = vcheck.CheckMod(mod2check)

        return self._cmod

    def _clearcmod(self):
        self._cmod = None

    # ================================
    # Test init
    # ================================
    def init_raisedirty_test(self):
        self.mockrepo_real(is_dirty=True)

        with self.assertRaises(vcheck.VersionError) as cm:
            cmod = vcheck.CheckMod(mod2check)  # noqa

        self.assertEqual(cm.exception.errno, vcheck.VersionError.DIRTY)

    def init_notgit_test(self):
        self.doCleanups()
        self.gitRepo_patcher = mock.patch('git.Repo', autospec=True, side_effect=git.InvalidGitRepositoryError('Mock Error'))
        self.gitRepo_patcher.start()
        self.addCleanup(self.gitRepo_patcher.stop)

        with self.assertRaises(vcheck.VersionError) as cm:
            self.cmod

        self.assertEqual(cm.exception.errno, vcheck.VersionError.NO_GIT)

    # ================================
    # Test vcheck()
    # ================================
    def vcheck_toomanyargs_test(self):
        on_version_ind = -1
        self.mockrepo_real(on_version_ind=on_version_ind)

        with self.assertRaisesRegex(ValueError, 'Only specify either hexsha (.*) or version(.*)'):
            self.cmod.vcheck(hexsha=current_hexshas[on_version_ind] , version=current_versions[on_version_ind])

    def vcheck_notenoughargs_test(self):
        on_version_ind = -1
        self.mockrepo_real(on_version_ind=on_version_ind)

        with self.assertRaisesRegex(ValueError, 'Neither hexsha nor version specified'):
            self.cmod.vcheck()

    def vcheck_hexshamatches_test(self):
        self.assertTrue(self.cmod.vcheck(hexsha=current_hexsha))

    def vcheck_hexshafails_test(self):
        self.assertFalse(self.cmod.vcheck(hexsha=unpresent_hexsha))

    def vcheck_versionmatches_test(self):
        on_version_ind = -1
        self.mockrepo_real(on_version_ind=on_version_ind)
        
        self.assertTrue(self.cmod.vcheck(version=current_versions[on_version_ind]))

    def vcheck_versionfails_test(self):
        on_version_ind = -1
        self.mockrepo_real(on_version_ind=on_version_ind)
        
        self.assertFalse(self.cmod.vcheck(version=unpresent_version))

    def vcheck_versionerrors_test(self):
        with self.assertRaisesRegex(vcheck.VersionError, 'Repo for module .* does not match a released version.'):
            self.cmod.vcheck(version=unpresent_version)

    # ================================
    # Test attributes
    # ================================
    def mod_test(self):
        self.assertIs(self.cmod.mod, mod2check)

    def mainmod_test(self):
        self.assertIs(self.cmod.mainmod, vcheck)

    def mainmod_path_test(self):
        self.assertEqual(self.cmod.mainmod_path, vcheck.__path__[0])

    def repo_test(self):
        self.assertIs(self.cmod.repo, self.gitRepoInst)

    def hexsha_test(self):
        self.assertEqual(self.cmod.hexsha, current_hexsha)

    def version_notags_test(self):
        self.mockrepo_real(current_hexshas=[], current_versions=[])

        with self.assertRaisesRegex(vcheck.VersionError, 'The module has no version as it is not tagged.'):
            self.cmod.version

    def version_notattag_test(self):
        with self.assertRaisesRegex(vcheck.VersionError, 'Unable to return version: not at a tag.'):
            self.cmod.version

    def version_test(self):
        on_version_ind = -1
        self.mockrepo_real(on_version_ind=on_version_ind)

        self.assertEqual(self.cmod.version, current_versions[on_version_ind])
