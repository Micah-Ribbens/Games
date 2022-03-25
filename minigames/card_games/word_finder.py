from base.utility_functions import get_lowercase, remove_letter
from minigames.card_games.all_words import all_english_words


class Node:
    def __init__(self, value=None):
        self.children = {}
        self.is_end_of_word = False
        self.value = value


class WordFinder:
    """Uses a trie to find all words and see if something is a word"""

    letters = ""

    def __init__(self):
        self.root = Node(" ")

        for word in all_english_words:
            self.add_word(word)

    def get_children(self, node):
        """returns: List of String; the letters (children) that the node has"""
        children_list = []
        alphabet_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                         "t", "u", "v", "w", "x", "y", "z"]
        for x in range(len(alphabet_list)):
            if self.has_child(alphabet_list[x], node):
                children_list.append(alphabet_list[x])
        return children_list

    def has_child(self, ch, node):
        """returns: boolean; if the node has that child"""

        return node is not None and node.children.get(ch) is not None

    def add_child(self, ch, node):
        """Adds the ch (child) to the node"""
        node.children[ch] = Node(ch)

    def get_child(self, ch, node):
        """returns: Node; the child of that node"""
        return node.children.get(ch)

    def add_word(self, word):
        """Adds the word to the word finder, so it knows it is a word"""

        current = self.root
        for ch in word:
            if not self.has_child(ch, current):
                self.add_child(ch, current)
            current = self.get_child(ch, current)
        current.is_end_of_word = True

    def is_word(self, word):
        """returns: boolean; if the parameter 'word' is a word (more specifically in the trie)"""

        current = self.root
        for ch in word:
            if not self.has_child(ch.lower(), current):
                return False

            current = self.get_child(ch.lower(), current)

        return current.is_end_of_word

    def get_node(self, letters):
        """returns: Node; the node that the letters lead to"""

        current = self.root
        for ch in letters:
            current = self.get_child(ch, current)
        return current

    def get_all_words(self, letters):
        """returns: List of String; all the words possible with those letters"""

        # I used two lists that the indexes correlate;
        # I could've used a list of dictionaries, but it was too complex
        combinations = []
        all_words = []
        current_combination = ""
        index = 0
        letters_available = get_lowercase(letters)
        letters_left = []
        while True:
            current = self.get_node(current_combination)
            possible_letters = self.get_children(current)
            for letter in possible_letters:
                if letters_available.__contains__(letter):
                    letters_left.append(remove_letter(letters_available, letter))
                    combinations.append(current_combination + letter)

            if index >= len(combinations):
                break

            current_combination = combinations[index]
            letters_available = letters_left[index]
            if self.is_word(current_combination) and len(current_combination) >= 2:
                all_words.append(current_combination)
            index += 1

        return all_words

    def get_longest_word(self, letters):
        """returns: String; the longest word possible with those letters; the lowercase form"""
        longest_word = ""

        for word in self.get_all_words(letters):
            if len(word) > len(longest_word):
                longest_word = word

        return longest_word

    def get_all_words_of_length(self, letters, length):
        """returns: String; all the words that those letters can yield which length matches the parameter 'length'"""

        return_value = []

        for word in self.get_all_words(letters):
            if len(word) == length:
                return_value.append(word)

        return return_value



