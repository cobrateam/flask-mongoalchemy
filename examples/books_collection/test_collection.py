import unittest
import collection

class BooksCollectionTestCase(unittest.TestCase):

    def setUp(self):
        self.app = collection.app.test_client()

if __name__ == '__main__':
    unittest.main()
