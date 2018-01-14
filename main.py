#!/usr/bin/env python; # -*- coding: utf-8 -*-
import os
import csv
import instaloader
import operator
import xlsxwriter
import requests
import time
from apius import *


# main(x) --- > given username to scrape its profile
def main(user):
    start_time = time.time()
    # instance of InstaLoader
    br = instaloader.Instaloader()
    # prof1 is the username given when you called the func
    prof1 = user #str(input("Profile to scrape: "))
    f = br.get_profile_metadata(prof1)
    # first list of Post objects
    psts= list()
    for i in br.get_profile_posts(f):
        psts.append(i)
    link1 = "https://www.instagram.com/"+prof1
    #posts quantity
    posts_qty = len(psts)

    # Scraping manually to get this values, had some troubles with Bfsoup PD: Still the scraping is quite fast (0.9s)
    page = requests.get(link1).text
    m=page.find('biography": "')
    k= len('biography": "')
    n= page.find('"blo')
    #print(page)
    description = page[m+k:n-len('"blo')]

    fws= page.find('"followed_by": {"count": ')
    fws_p1 = len('"followed_by": {"count": ')
    fws2 = page.find('}, "followed_by_viewer":')
    fws2_p2 = len('}, "followed_by_viewer":')
    followers = page[fws+fws_p1:fws2]

    fwng = page.find('"follows": {"count": ')
    fwng_p1 = len('"follows": {"count": ')
    fwng2 = page.find('}, "follows_viewer":')
    fwng2_p2 = len('}, "follows_viewer":')
    following = page[fwng+fwng_p1:fwng2]
    l= str()
    for i in description:
        l+=i
    l= l.replace('\\n', '')
    description = l
    # Manual scrape finished
    # FF is a dict, where I saved the post objects as keys and values is a tuple of the content
    ff=dict()
    for i in psts:
        ff[i] = i.likes+i.comments,'=IMAGE("'+str(i.url)+'",4,100,100)',i.url,i.caption,'', '',i.caption_hashtags,len(i.caption_hashtags),i.likes,i.comments
    sorted_x = sorted(ff.items(), key=operator.itemgetter(1), reverse=True)
    print("--- %s seconds is what take to scrape data to a list of objects ---" % (time.time() - start_time))
    # sorted_x is a list of the post objects and props. With this func the dict gets ordered by likes+comments.

    # ----- IMPORTANT ---------
    # workbook, creating sheet. Name can be whatever, but be sure to change it in the apius.py as well.
    # PD: something obvious but you could make apius main() func take the name of the file as argument
    namef = prof1+".xlsx"
    workbook = xlsxwriter.Workbook(namef)
    worksheet = workbook.add_worksheet()

    # formatting big header (Account - Total posts)
    format = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': 'black', 'font_size': '28'})
    # Widen columns
    worksheet.set_column('A:D', 14)
    worksheet.set_column('J:J', 16)
    worksheet.set_row(0, 40, format)
    # Add a bold format
    bold = workbook.add_format({'bold': True})
    # BIG HEADERS WITH FORMAT BACKGROUND & COLOR
    worksheet.write('A1', 'Account', format)
    # big headers. formatting rest of cells
    M = ['B1','C1', 'D1', 'E1', 'F1', 'G1']
    for i in M:
        worksheet.write(i, '',format)
    worksheet.write('A2', 'Instagram')
    worksheet.write('B2', 'Handle URL')
    worksheet.write('C2', 'Blurb')
    worksheet.write('D2', 'Total Posts')
    worksheet.write('E2', 'Followers')
    worksheet.write('F2', 'Following')
    worksheet.write('G2', 'Posts')
    # HEADERS. TOP CONTENT'S A BIG HEADER W/ FORMAT BACKGROUND & COLOR
    worksheet.write('I1', 'Top Content', format)
    # Total posts secondary headers
    worksheet.write('I2', 'Likes and comments')
    worksheet.write('J2', 'Post')
    worksheet.write('K2', 'URL')
    worksheet.write('L2', 'Caption')
    worksheet.write('M2', '')
    worksheet.write('N2', '')
    worksheet.write('O2', 'Hashtags')
    worksheet.write('P2', '# of hashtags')
    worksheet.write('Q2', 'Likes')
    worksheet.write('R2', 'Comments')

    # writing Account data in cells
    worksheet.write('A3', prof1)
    worksheet.write("B3", link1)
    worksheet.write("C3", description)
    worksheet.write("D3", posts_qty)
    worksheet.write("E3", followers)
    worksheet.write("F3", following)
    worksheet.write("G3", posts_qty)
    # Insert an image.
    format2= workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'silver'})
    counter_H = 2
    for i in range(1,101):
        counter_H+=1
        worksheet.write(str('H'+str(counter_H)),i, format2)

    # list of characters, with this I generate the position for the further data
    pos_sh = list(map(chr, range(73, 83)))
    # since we start writing the Total post data in the third row, we start a for loop at 2 and adds 1, that finishes
    # at the 100 requested posts, so there will be 2+1, 3+1, till 102. This will be the position, w/ the char list
    # A3, B3, C3.... A102, B102, C102
    pos = 2
    #m = [('comment+likes', pst', 'link2p', 'pst_cap', '', '', 'hashtags', 'num_hash', 'likes', 'comments')]
    for i in range(100):
        pos+=1
        # for loop, to get the char. lj will be now the position eg. A54 in a loop instance. Or B52 in another instance
        # PD Not OOP instance, I mean like physical (time) instance
        for j in range(0, len(pos_sh)):
            lj = pos_sh[j] + str(pos)
            # writing in the position or cell address (An, Bn, Cn... * 100) the value sorted_[i][1][j]
            # that stands for [i], loop til 100 posts, [1], because is saved in tuple, so [0], and [j] because of the
            # str index in the tuple, since the char list and the data has to be the same len, in 1, the data would be
            # the image in Jn cell, in 2 would be captions in Kn cell
            worksheet.write(lj, str(sorted_x[i][1][j]))
    workbook.close()
    upload_sheet(namef, prof1)
    # this could be replaced for a better way to call the main function of the google drive api
    print("--- %s seconds is what takes to fully run the script ---" % (time.time() - start_time))
main(USERNAME_STRING) # pass string username example 'type.gang'
# By David Ramos Penott
