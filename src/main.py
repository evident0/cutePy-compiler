import sys

from new_parser import MyParser

def exec(infilename):
    inputFile = open(infilename)
    input = inputFile.read()
    parser = MyParser(input)
    quads = parser.syntax_analyzer()
    outfilename = infilename.split('.')[0]+".int"
    outputFile = open(outfilename, 'w')
    for quad in quads:
        outputFile.write(quad.__repr__()+'\n')
    inputFile.close()
    outputFile.close()

exec(sys.argv[1])
