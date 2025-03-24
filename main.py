import requests as re
from bs4 import BeautifulSoup
import csv
import json

sectors = {}
industries = {}

def keep_list(line):
    if line[4] not in sectors:
        sectors[line[4]] = 1
    else:
        sectors[line[4]] = sectors[line[4]] + 1
    if line[5] not in industries:
        industries[line[5]] = 1
    else:
        industries[line[5]] = industries[line[5]] + 1

def better_list(line):
    if line[4] not in sectors:
        sectors[line[4]] = {}
    # else:
    #     sectors[line[4]].append(line[5])
    if line[5] not in sectors[line[4]]:
        sectors[line[4]][line[5]] = 1
    else:
        sectors[line[4]][line[5]] = sectors[line[4]][line[5]] + 1



def parse(page_num):
    URL = "https://disfold.com/united-states/companies/?page=" + str(page_num)
    html = re.get(URL)
    soup = BeautifulSoup(html.content, 'html.parser')

    lines = []
    line = []
    i = 0
    finds = soup.find_all("td")
    file = open('companies.csv', 'a', newline='')
    writer = csv.writer(file)
    for find in finds:
        if i % 6 == 0 and len(line) >= 5:
            lines.append(line)
            writer.writerow(line)
            better_list(line)
            line = []
        entry = str(find.text).strip()
        if not entry == '':
            # print(entry)
            line.append(entry)
            i = i + 1
    file.close()

    # print("PRINT LINES")
    # for thing in lines:
    #     print(thing)



for i in range (1, 34):
    parse(i)
    print("Finished page " + str(i))
print(sectors)
print(industries)

json_file = open('sectors.json', 'w')
json.dump(sectors, json_file, indent=4, separators=(",", ": "))