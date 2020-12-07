#!/usr/bin/env python3

'''
(re)hydrator script for twarc
by Simon Lindgren

github.com/simonlindgren/smalt
'''

from twarc import Twarc
import glob
import json

# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

t = Twarc(consumer_key, consumer_secret, access_token, access_secret)


def main():
    print("Using all .txt files in this dir")
    files = glob.glob("*txt")

    for f in files:
        prefix = f.split(".")[0]
        print("Hydrating " + str(prefix))
        with open(prefix + ".jsonl", "w") as outfile:
            for tweet in t.hydrate(open(f)):
                json.dump(tweet,outfile)
                outfile.write("\n") # insert newline to get one json entry per line

if __name__ == '__main__':
    main()
