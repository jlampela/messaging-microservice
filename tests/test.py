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
                            "message" : "JEE",
                            "language": "fi"
                            })
        
        
        a = self.client.get("/chats/test1")
        b = a.get_json()
        assert b[0]["type"] == "Private"


        #print(a.get_json())
        assert a.status_code == 200

    #needs to be group
    def test_groupchats(self):
        self.client.post("/chats/test2", json={
                            "receiver" : ["test1", "test2"],
                            "course_space" : "ohj1",
                            "topic" : "afdsas",
                            "message" : "jee",
                            "language": "fi"
                            })
        
        b = self.client.get("/chats/test2")
        c = b.get_json()
        assert c[0]["type"] == "Group"

        #print(b.get_json())
        assert b.status_code == 200

    def test_wrong_requirement(self):
        self.client.post("/chats/test3", json={
                            "vastaanottaja" : "name",
                            "course_space" : "ohj1",
                            "topic" : "afdsas",
                            "message" : "JEE",
                            "language": "fi"
                            })
        
        b = self.client.get("/chats/test3")
            
        test = b.get_json()
        print(test)

        #print(a.get_json())
        assert a.status_code == 400
        print("wrong receiver test successful")

    def test_posting_alot_msgs(self):
        try:
            #about 400 in 1min
            for x in range(1):
                self.client.post("/chats/test1", json={
                                    "receiver" : "test",
                                    "course_space" : "ohj1",
                                    "topic" : "afdsas",
                                    "message" : "JEE",
                                    "language": "fi"
                                })
        except:
            print("test posting alot msgs failed")

    #cover trying to get messages with length of 0
    def test_getting_empty_database(self):  
            a = self.client.get("/chats/test123")
            print(a)

            assert a.status_code == 403

   

    def test_linking_to_other(self):
        try:
            self.client.post("/chats/linktest", json={
                "userId" : "1",
                "message" : "link test",

            })

            testlink1 = self.client.get("/chats/linktest")
            testlink2 = testlink1.get_json() 

            self.client.post("/chats/linktest", json={
                "userId" : "2",
                "message:" : "link test",
                "linked_to" : testlink2
            })

        except:
            print("failed")

            



if __name__ == '__main__':
    unittest.main()