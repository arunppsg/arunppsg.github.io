#!/usr/bin/python3

"""
This program searches the directories of blogs and add the entry to index.html file.
It gets title from the blog name, date from os.getmtime utility
"""

import os
import datetime

header = """
<html>

<head>
    <!-- Tamil Quote -->

    <script>
    // https://stackoverflow.com/questions/49468425/js-pick-random-quotes-on-page-refresh
    function PickThirukkural()
    {
        var kurals[10];
        alert("Alert");
    }
    </script>

    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-M6KVQ3TNZY"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-M6KVQ3TNZY');
    </script>
    <title>Home</title>
    <link rel = "stylesheet" type = "text/css" href = "index.css" />
</head>
"""

active_work = """
<body>
    <div class="thirukkual">
    </div>

    <div class="container">
        <div class="content">
            <div class="active-works">
                <h2>Active Works</h2>
                <ul class="active-works-list">
                    <li>
                        <br><span class="active-works-link">Working on detecting malware from network traffic.</span>
                    </li>
                </ul>
            </div>
"""

papers = """
            <div class="papers">
                <h2>Unpublished Manuscripts</h2>
                <ul class="paper-list">
                <li>
                    <a class="paper-link" href="files/FCI.pdf">Data-Driven Analysis of Food Corporation of India’s Operations and Recommendations</a>(Submitted to DSE Winter School 2020)
                </li>
                </ul>
            </div>
"""

essay_list_start = """
            <div class="essays">
                <h2>Essays</h2>
                <ul class="essay-list">
"""

def get_starting_lines():
    start_lines = []
    start_lines.append("                <li>\n")
    start_lines.append('                   <div class="post-meta">\n')
    return start_lines

def get_date_line(file_path):
    time = os.path.getctime(file_path)
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
    line += '>'
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
file_list = []
for dir in dirs:
    for file in os.listdir(os.path.join('..', dir)):
        file_path = os.path.join(os.path.join('..', dir), file)
        file_list.append([file_path, os.path.getmtime(file_path)])
file_list.sort(key = lambda x: x[1], reverse=True)

new_lines = []
for file in file_list:
    new_lines.extend(get_starting_lines())
    new_lines.extend(get_date_line(file[0]))
    new_lines.extend(get_essay_link_line(file[0]))
    new_lines.extend('<span class="tags"> </span>\n')
    new_lines.extend('</div>\n</li>\n')

footer = """
       </ul>
       </div>
        </div>
       <div class="sidebar">
            <span class='about'>
                <a href="about.html">About me</a>
                <br><br>
                <a href="bookshelf.html">Bookshelf</a>
            </span>
        </div>
    </div>
    <a href="https://info.flagcounter.com/SG6L"><img src="https://s05.flagcounter.com/count2/SG6L/bg_FFFFFF/txt_000000/border_CCCCCC/columns_5/maxflags_25/viewers_0/labels_0/pageviews_0/flags_0/percent_0/" alt="Flag Counter" border="0"></a>
    <br>
    <div class="footer">
        Arun Palaniappan © 2021. Last update: 28 March 2021.
    </div>

</html>

</body>

</html>

"""

with open('../index.html', 'w') as f:
    f.write(header)
    f.write(active_work)
    f.write(papers)
    f.write(essay_list_start)
    f.writelines(new_lines)
    f.write(footer)



