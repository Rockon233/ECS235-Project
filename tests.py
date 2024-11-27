import requests
from itertools import permutations
from datetime import datetime
import random 
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
                if (requests.post("http://localhost:8000/insert", json={"word": word}).status_code != 200):
                    print("Insert failed")
        print("Finished")
        
    def testWithNumbers(self):
        print("Entering test with numbers")
        word = None
        for perm in permutations(self.numbers):
            for y in range(self.attempts):
                if (requests.post("http://localhost:8000/insert", json={"perm" : perm}).status_code != 200):
                    print("Insert failed")
        print("Finished")

    def test(self):
        print('Testing test route')
        
        print(requests.post("http://localhost:8000/test", json={"text" : f" Hello World! {datetime.now()}" }).status_code )
        print("Got here")
        print("-----")


if __name__ == '__main__':
    random_num = random
    test_class = Test()
    test_class.test()
    # test_class.testWithWords()
    test_class.testWithNumbers()