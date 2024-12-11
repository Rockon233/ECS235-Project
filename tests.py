import requests
from itertools import permutations
from datetime import datetime
import random 
class Test:
    
    def __init__(self):
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        # self.alphabet = 'Until recently, the prevailing view assumed lorem ipsum was born as a nonsense text. “It’s not Latin, though it looks like it, and it actually says nothing,” Before & After magazine answered a curious reader, “Its ‘words’ loosely approximate the frequency with which letters occur in English, which is why at a glance it looks pretty real.” As Cicero would put it, “Um, not so fast.” The placeholder text, beginning with the line “Lorem ipsum dolor sit amet, consectetur adipiscing elit”, looks like Latin because in its youth, centuries ago, it was Latin. Richard McClintock, a Latin scholar from Hampden-Sydney College, is credited with discovering the source behind the ubiquitous filler text. In seeing a sample of lorem ipsum, his interest was piqued by consectetur—a genuine, albeit rare, Latin word. Consulting a Latin dictionary led McClintock to a passage from De Finibus Bonorum et Malorum (“On the Extremes of Good and Evil”), a first-century B.C. text from the Roman philosopher Cicero. In particular, the garbled words of lorem ipsum bear an unmistakable resemblance to sections 1.10.32–33 of Cicero’s work, with the most notable passage excerpted below: “Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.” A 1914 English translation by Harris Rackham reads: “Nor is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but occasionally circumstances occur in which toil and pain can procure him some great pleasure.” McClintock’s eye for detail certainly helped narrow the whereabouts of lorem ipsum’s origin, however, the “how and when” still remain something of a mystery, with competing theories and timelines.'
        self.numbers = [0,1,2]
        self.attempts = 1
        

    def testWithWords(self):
        print("Entering test with words")
        word = ''
        for letter in self.alphabet:
            word += letter
            for y in range(self.attempts):
                response = requests.post("http://localhost:8000/testrsa", json={"word": word})
                if (response.status_code != 201):
                    print("test failed")
                    print(response.json)
                    
        print("Finished")
        
    def testWithNumbers(self):
        print("Entering test with numbers")
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
    # test_class.testWithWords()
    test_class.testWithWords()