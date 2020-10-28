#!/usr/bin/env python3

'''
instadigger.py

This script is for getting hashtag posts from Instagram
using Instaloader (https://github.com/instaloader/instaloader),
and to then only get posts from a certain period of time.

Based on https://instaloader.github.io/codesnippets.html

This script from https://github.com/simonlindgren/smalt
'''

import instaloader
import datetime as datetime
import time

def main():
    print("instadigger.py")
    print("---------------------------")
    HASHTAG = "metoo"

    L = instaloader.Instaloader()

    posts = instaloader.Hashtag.from_name(L.context, HASHTAG).get_posts()

    SINCE = datetime.datetime(2016, 12, 31)  # further from today, inclusive
    UNTIL = datetime.datetime(2017, 8, 1)  # closer to today, not inclusive

    k = 0  # initiate k
    #k_list = []  # uncomment this to tune k

    print("Paging through posts and skipping until reaching the set period ...")
    print("(Instagram hashtag search history will not be entirely chronological, but sometimes makes back-and-forth skips)")
    for post in posts:
        postdate = post.date

        if postdate > UNTIL:
            # we don't want this post
            postmonth = str(postdate)[:7]
            print("\rNow at " + postmonth, end="")
            print("\n")
            continue
        elif postdate <= SINCE:
            # we don't want this post either
            postmonth = str(postdate)[:7]
            print("\rNow at " + postmonth, end="")
            print("\n")
            k += 1
            if k == 500:
                break
            else:
                continue
        else:
            # we want this post
            print(postdate)
            L.download_post(post, HASHTAG)
            # if you want to tune k, uncomment below to get your k max
            #k_list.append(k)
            k = 0  # set k to 0

        time.sleep(2)

    #max(k_list)

if __name__ == '__main__':
    main()
