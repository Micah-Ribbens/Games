from minigames.card_games.all_words import all_english_words


class Node:
    def __init__(self, value=None):
        self.children = {}
        self.is_end_of_word = False
        self.value = value


class WordFinder:
    finalLetters = ""
    letters = ""
    startingLetter = 0
    allWords = []
    usedLetters = ""
    letterList = []
    letterDictionary = {}
    alreadyReturned = False

    def __init__(self):
        self.root = Node(" ")

        for word in all_english_words:
            self.add_word(word)

    def get_children(self, current):
        children_list = []
        alphabet_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                         "t", "u", "v", "w", "x", "y", "z"]
        for x in range(len(alphabet_list)):
            if self.has_child(alphabet_list[x], current):
                children_list.append(alphabet_list[x])
        return children_list

    def has_child(self, ch, current):
        """
        give current and character
        """
        if current is None:
            return False
        if current.children.get(ch) is None:
            return False
        else:
            return True

    def add_child(self, ch, current):
        """
        give character and current
        """
        current.children[ch] = Node(ch)

    def get_child(self, ch, current):
        """
        give character and current
        """
        try:
            if current.children.get(ch) is not None:
                return current.children.get(ch)
        except AttributeError:
            pass

    def add_word(self, word):
        current = self.root
        for ch in word:
            if not self.has_child(ch, current):
                self.add_child(ch, current)
            current = self.get_child(ch, current)
        current.is_end_of_word = True

    def is_word(self, word):
        current = self.root
        for ch in word:
            if not self.has_child(ch.lower(), current):
                return False

            current = self.get_child(ch.lower(), current)

        return current.is_end_of_word

    def find_child(self, letters):
        current = self.root
        for ch in letters:
            current = self.get_child(ch, current)
        return current

    def get_lowercase(self, letters):
        """returns: String; the lowercase form of all the letters"""

        return_value = ""

        for letter in letters:
            return_value += letter.lower()

        return return_value

    def get_all_words(self, letters):
        current = self.root
        # I used two lists that the indexes correlate;
        # I could've used a list of dictionaries, but it was too complex
        combinations = []
        all_words = []
        current_combination = ""
        index = 0
        letters_available = self.get_lowercase(letters)
        letters_left = []
        while True:
            current = self.find_child(current_combination)
            possible_letters = self.get_children(current)
            for letter in possible_letters:
                if letters_available.__contains__(letter):
                    letters_left.append(self.remove_letter(letters_available, letter))
                    combinations.append(current_combination + letter)

            if index >= len(combinations):
                break

            current_combination = combinations[index]
            letters_available = letters_left[index]
            if self.is_word(current_combination) and len(current_combination) >= 2:
                all_words.append(current_combination)
            index += 1

        return all_words

    def remove_indexes(self, letters, remove_index):
        return letters[:remove_index] + letters[remove_index + 1:]

    def remove_letter(self, letters, letter):
        for x in range(len(letters)):
            if letters[x] == letter:
                return self.remove_indexes(letters, x)

    def get_longest_word(self, letters):
        """returns: String; the longest word possible with those letters; the lowercase form"""
        longest_word = ""

        for word in self.get_all_words(letters):
            if len(word) > len(longest_word):
                longest_word = word

        return longest_word



