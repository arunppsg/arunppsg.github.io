#!/usr/bin/python3
import datetime
import sys
post_title = input("Enter post title" )
post_tags = input('Enter post tags seperated by ,').split(',')
post_link = post_title.lower().replace(' ','-')+'.html'

with open("../index.html", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if "essay-list" in line:
        blank_space_len = 0
        for i in line:
            if i == ' ':
                blank_space_len += 1
            if i.isalnum():
                break
 
        new_lines.append(' '*blank_space_len+"<li>\n")
        new_lines.append(' '*blank_space_len+'<div class="post-meta">\n')
        span_line=' '*blank_space_len+'<span class="post-date">'+datetime.date.today().strftime("%B %d, %Y")+'</span>\n'
        new_lines.append(span_line)
        essay_link=' '*blank_space_len+'<a class="essay-link" href='+datetime.date.today().strftime("%Y")+'/'+post_link+'">'+post_title+"</a>\n"
        new_lines.append(essay_link)
        span_tags=' '*blank_space_len+'<span class="tags">'
        for tag in post_tags:
            span_tags = span_tags+tag+' '
        span_tags = span_tags + '</span>\n'
        new_lines.append(span_tags)
        new_lines.append(' '*blank_space_len+'</div>\n')
        new_lines.append(' '*blank_space_len+'</li>\n')


with open('../index.html', 'w') as f:
    f.writelines(new_lines)

