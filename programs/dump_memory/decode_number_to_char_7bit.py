map = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "§", "$", "%", "&", "/", "(", ")", "=", "?", "ß", "`", "´", "*", "+", "'", "#", "_", "-", ":", ".", ";", ",", ">", "<", "|", "^", "°", "~", "@", "{", "[", "]", "}", "ä", "ö", "ü", "Ä", "Ö", "Ü", "€", "»", "«", "·", "…", "ø", "¹", "²", "³", "¼", "½", "¬", "¢", "µ", "æ", "ð", "đ", "ŋ", "ħ", "ł", "¶", "ŧ", "þ", "ы", "т"]


def decode_char(char: str):
    return map.index(char)



if __name__ == '__main__':
    print(decode_char("a"))
    print(decode_char("т"))
