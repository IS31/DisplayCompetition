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
    quarterFinalsDir = tournamentResultsDir + '1/'
    semiFinalsDir = tournamentResultsDir + '2/'
    finalDir = tournamentResultsDir + '3/'
    quarterFinalsRound = 1
    semiFinalsRound = 2
    finalRound = 4
    numberOfLeagues = 4

    groups2Bots = {}
    leaguesMaps = []
    quarterFinalsMaps = []
    semiFinalsMaps = []
    finalMaps = []
    
    def __init__(self):
        self.initGroups2Bots()
        self.generateCover()
        self.doLeagues()
        self.generateLeaguesDisplay()
        self.generateQuarterFinalsCover()
        self.doQuarterFinals()
        self.generateQuarterFinalsDisplay()
        self.generateSemiFinalsCover()
        self.doSemiFinals()
        self.generateSemiFinalsDisplay()
        self.generateFinalCover()
        self.doFinal()
        self.generateFinalDisplay()
        self.generateChampionDisplay()

    def initGroups2Bots(self):
        for d in os.listdir(self.submissionsDir):
            f = open(self.submissionsDir + d + '/bot.txt', 'r')
            self.groups2Bots[d] = f.readline()

    def doLeagues(self):
        for league in range(1, self.numberOfLeagues + 1):
            for match in os.listdir(self.leaguesDir + str(league)):
                print "Entering match {}".format(match)
                matchDir = self.leaguesDir + str(league) + '/' + match
                matchWinner = self.getMatchWinner(matchDir)
                maxSizeRoundFile = self.getMapToDisplay(matchDir, matchWinner)
                self.leaguesMaps.append(matchDir + '/' + maxSizeRoundFile +  '/generated.htm')
            print self.leaguesMaps
        print len(self.leaguesMaps)

    def getMatchWinner(self, matchDir):
        match = matchDir.split('/')[-1]
        playerA = match.split('-')[0]
        playerAWins = 0
        playerB = match.split('-')[1]
        playerBWins = 0
        if 'draw' in os.listdir(matchDir):
            matchDir = matchDir + '/draw/'
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
                #print "Draw game!"
                matchWinner = playerA
                matchLooser = playerB
        print "Group {} wins against group {}".format(matchWinner, matchLooser)
        return matchWinner

    def getMapToDisplay(self, matchDir, matchWinner):
        wonRoundFiles = [rnd for rnd in os.listdir(matchDir) if rnd.split('_')[0] == 'w' + matchWinner and rnd.split('.')[-1] != 'txt']
        maxSizeRoundFiles = [f for f in wonRoundFiles if f.endswith('map5')]
        if len(maxSizeRoundFiles) == 0:
            maxSizeRoundFiles = [f for f in wonRoundFiles if f.endswith('map4')]
        if len(maxSizeRoundFiles) == 0:
            maxSizeRoundFiles = [f for f in wonRoundFiles if f.endswith('map3')]
        if len(maxSizeRoundFiles) == 0:
            maxSizeRoundFiles = [f for f in wonRoundFiles if f.endswith('map2')]
        return sorted(maxSizeRoundFiles)[-1]

    def generateLeaguesDisplay(self):
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
    <div align='left'><a href='resultsDisplay""" + str(x - 1) + """.html'>Previous</a></div><div align='right'><a href='resultsDisplay""" + str(x) + """.html'>Next</a></div><hr>
    <iframe src='""" + self.leaguesMaps[x + 0] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + self.leaguesMaps[x + 10] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + self.leaguesMaps[x + 20] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + self.leaguesMaps[x + 30] + """' height=1000 width=900 frameborder=0></iframe>
  </body>
</html>
"""
            htmlLeagueDisplayFile.write(fileContents)
            htmlLeagueDisplayFile.close()
            htmlResultsDisplayFile = open('resultsDisplay' + str(x) + '.html', 'w')
            fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='left'><a href='leagueDisplay""" + str(x) + """.html'>Previous</a></div><div align='right'><a href='leagueDisplay""" + str(x + 1) + """.html'>Next</a></div><hr>

  </body>
</html>
"""
            htmlResultsDisplayFile.write(fileContents)
            htmlResultsDisplayFile.close()



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
    <div align='left'><a href='resultsDisplay""" + str(x - 1) + """.html'>Previous</a></div><div align='right'><a href='resultsDisplay""" + str(x) + """.html'>Next</a></div><hr>
    <iframe src='""" + self.leaguesMaps[x + 0] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + self.leaguesMaps[x + 10] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + self.leaguesMaps[x + 20] + """' height=1000 width=900 frameborder=0></iframe>
  </body>
</html>
"""
            htmlLeagueDisplayFile.write(fileContents)
            htmlLeagueDisplayFile.close()
            htmlResultsDisplayFile = open('resultsDisplay' + str(x) + '.html', 'w')
            if x < 8:
                fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='left'><a href='leagueDisplay""" + str(x) + """.html'>Previous</a></div><div align='right'><a href='leagueDisplay""" + str(x + 1) + """.html'>Next</a></div><hr>

  </body>
</html>
"""
            else:
                fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='left'><a href='leagueDisplay""" + str(x) + """.html'>Previous</a></div><div align='right'><a href='quarterFinalsDisplayCover.html'>Next</a></div><hr>

  </body>
</html>
"""


            htmlResultsDisplayFile.write(fileContents)
            htmlResultsDisplayFile.close()

                #maxSizeRoundPath = os.path.dirname(os.path.realpath(__file__)) + '/' + matchDir + '/' + maxSizeRoundFile +  '/generated.htm'
                #webbrowser.open("file://" + maxSizeRoundPath)

    def generateCover(self):
        htmlCoverPage = open('leagueDisplayCover.html', 'w')
        fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='center'><a href='leagueDisplay0.html'>Next</a></div><hr>
  </body>
</html>
"""
        htmlCoverPage.write(fileContents)
        htmlCoverPage.close()

    def doQuarterFinals(self):
        print "Doing quarter finals"
        for match in os.listdir(self.quarterFinalsDir):
            matchDir = self.quarterFinalsDir + match
            matchWinner = self.getMatchWinner(matchDir)
            maxSizeRoundFile = self.getMapToDisplay(matchDir, matchWinner)
            self.quarterFinalsMaps.append(matchDir + '/' + maxSizeRoundFile +  '/generated.htm')
        print self.quarterFinalsMaps

    def generateQuarterFinalsDisplay(self):
        print "Generating quarter finals display"
        for x in range(4):
            htmlQuarterFinalsDisplay = open('quarterFinalsDisplay' + str(x) + '.html', 'w')
            fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='left'><a href='resultsQuarterFinalsDisplay""" + str(x - 1) + """.html'>Previous</a></div><div align='right'><a href='resultsQuarterFinalsDisplay""" + str(x) + """.html'>Next</a></div><hr>
    <iframe src='""" + self.quarterFinalsMaps[x] + """' height=1000 width=900 frameborder=0></iframe>
  </body>
</html>
"""
            htmlQuarterFinalsDisplay.write(fileContents)
            htmlQuarterFinalsDisplay.close()
            htmlResultsDisplayFile = open('resultsQuarterFinalsDisplay' + str(x) + '.html', 'w')
            if x < 3:
                fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='left'><a href='quarterFinalsDisplay""" + str(x) + """.html'>Previous</a></div><div align='right'><a href='quarterFinalsDisplay""" + str(x + 1) + """.html'>Next</a></div><hr>

  </body>
</html>
"""
            else:
                fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='left'><a href='quarterFinalsDisplay""" + str(x) + """.html'>Previous</a></div><div align='right'><a href='semiFinalsDisplayCover.html'>Next</a></div><hr>

  </body>
</html>
"""
            htmlResultsDisplayFile.write(fileContents)
            htmlResultsDisplayFile.close()


    def generateQuarterFinalsCover(self):
        htmlCoverQuarterFinalsPage = open('quarterFinalsDisplayCover.html', 'w')
        fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='center'><a href='quarterFinalsDisplay0.html'>Next</a></div><hr>
  </body>
</html>
"""
        htmlCoverQuarterFinalsPage.write(fileContents)
        htmlCoverQuarterFinalsPage.close()

    def doSemiFinals(self):
        print "Doing semi finals"
        for match in os.listdir(self.semiFinalsDir):
            matchDir = self.semiFinalsDir + match
            matchWinner = self.getMatchWinner(matchDir)
            maxSizeRoundFile = self.getMapToDisplay(matchDir, matchWinner)
            self.semiFinalsMaps.append(matchDir + '/' + maxSizeRoundFile +  '/generated.htm')
        print self.semiFinalsMaps

    def generateSemiFinalsDisplay(self):
        print "Generating semi finals display"
        for x in range(2):
            htmlSemiFinalsDisplay = open('semiFinalsDisplay' + str(x) + '.html', 'w')
            fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='left'><a href='resultsSemiFinalsDisplay""" + str(x - 1) + """.html'>Previous</a></div><div align='right'><a href='resultsSemiFinalsDisplay""" + str(x) + """.html'>Next</a></div><hr>
    <iframe src='""" + self.semiFinalsMaps[x] + """' height=1000 width=900 frameborder=0></iframe>
  </body>
</html>
"""
            htmlSemiFinalsDisplay.write(fileContents)
            htmlSemiFinalsDisplay.close()
            htmlResultsDisplayFile = open('resultsSemiFinalsDisplay' + str(x) + '.html', 'w')
            if x < 1:
                fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='left'><a href='semiFinalsDisplay""" + str(x) + """.html'>Previous</a></div><div align='right'><a href='semiFinalsDisplay""" + str(x + 1) + """.html'>Next</a></div><hr>

  </body>
</html>
"""
            else:
                fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='left'><a href='semiFinalsDisplay""" + str(x) + """.html'>Previous</a></div><div align='right'><a href='finalDisplayCover.html'>Next</a></div><hr>

  </body>
</html>
"""
            htmlResultsDisplayFile.write(fileContents)
            htmlResultsDisplayFile.close()


    def generateSemiFinalsCover(self):
        htmlCoverSemiFinalsPage = open('semiFinalsDisplayCover.html', 'w')
        fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='center'><a href='semiFinalsDisplay0.html'>Next</a></div><hr>
  </body>
</html>
"""
        htmlCoverSemiFinalsPage.write(fileContents)
        htmlCoverSemiFinalsPage.close()

    def doFinal(self):
        print "Doing final"
        for match in os.listdir(self.finalDir):
            matchDir = self.finalDir + match
            for rnd in os.listdir(matchDir):
                if not rnd.endswith('.txt'):
                    self.finalMaps.append(matchDir + '/' + rnd +  '/generated.htm')
        print self.finalMaps

    def generateFinalDisplay(self):
        print "Generating final display"
        for x in range(len(self.finalMaps)):
            htmlFinalDisplay = open('finalDisplay' + str(x) + '.html', 'w')
            fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='left'><a href='resultsFinalDisplay""" + str(x - 1) + """.html'>Previous</a></div><div align='right'><a href='resultsFinalDisplay""" + str(x) + """.html'>Next</a></div><hr>
    <iframe src='""" + self.finalMaps[x] + """' height=1000 width=900 frameborder=0></iframe>
  </body>
</html>
"""
            htmlFinalDisplay.write(fileContents)
            htmlFinalDisplay.close()
            htmlResultsDisplayFile = open('resultsFinalDisplay' + str(x) + '.html', 'w')
            if x < 7:
                fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='left'><a href='finalDisplay""" + str(x) + """.html'>Previous</a></div><div align='right'><a href='finalDisplay""" + str(x + 1) + """.html'>Next</a></div><hr>

  </body>
</html>
"""
            else:
                fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='left'><a href='finalDisplay""" + str(x) + """.html'>Previous</a></div><div align='right'><a href='championDisplay.html'>Next</a></div><hr>

  </body>
</html>
"""


            htmlResultsDisplayFile.write(fileContents)
            htmlResultsDisplayFile.close()


    def generateFinalCover(self):
        htmlCoverFinalPage = open('finalDisplayCover.html', 'w')
        fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <div align='center'><a href='finalDisplay0.html'>Next</a></div><hr>
  </body>
</html>
"""
        htmlCoverFinalPage.write(fileContents)
        htmlCoverFinalPage.close()

    def generateChampionDisplay(self):
        htmlChampionPage = open('championDisplay.html', 'w')
        fileContents = """
<html>
  <head>
    <title>
      PlanetWars Tournament
    </title>
  </head>
  <body>
    <h1>PlanetWars Champion!</h1>
  </body>
</html>
"""
        htmlChampionPage.write(fileContents)
        htmlChampionPage.close()


        
dc = DisplayCompetition()
