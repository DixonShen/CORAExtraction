#coding=utf-8

from xml.sax import handler, make_parser

paperTag = ('article', 'inproceedings', 'proceedings', 'book', 'incollection', 'pdhthesis', 'masterthesis', 'www')
DBLP_XML_PATH = 'E:\\DataSets\\dblp.xml'


class mHandler(handler.ContentHandler):
    
    def __init__(self):
        self.element_count = 0
    
    def startDocument(self):
        print 'Document Start'

    def endDocument(self):
        print 'Document End'

    def startElement(self, name, attrs):
        print 'Element Start'
        self.element_count += 1

    def endElement(self, name):
        print 'Element End'
        print "Count of elements: " + str(self.element_count)

    def characters(self, content):
        print content


def parserDblpXml():
    handler = mHandler()
    parser = make_parser()
    parser.setContentHandler(handler)
    f = open(DBLP_XML_PATH, 'r')
    parser.parse(f)
    f.close()

if __name__ == '__main__':
    print 'START'
    parserDblpXml()