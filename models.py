import textract
import re

class Scene:
    characters = []
    location = ""
    number = 0
    time = ""
    length = 0


class Script:

    def document_reader(self, file):
        '''Uses textract to read and return the text of files, split them into different lines and return the whole thing
        as a list object'''
        t =textract.process(file).decode('utf-8')
        return t


    def __init__(self, source):
        self.source = source
        self.text = self.document_reader(self.source)
        self.raw_text = ''.join(self.text)

    def __repr__(self):
        print("<Script title: {}".format(self.text[0:10]))

    scenes = 0
    title = ""
    author = ''
    locus = ['INT', 'EXT', 'INT./EXT']
    times = ['DAY', 'NIGHT', 'EVENING', 'DAWN']


