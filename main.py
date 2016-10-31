import requests
from bs4 import BeautifulSoup

limitPages = 30
filepath = 'out/users.txt'
threadLinks = list()

for i in range (1, limitPages):
    print ('Getting threads list from page #' + str(i))
    r = requests.get('https://forum.openstreetmap.org/viewforum.php?id=21&p=' + str(i))
    pageContent = r.text
    soup = BeautifulSoup(pageContent, 'html.parser')

    for threadDiv in soup.find_all("div", "tclcon"):
        for threadLink in threadDiv.find_all('a', limit=1):
            threadLinks.append(threadLink.get('href'))

threadsLen = len(threadLinks)
print ('Now we have ' + str(threadsLen) + ' threads to process')

for i in range (0, threadsLen):
    j = 1
    userNames = set()
    linesSet = set()
    print ('Processing thread #' + str(i))
    while True:
        r = requests.get('https://forum.openstreetmap.org/' + threadLinks[i] + '&p=' + str(j))
        pageContent = r.text
        soup = BeautifulSoup(pageContent, 'html.parser')

        if soup.find(rel="prev") == None and j > 1:
            i = i + 1
            break

        print ('Processing page #' + str(j) + ' from thread #' + str(i + 1))

        for postDiv in soup.find_all("div", "postleft"):
            for userName in postDiv.find('strong'):
                userNames.add(userName)

        j = j + 1

    print ('Saving thread users to file...')

    with open(filepath) as f:
        lines = f.read().splitlines()
        linesSet = set(lines)
        for user in userNames:
            linesSet.add(user)

    with open(filepath, 'w') as file_handler:
        for line in linesSet:
            file_handler.write("{}\n".format(line))
