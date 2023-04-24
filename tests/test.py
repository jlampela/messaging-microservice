import unittest

class Tests(unittest.TestCase):

    def setUp(self):
        from app import create_app
        self.app = create_app("development")
        self.client = self.app.test_client()


    def test(self):
        assert 1 == 1


if __name__ == '__main__':
    unittest.main()