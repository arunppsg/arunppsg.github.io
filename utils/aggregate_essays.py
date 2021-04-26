#!/usr/bin/python3

"""
This program searches the directories of blogs and add the entry to index.html file.
It gets title from the blog name, date from os.getmtime utility
"""

import os
import datetime
with open("../index.html", "r") as f:
    lines = f.readlines()

def get_starting_lines():
    start_lines = []
    start_lines.append("                <li>\n")
    start_lines.append('                   <div class="post-meta">\n')
    return start_lines

def get_date_line(file_path):
    time = os.path.getmtime(file_path)
    day, month, year = datetime.datetime.fromtimestamp(time).strftime('%d %m %Y').split(' ')
    month_dict = {1:'Jan', 2:'Feb', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July',
                    8:'Aug', 9:'Sept', 10:'Oct', 11:'Nov', 12:'Dec'}
    month = month_dict[int(month)]
    line = '<span class="post-date">'+month+' '+day+', '+year+'</span>\n'
    return line

def get_essay_link_line(file_path):
    line = '<a class="essay-link" href='
    file_name = file_path.split('/')[2]
    dir_name = file_path.split('/')[1]
    line += dir_name + '/' + file_name
    line += '">'
    heading = file_name.replace('-', ' ').replace('.html', '')
    heading = heading.split(' ')
    for i, word in enumerate(heading):
        if len(word) > 3:
            word = word[0].upper()+word[1:]
            heading[i] = word
    heading = ' '.join(heading)
    line += heading
    line += '</a>\n'

    return line
                
dirs = ['2020', '2021']
new_lines = []
for line in lines:
    new_lines.append(line)
    if '<ul class="essay-list">' in line:
        for dir in dirs:
            for file in os.listdir(os.path.join('..', dir)):
                file_path = os.path.join(os.path.join('..', dir), file)
                new_lines.extend(get_starting_lines())
                new_lines.extend(get_date_line(file_path))
                new_lines.extend(get_essay_link_line(file_path))
                new_lines.extend('<span class="tags"> </span>\n')
                new_lines.extend('</div>\n</li>\n')

with open('../index.html', 'w') as f:
    f.writelines(new_lines)



