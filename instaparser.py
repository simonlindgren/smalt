#!/usr/bin/env python
# coding: utf-8

'''
instaparser.py

Parse a directory of files and data downloaded with Instaloader (https://github.com/instaloader/instaloader).

Run this script from within the same directory as where the data files have been saved.

This script from https://github.com/simonlindgren/smalt
'''

import glob
import re
import pandas as pd
import lzma
import json
from datetime import datetime

def main():
    print("instaparser.py")
    print("---------------------------")

    # First, use the media filenames to create a list of post ids
    print("Getting media ids")

    mediafile_ids = []
    jpegs = glob.glob('*.jpg')
    mp4s = glob.glob('*.mp4)')

    for jpeg in jpegs:
        mediafile_ids.append(jpeg)
    for mp4 in mp4s:
        mediafile_ids.append(mp4)

    post_ids = []

    for file in mediafile_ids:
        post_id = file.split('_UTC')[0]
        post_ids.append(post_id)

    post_ids = list(set(post_ids))

    posts_df = pd.DataFrame(post_ids, columns = ["id"])


    # Make datetime column
    print("Getting dates and times")

    datetime_col = []

    for i in posts_df.id:
        day = i.split("_")[0]
        hms_split = i.split("_")[1].split("-")
        hms = " " + str(hms_split[0]) + ":" + str(hms_split[1]) + ":" + str(hms_split[2])
        timestamp = day + hms
        datetime_col.append(timestamp)

    posts_df['datetime'] = datetime_col


    # Read the caption txts to add captions to the posts
    print("Parsing captions")

    capfiles = glob.glob('*UTC.txt')

    cap_ids = []
    captions = []


    for file in capfiles:
        cap_id = file.split('_UTC')[0]
        cap_ids.append(cap_id)
        caption = open(file, "r").read()
        caption = re.sub("\n", " ", caption)
        captions.append(caption)

    cap_df = pd.DataFrame(list(zip(cap_ids, captions)))
    cap_df.columns = ['id', 'caption']

    data_df = pd.merge(posts_df, cap_df, on="id")
    data_df['type'] = "caption"


    # Get usernames from the metadata file
    print("Parsing user ids")

    datafiles = glob.glob('*xz')
    file_ids = []
    usernames = []

    for file in datafiles:
        file_id = file.split('_UTC')[0]
        with lzma.open(file) as f:
            json_bytes = f.read()
            if len(json_bytes) > 0:
                data = json.loads(json_bytes)
                try:
                    username = data['node']['owner']['id']
                    usernames.append(username)
                except:
                    usernames.append("NaN")

                file_ids.append(file_id)


    users_df = pd.DataFrame(list(zip(file_ids, usernames)))
    users_df.columns = ['id', 'user']

    data_df = pd.merge(data_df, users_df, on="id")


    # Get the comments from the comments files
    print("Parsing comments")

    commfiles = glob.glob('*_comments.json')

    file_ids = []
    comments = []
    types = []
    users = []
    times = []

    for file in commfiles:
        file_id = file.split('_UTC')[0]

        with open(file) as f:
            json_bytes = f.read()
            data = json.loads(json_bytes)
            if len(data) > 0:
                for i in data:
                    file_ids.append(file_id)
                    comment = re.sub("\n", " ", i['text'])
                    comments.append(comment)
                    types.append("comment")
                    user = i['owner']['id']
                    timestamp = i['created_at']
                    converted_time = str(datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
                    times.append(converted_time)
                    users.append(user)

    comments_df = pd.DataFrame(list(zip(file_ids, times, comments, types, users)))
    comments_df.columns = ['id', 'datetime', 'caption', 'type', 'user']

    data_df = pd.concat([data_df, comments_df])


    data_df = data_df.sort_values(by=["id","type"])


    # Create a hashtags column
    print("Finding hashtags")

    hashtags = []

    for i in data_df.caption:
        post_hashtags = []
        i = re.sub("#", " #", str(i))
        i = re.sub("  ", " ", i).lower()
        i = (i.split(" "))
        for token in i:
            if token.startswith("#"):
                post_hashtags.append(token)
        hashtags.append(post_hashtags)

    data_df['hashtags'] = hashtags


    # Save csv
    print("Saving csv")

    data_df.to_csv("parsed_instaloader.csv", index=False)

    print("Done")

if __name__ == '__main__':
    main()
