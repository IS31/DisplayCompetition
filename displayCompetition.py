import os
import webbrowser
from HTMLParser import HTMLParser

class RoundDisplayHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag
    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag
    def handle_data(self, data):
        print "Encountered some data  :", data

class DisplayCompetition(object):
    submissionsDir = 'submissions/'
    tournamentResultsDir = 'tournamentResults/'
    leaguesDir = tournamentResultsDir + '0/'
    quarterFinalsRound = 1
    semiFinalsRound = 2
    finalRound = 4
    numberOfLeagues = 4

    groups2Bots = {}
    leaguesMaps = []
    
    def __init__(self):
        self.initGroups2Bots()
        self.doLeagues()
        self.displayLeagues()

    def initGroups2Bots(self):
        for d in os.listdir(self.submissionsDir):
            f = open(self.submissionsDir + d + '/bot.txt', 'r')
            self.groups2Bots[d] = f.readline()

    def doLeagues(self):
        for league in range(1, self.numberOfLeagues + 1):
            for match in os.listdir(self.leaguesDir + str(league)):
                print "Entering match {}".format(match)
                playerA = match.split('-')[0]
                playerAWins = 0
                playerB = match.split('-')[1]
                playerBWins = 0
                matchDir = self.leaguesDir + str(league) + '/' + match
                for rnd in os.listdir(matchDir):
                    if rnd.split('.')[-1] != "txt":
                        continue
                    winner = rnd.split('_')[0][1:]
                    if winner == playerA:
                        playerAWins += 1
                    elif winner == playerB:
                        playerBWins += 1
                    else:
                        playerAWins += 1
                        playerBWins += 1
                matchWinner = ''
                matchLooser = ''
                if playerAWins > playerBWins:
                    matchWinner = playerA
                    matchLooser = playerB
                elif playerBWins > playerAWins:
                    matchWinner = playerB
                    matchLooser = playerA
                else:
                    print "Draw game!"
                    matchWinner = playerA
                    matchLooser = playerB
                print "Group {} wins against group {}".format(matchWinner, matchLooser)
                wonRoundFiles = [rnd for rnd in os.listdir(matchDir) if rnd.split('_')[0] == 'w' + matchWinner and rnd.split('.')[-1] != 'txt']
                maxSizeRoundFiles = [f for f in wonRoundFiles if f.endswith('map5')]
                if len(maxSizeRoundFiles) == 0:
                    maxSizeRoundFiles = [f for f in wonRoundFiles if f.endswith('map4')]
                if len(maxSizeRoundFiles) == 0:
                    maxSizeRoundFiles = [f for f in wonRoundFiles if f.endswith('map3')]
                if len(maxSizeRoundFiles) == 0:
                    maxSizeRoundFiles = [f for f in wonRoundFiles if f.endswith('map2')]
                #print maxSizeRoundFiles
                maxSizeRoundFile = sorted(maxSizeRoundFiles)[-1]
                self.leaguesMaps.append(matchDir + '/' + maxSizeRoundFile +  '/generated.htm')
            print self.leaguesMaps
        print len(self.leaguesMaps)

    def displayLeagues(self):
        #roundDisplayParser = RoundDisplayHTMLParser()
        #roundDisplayParser.feed()

        for x in range(6):
            htmlLeagueDisplayFile = open('leagueDisplay' + str(x) + '.html', 'w')
            fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <iframe src='""" + self.leaguesMaps[x + 0] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + self.leaguesMaps[x + 10] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + self.leaguesMaps[x + 20] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + self.leaguesMaps[x + 30] + """' height=1000 width=900 frameborder=0></iframe>
  </body>
</html>
"""
            htmlLeagueDisplayFile.write(fileContents)
            htmlLeagueDisplayFile.close()

        for x in range(6,9):
            htmlLeagueDisplayFile = open('leagueDisplay' + str(x) + '.html', 'w')
            fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <iframe src='""" + self.leaguesMaps[x + 0] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + self.leaguesMaps[x + 10] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + self.leaguesMaps[x + 20] + """' height=1000 width=900 frameborder=0></iframe>
  </body>
</html>
"""
            htmlLeagueDisplayFile.write(fileContents)
            htmlLeagueDisplayFile.close()



                #maxSizeRoundPath = os.path.dirname(os.path.realpath(__file__)) + '/' + matchDir + '/' + maxSizeRoundFile +  '/generated.htm'
                #webbrowser.open("file://" + maxSizeRoundPath)
                                
                    
        
dc = DisplayCompetition()
