import unittest

class Tests(unittest.TestCase):

    def setUp(self):
        from app import create_app
        self.app = create_app("development")
        self.client = self.app.test_client()

    #needs to be private
    def test_chats(self):
        self.client.post("/chats/test1", json={
                            "receiver" : "name",
                            "course_space" : "ohj1",
                            "topic" : "afdsas",
                            "message" : "JEE"
                            })
        
        a = self.client.get("/chats/test1")

        print(a.get_json())
        assert a.status_code == 200

    #needs to be group
    def test_groupchats(self):
        self.client.post("/chats/test2", json={
                            "receiver" : ["test1", "test2"],
                            "course_space" : "ohj1",
                            "topic" : "afdsas",
                            "message" : "jee"
                            })
        
        b = self.client.get("/chats/test2")

        print(b.get_json())
        assert b.status_code == 200


        


if __name__ == '__main__':
    unittest.main()