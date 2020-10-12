#!/usr/bin/env python3

'''
Convert a json file (all entries on one line)
to a jsonl file (one entry per line)

github.com/simonlindgren/smalt
'''

def main():
    # Read a file with all json on one line and split to a list
    file = open("fat.json","r")
    filestring = file.read()
    splitter = "}{"
    filelist = filestring.split(splitter)

    # Write the list to a file with each json entry on one line each
    with open("lined.jsonl", "w") as outfile:

        # Deal with first line
        outfile.write(filelist[0] + "}")
        outfile.write("\n")

        # Deal with all lines in between
        for dataline in filelist[1:10]:
            dataunit = "{" + dataline + '}'
            outfile.write(str(dataunit))
            outfile.write("\n")

        # Deal with last line
        outfile.write(filelist[-0] + "}")
        outfile.write("\n")

if __name__ == '__main__':
    main()
