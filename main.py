#!/usr/bin/env python; # -*- coding: utf-8 -*-
import os
import csv
from instaloader import *
import operator
import xlsxwriter
import time
from apius import *

def main(user):
    start_time = time.time()
    instagramUsername = user #str(input("Profile to scrape: "))
    profileUrl = "https://www.instagram.com/" + instagramUsername
    # instance of InstaLoader
    instagramLoader = instaloader.Instaloader()
    # instagramUsername is the username given when you call the func
    instagramProfile = Profile.from_username(instagramLoader.context, instagramUsername)
    description = instagramProfile.biography
    following = instagramProfile.followees
    followers = instagramProfile.followers
    # first list of Post objects
    postsList= list()
    for posts in instagramProfile.get_posts():
        postsList.append(posts)
    #posts quantity
    numberOfPosts = len(postsList)
    dict_posts=dict()
    for post in postsList:
        dict_posts[post] = post.likes, '=IMAGE("' + str(post.url) + '",4,100,100)', post.url, post.caption, '', '', post.caption_hashtags, len(post.caption_hashtags), post.likes, post.comments
    posts_list = sorted(dict_posts.items(), key = operator.itemgetter(1), reverse = True)
    # dict_posts is a dictionary, where I saved the post objects as keys and values is a tuple of the content
    print("--- %s seconds is what take to scrape data to a list of objects ---" % (time.time() - start_time))
    # posts_list is a list of the post objects and props. With this func the dict gets ordered by likes+comments.
    # ----- IMPORTANT ---------
    # workbook, creating sheet. Name can be whatever, but be sure to change it in the apius.py as well.
    # PD: something obvious but you could make apius main() func take the name of the file as argument
    sheetName = instagramUsername + ".xlsx"
    workbook = xlsxwriter.Workbook(sheetName)
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
        worksheet.write(i, '', format)
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
    worksheet.write('A3', instagramUsername)
    worksheet.write("B3", profileUrl)
    worksheet.write("C3", description)
    worksheet.write("D3", numberOfPosts)
    worksheet.write("E3", followers)
    worksheet.write("F3", following)
    worksheet.write("G3", numberOfPosts)
    # Insert an image.
    format2= workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': 'silver'})
    startPosition = 2
    # This loop controls the quantity of posts
    for i in range(1,101):
        if(i > numberOfPosts):
            break
        startPosition+=1
        worksheet.write(str('H'+str(startPosition)),i, format2)
    # list of characters, with this I generate the position for the further data
    list_abecedary = list(map(chr, range(73, 83)))
    # since we start writing the Total post data in the third row, we start a for loop at 2 and adds 1, that finishes
    # at the 100 requested posts, so there will be 2+1, 3+1, till 102. This will be the position, w/ the char list
    # A3, B3, C3.... A102, B102, C102
    startPosition = 2
    if(numberOfPosts > 100):
        numberOfPosts = 100
    for i in range(numberOfPosts):
        startPosition+=1
        # for loop, to get the char. cell will be now the cell startPositionition eg. A54 in a loop. Or B52 in another loop
        for j in range(0, len(list_abecedary)):
            cell = list_abecedary[j] + str(startPosition)
            # writing in the position or cell address (An, Bn, Cn... * 100) the value sorted_[i][1][j]
            # that stands for [i], loop til 100 posts, [1], because is saved in tuple, so [0], and [j] because of the
            # str index in the tuple, since the char list and the data has to be the same len, in 1, the data would be
            # the image in Jn cell, in 2 would be captions in Kn cell
            worksheet.write(cell, str(posts_list[i][1][j]))
    workbook.close()
    upload_sheet(sheetName, instagramUsername)
    # this could be replaced for a better way to call the main function of the google drive api
    print("--- %s seconds is what takes to fully run the script ---" % (time.time() - start_time))
main('daveit0') # pass string username e.g:'Google'
# By David Ramos Penott
