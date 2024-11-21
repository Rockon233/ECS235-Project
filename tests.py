import requests
from itertools import permutations

class Test:

    def __init__(self):
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.numbers = [0,1,2]
        self.attempts = 1
        

    def testWithWords(self):
        print("Entering test with words")
        word = None
        for letter in self.alphabet:
            word += letter
            for y in range(self.attempts):
                if (requests.post("http://localhost:5000/insert", json={"word": word}).status_code != 200):
                    print("Insert failed")
        print("Finished")
        
    def testWithNumbers(self):
        print("Entering test with numbers")
        word = None
        for perm in permutations(self.numbers):
            for y in range(self.attempts):
                if (requests.post("http://localhost:5000/insert", json={"perm" : perm}).status_code != 200):
                    print("Insert failed")
        print("Finished")

    def test(self):
        print('Testing test route')
        print(requests.post("http://localhost:5000/test", json={"text" : " Hello World! " }).status_code )
        print("Got here")


if __name__ == '__main__':
    test_class = Test()
    test_class.test()