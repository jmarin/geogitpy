import unittest
import os
from geogitpy.repo import Repository
import time
import shutil
from geogitpy import geogit
from geogitpy.commitish import Commitish

class GeogitCommitishTest(unittest.TestCase):
        
    repo = Repository(os.path.join(os.path.dirname(__file__), 'data/testrepo'))

    def getTempPath(self):
        return os.path.join(os.path.dirname(__file__), "temp", str(time.time())).replace('\\', '/')

    def getClonedRepo(self):
        dst = self.getTempPath()
        return self.repo.clone(dst)  

    def testLog(self):
        commitish = Commitish(self.repo, geogit.HEAD)
        log = commitish.log()
        self.assertEquals(4, len(log))        
        self.assertEquals("message_4", log[0].message)                

    def testRootTreeListing(self):
        commitish = Commitish(self.repo, geogit.HEAD)
        trees = commitish.root().trees()        
        self.assertEquals(1, len(trees))
        self.assertEquals("parks", trees[0].path)
        entries = self.repo.log()      
        id = self.repo.revparse(trees[0].ref)  
        self.assertEquals(entries[0].commitid, id)  

    def testCheckout(self):
        repo = self.getClonedRepo()
        branch = Commitish(repo, "conflicted")
        branch.checkout()
        self.assertEquals(repo.head().ref, branch.ref)
        master = Commitish(repo, geogit.MASTER)
        master.checkout()
        self.assertEquals(repo.head().ref, master.ref)

    def testDiff(self):
        commitish = Commitish(self.repo, geogit.HEAD)
        diff = commitish.diff()
        self.assertEquals(1, len(diff))
        self.assertEquals("parks/5", diff[0].path)

    def testDiffCaching(self):
        commitish = Commitish(self.repo, geogit.HEAD)
        diff = commitish.diff()
        self.assertEquals(diff, commitish._diff)
