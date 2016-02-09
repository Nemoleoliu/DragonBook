
class Tag(object):
    NUM = 256
    ID = 257
    TRUE = 258
    FALSE = 259
    REL = 260

class Token(object):
    """docstring for Token"""
    def __init__(self, tag):
        self.tag = tag

class Word(Token):
    """docstring for Word"""
    def __init__(self, tag, lexeme):
        super(Word, self).__init__(tag)
        self.lexeme = lexeme
    def __str__(self):
        return "[Word][%s]" %self.lexeme

class Num(Token):
    """docstring for Num"""
    def __init__(self, value):
        super(Num, self).__init__(Tag.NUM)
        self.value = value
    def __str__(self):
        return "[Num][%f]" % self.value

class Rel(Token):
    """docstring for Rel"""
    def __init__(self, value):
        super(Rel, self).__init__(Tag.REL)
        self.value = value
    def __str__(self):
        return "[REL][%s]" % self.value


class LexAnalyzer(object):

    def __init__(self):
        self.words = dict()
        self.line = 0
        self.addReserveKeywords()

    def addReserveKeywords(self):
        self.addKeyword(Word(Tag.TRUE, 'true'))
        self.addKeyword(Word(Tag.FALSE, 'false'))

    def addKeyword(self, word):
        self.words[word.lexeme] = word

    def scan(self):
        f = open("test")
        while 1:
            peek = f.read(1)
            if not peek:
                break
            if peek == ' ' or peek == '\t':
                continue
            if peek == '\n':
                self.line += 1
            break
        if peek == '/':
            buf = peek
            peek = f.read(1)
            if buf=='/' and peek=='/':
                peek = f.read(1)
                while peek!='\n':
                    peek = f.read(1)
                self.line += 1
                peek = f.read(1)
            elif buf=='/' and peek=='*':
                buf = f.read(1)
                peek = f.read(1)
                while buf!='*' or peek!='/':
                    if peek == '\n':
                        self.line += 1
                    buf = peek
                    peek = f.read(1)
                peek = f.read(1)
        if peek in "<!=>":
            buf = peek
            peek = f.read(1)
            if peek == '=':
                return Rel(buf+peek)
            if buf == '>' or buf == '<':
                return Rel(buf)
        if peek.isdigit() or peek == '.':
            buf = []
            dot = peek=='.'
            while peek.isdigit() or ((not dot) and peek=='.'):
                buf.append(peek)
                peek = f.read(1)
            return Num(float("".join(buf)))
        if peek.isalpha():
            buf = []
            while peek.isalpha() or peek.isdigit():
                buf.append(peek)
                peek = f.read(1)
            lexeme = "".join(buf)
            if self.words.has_key(lexeme):
                return self.words[lexeme]
            return Word(Tag.ID, lexeme)
        t = Token(peek)
        return t

if __name__ == "__main__":
    la = LexAnalyzer()
    t = la.scan()
    print la.line
    print t

