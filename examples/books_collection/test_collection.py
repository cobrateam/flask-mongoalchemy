# -*- coding: utf-8 -*-

# Copyright 2010 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest
import collection


class BooksCollectionTestCase(unittest.TestCase):

    def setUp(self):
        self.app = collection.app.test_client()

if __name__ == '__main__':
    unittest.main()
