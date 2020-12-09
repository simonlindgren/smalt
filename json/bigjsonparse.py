#!/usr/bin/python

'''
bigjsonparse.py

A set of functions for parsing json(l) files. Initially created to
parse a large jsonl file of tweets collected using twarc.

Usage:
import bigjsonparse as bjp
bjp.get_keys("/path/to/file.jsonl")
wanted_keys = ['list', 'of', 'your', 'choosing']
bjp.filter_keys("/path/to/file.jsonl", wanted_keys)
bjp.to_csv()

This script from https://github.com/simonlindgren/smalt
'''

import json
import collections
import pandas as pd


def flatten(d, parent_key='', sep='_'):  # flattening nested dicts
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_keys(filepath):  # get first line of data and print keys
    with open(filepath, "rb") as data:
        dataline = json.loads(data.readline())
        dataline = flatten(dataline)
        for k, v in dataline.items():
            print(k)


def filter_keys(filepath, wanted_keys):  # process 1 line at a time and write to file
    with open(filepath, "rb") as infile:
        with open("filtered_data.jsonl", "w") as outfile:
            for c, line in enumerate(infile):
                line_dict = flatten(json.loads(line))
                new_dict = {k: line_dict[k] for k in wanted_keys if k in line_dict}
                outfile.write(str(new_dict) + "\n")
                print("\r"+str(c), end="")


def to_csv(): # read 'filtered_data.jsonl" line by line and write to csv
    with open("filtered_data.csv", "w") as outfile:
        with open("filtered_data.jsonl", "r") as infile:
            header = eval(infile.readline())
            header = ",".join([k for k,v in header.items()])
            outfile.write(header + "\n")

            for c,i in enumerate(infile):
                dataline = eval(i)

                # for csv parsing, replace in-text " with ' and
                # enclose all of full_text in " "
                raw = dataline['full_text']
                raw = raw.replace('"', "'").replace('”', "'").replace('“', "'")
                raw = '"' + raw + '"'
                dataline['full_text'] = raw

                dataline = ",".join([str(v) for k,v in dataline.items()])
                outfile.write(dataline + "\n")
                print("\r" + str(c+1), end="")
