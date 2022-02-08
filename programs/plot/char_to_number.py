characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789!§$%&/()=?ß`´*+'#_-:.;,><|^°~@{[]}äöüÄÖÜ€»«·…ø¹²³¼½¬¢µæðđŋħł¶ŧþыт"


def char_to_number(char):
    return characters.index(char)


def test():
    testing = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789!§$%&/()=?ß`´*+'#_-:.;,><|^°~@{[]}äöüÄÖÜ€»«·…ø¹²³¼½¬¢µæðđŋħł¶ŧþыт"
    x = 0
    for char in testing:
        y = char_to_number(char)
        assert x == y
        x += 1


if __name__ == '__main__':
    test()
