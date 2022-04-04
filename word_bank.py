import random
NORMAL = 4
class Wordbank():
    def __init__(self):
        # make a compilation of english words
        with open('most_common_words_1000.txt', mode='r') as file:
            self.all_english_words = [word.strip() for word in file.readlines() if len(word) > NORMAL]
            random.shuffle(self.all_english_words)

        # self.all_words = self.english_words
        # self.first_20_words = self.english_words[:20]
        self.submitted_words = []
        self.attempted = []
        self.correct_counter = 0
        self.mistake_counter = 0
        self.total_submission = 0
        self.backspace_counter = 0


