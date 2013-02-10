import os
import webbrowser
import sys
from HTMLParser import HTMLParser
from random import randint

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

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

    players2Bots = {}
    leaguesMaps = []
    quarterFinalsMaps = []
    semiFinalsMaps = []
    finalMaps = []

    leaguesPlayers = []
    quarterFinalsPlayers = []
    quarterFinalsWinners = []
    semiFinalsPlayers = []
    semiFinalsWinners = []
    finalPlayers = []
    scores = {}
    finalScores = {}

    drawFlag = False
    drawMaps = []
    
    def __init__(self):
        self.initPlayers2Bots()
        
        self.doLeagues()
        self.initScoreRounds()
        self.generateLeaguesCover()
        self.generateLeaguesDisplay()
        self.resetScores()
        self.doQuarterFinals()
        self.generateQuarterFinalsCover()
        self.generateQuarterFinalsDisplay()
        self.resetScores()
        self.doSemiFinals()
        self.generateSemiFinalsCover()
        self.generateSemiFinalsDisplay()
        self.resetScores()
        self.doFinal()
        self.initScoreFinal()
        self.generateFinalCover()
        self.generateFinalDisplay()
        self.generateChampionDisplay()

    def initPlayers2Bots(self):
        for d in listdir_nohidden(self.submissionsDir):
            f = open(self.submissionsDir + d + '/bot.txt', 'r')
            self.players2Bots[d] = f.readline()

    def doLeagues(self):
        for league in range(1, self.numberOfLeagues + 1):
            leaguePlayers = set()
            for match in listdir_nohidden(self.leaguesDir + str(league)):
                leaguePlayers.add(match.split('-')[0])
                leaguePlayers.add(match.split('-')[1])
                matchDir = self.leaguesDir + str(league) + '/' + match
                matchWinner = self.getMatchWinner(matchDir)
                maxSizeRoundFile = self.getMapToDisplay(matchDir, matchWinner)
                if maxSizeRoundFile:
                    self.leaguesMaps.append(matchDir + '/' + maxSizeRoundFile +  '/generated.htm')
            self.leaguesPlayers.append(list(leaguePlayers))
            #print self.leaguesMaps
        #print len(self.leaguesMaps)
        #print self.leaguesPlayers

    def initScoreRounds(self):
        for league in self.leaguesPlayers:
            for player in league:
                self.scores[player] = 0

    def initScoreFinal(self):
        self.finalScores['0'] = 0
        for player in self.finalPlayers:
            self.finalScores[player] = 0

    def getMatchWinner(self, matchDir):
        match = matchDir.split('/')[-1]
        playerA = match.split('-')[0]
        playerAWins = 0
        playerB = match.split('-')[1]
        playerBWins = 0
        if 'draw' in listdir_nohidden(matchDir):
            matchDir = matchDir + '/draw/'
        for rnd in listdir_nohidden(matchDir):
            if rnd.split('.')[-1] != "txt":
                continue
            winner = rnd.split('_')[0][1:]
            if winner == playerA:
                playerAWins += 1
            elif winner == playerB:
                playerBWins += 1
            elif winner == '0':
                playerAWins += 1
                playerBWins += 1
            else:
                print "ERROR SOLVING MATCH"
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
            print matchDir
            matchWinner = playerA
            matchLooser = playerB
            self.drawFlag = True
        #print "Group {} wins against group {}".format(matchWinner, matchLooser)
        return matchWinner

    def getMapToDisplay(self, matchDir, matchWinner):
        wonRoundFiles = [rnd for rnd in listdir_nohidden(matchDir) if rnd.split('_')[0] == 'w' + matchWinner and rnd.split('.')[-1] != 'txt']
        try:
            selectedMap = wonRoundFiles[randint(0,len(wonRoundFiles)-1)]
            if self.drawFlag:
                self.drawMaps.append(selectedMap)
                self.drawFlag = False
                print "FOOOOOOOOOOOOOOOO"
                print self.drawMaps
            return selectedMap
        except ValueError:
            print "unable to find map in dir. Probably crashed for all maps"
       

    def resetScores(self):
        for x,y in self.scores.iteritems():
            self.scores[x] = 0

    def generateLeaguesDisplay(self):
        #roundDisplayParser = RoundDisplayHTMLParser()
        #roundDisplayParser.feed()

        for x in range(9):
            htmlLeagueDisplayFile = open('leagueDisplay' + str(x) + '.html', 'w')
            fileContents = """
<html>
  <head>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
  <script src="js/jquery.tablesorter.js"></script>
  <script src="js/competition.js"></script>
    <title>
      PlanetWars Tournament
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div class="next"><a href='resultsDisplay""" + str(x) + """.html'><img src="imgs/next.png" height="16px" width="16px"></img></a></div>
    <iframe src='""" + self.leaguesMaps[x + 0] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + self.leaguesMaps[x + 10] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + self.leaguesMaps[x + 20] + """' height=1000 width=900 frameborder=0></iframe>
"""
            if x < 6:
                fileContents += """
    <iframe src='""" + self.leaguesMaps[x + 30] + """' height=1000 width=900 frameborder=0></iframe>
"""
            fileContents += """
  </body>
</html>
"""
            htmlLeagueDisplayFile.write(fileContents)
            htmlLeagueDisplayFile.close()
            
            winner1 = self.leaguesMaps[x].split('/')[-2].split('_')[0][1:]
            winner2 = self.leaguesMaps[x+10].split('/')[-2].split('_')[0][1:]
            winner3 = self.leaguesMaps[x+20].split('/')[-2].split('_')[0][1:]
            if x < 6:
                winner4 = self.leaguesMaps[x+30].split('/')[-2].split('_')[0][1:]
            for draws in self.drawMaps:
                if draws not in self.leaguesMaps[x]:
                    self.scores[winner1] += 3
                else:
                    onePlayer = self.leaguesMaps[x].split('/')[-2].split('_')[1].split('-')[0]
                    otherPlayer = self.leaguesMaps[x].split('/')[-2].split('_')[1].split('-')[1]
                    self.scores[onePlayer] += 1
                    self.scores[otherPlayer] += 1
                if draws not in self.leaguesMaps[x+10]:
                    self.scores[winner2] += 3
                else:
                    onePlayer = self.leaguesMaps[x+10].split('/')[-2].split('_')[1].split('-')[0]
                    otherPlayer = self.leaguesMaps[x+10].split('/')[-2].split('_')[1].split('-')[1]
                    self.scores[onePlayer] += 1
                    self.scores[otherPlayer] += 1
                if draws not in self.leaguesMaps[x+20]:
                    self.scores[winner3] += 3
                else:
                    onePlayer = self.leaguesMaps[x+20].split('/')[-2].split('_')[1].split('-')[0]
                    otherPlayer = self.leaguesMaps[x+20].split('/')[-2].split('_')[1].split('-')[1]
                    self.scores[onePlayer] += 1
                    self.scores[otherPlayer] += 1
                if x < 6:
                    if draws not in self.leaguesMaps[x+30]:
                        self.scores[winner4] += 3
                    else:
                        onePlayer = self.leaguesMaps[x+30].split('/')[-2].split('_')[1].split('-')[0]
                        otherPlayer = self.leaguesMaps[x+30].split('/')[-2].split('_')[1].split('-')[1]
                        self.scores[onePlayer] += 1
                        self.scores[otherPlayer] += 1
            htmlResultsDisplayFile = open('resultsDisplay' + str(x) + '.html', 'w')
            fileContents = """
<html>
  <head>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="js/jquery.tablesorter.js"></script>
  <script src="js/competition.js"></script>
    <title>
      PlanetWars Tournament
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div class="next"><a href='"""
            if x < 8:
                fileContents += """leagueDisplay""" + str(x + 1) + """.html"""
            else:
                fileContents += """quarterFinalsDisplayCover.html"""
            fileContents += """
'><img src="imgs/next.png" height="16px" width="16px"></img></a></div>
    <div align='center' style='width:900px; margin:20px auto;'>
    <div style='float:center'>
"""
            leagueId = 1
            for league in self.leaguesPlayers:
                
                fileContents += """
    <table class="tablesorter"><thead><tr><th align="left">Group Stage """ + str(leagueId) + """</th><th>&nbsp;</th></tr></thead><tbody>
"""             
                for player in league:
                    fileContents += """
      <tr>
        <td>""" + self.players2Bots['group' + player]  + """</td><td>""" + str(self.scores[player]) + """</td>
      </tr>
"""
                fileContents += """
    </tbody></table>
"""             
                leagueId +=  1
            fileContents += """
    </div>
    </div>

  </body>
</html>
"""
            htmlResultsDisplayFile.write(fileContents)
            htmlResultsDisplayFile.close()

    def generateLeaguesCover(self):
        htmlCoverPage = open('leagueDisplayCover.html', 'w')
        fileContents = """
<html>
  <head>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="js/jquery.tablesorter.js"></script>
  <script src="js/competition.js"></script>
    <title>
      PlanetWars Tournament
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div class="next"><a href='leagueDisplay0.html'><img src="imgs/next.png" height="16px" width="16px"></img></a></div>
    <div style='float:center'>
"""
        leagueId = 1
        for league in self.leaguesPlayers:
            fileContents += """
    <table class="tablesorter"><thead><tr><th align="left">Group Stage """ + str(leagueId) + """</th><th>&nbsp;</th></tr></thead><tbody>
""" 
            for player in league:
                fileContents += """
      <tr>
       <td>""" + self.players2Bots['group' + player]  + """</td><td>""" + str(self.scores[player]) + """</td>
      </tr>
"""
            fileContents += """
    </tbody></table>
"""
            leagueId += 1
        fileContents += """
    </div>
    </div>
  </body>
</html>
"""
        htmlCoverPage.write(fileContents)
        htmlCoverPage.close()

    def doQuarterFinals(self):
        print "Doing quarter finals"
        for match in listdir_nohidden(self.quarterFinalsDir):
            quarterPlayers = set()
            quarterPlayers.add(match.split('-')[0])
            quarterPlayers.add(match.split('-')[1])
            matchDir = self.quarterFinalsDir + match
            matchWinner = self.getMatchWinner(matchDir)
            self.quarterFinalsWinners.append(matchWinner)
            #maxSizeRoundFile = self.getMapToDisplay(matchDir, matchWinner)
            quarterMaps = []
            for rnd in listdir_nohidden(self.quarterFinalsDir + match):
                if not rnd.endswith('.txt') and rnd != 'draw':
                    quarterMaps.append(matchDir + '/' + rnd + '/generated.htm')
                if rnd == 'draw':
                    for rnd2 in listdir_nohidden(self.quarterFinalsDir + match + '/' + rnd):
                        if not rnd2.endswith('.txt'):
                            quarterMaps.append(matchDir + '/' + rnd + '/' + rnd2 + '/generated.htm')
            self.quarterFinalsMaps.append(quarterMaps)
            self.quarterFinalsPlayers.append(list(quarterPlayers))
        print self.quarterFinalsPlayers
        print self.quarterFinalsMaps

    def generateQuarterFinalsDisplay(self):
        print "Generating quarter finals display"
        indexPager = 0
        for qmap in self.quarterFinalsMaps:
            rnds = []
            if len(qmap) == 8:
                rnds = [0,4]
            else:
                rnds = [0,4,8]
            for x in rnds:
                #print qmap
                #print x
                htmlQuarterFinalsDisplay = open('quarterFinalsDisplay' + str(indexPager)  + '.html', 'w')
                fileContents = """
<html>
  <head>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="js/jquery.tablesorter.js"></script>
  <script src="js/competition.js"></script>
    <title>
      PlanetWars Tournament
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div class="next"><a href="""
                if indexPager > 6:
                    fileContents += """'resultsQuarterFinalsDisplay.html'"""
                else:
                    fileContents += """'quarterFinalsDisplay""" + str(indexPager + 1) + """.html'"""
                fileContents += """><img src="imgs/next.png" height="16px" width="16px"></img></a></div>
    <iframe src='""" + qmap[x] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + qmap[x + 1] + """' height=1000 width=900 frameborder=0></iframe>
"""
                if len(qmap) != 10 or x != 8:
                    fileContents += """
    <iframe src='""" + qmap[x + 2] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + qmap[x + 3] + """' height=1000 width=900 frameborder=0></iframe>
"""
                fileContents += """
  </body>
</html>
"""
    
                htmlQuarterFinalsDisplay.write(fileContents)
                htmlQuarterFinalsDisplay.close()
                indexPager += 1


            htmlResultsDisplayFile = open('resultsQuarterFinalsDisplay.html', 'w')
            fileContents = """
<html>
  <head>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="js/jquery.tablesorter.js"></script>
  <script src="js/competition.js"></script>
    <title>
      PlanetWars Tournament
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div class="next"><a href='semiFinalsDisplayCover.html'><img src="imgs/next.png" height="16px" width="16px"></img></a></div>
    <div style='float:center'>
"""
            quarterFinalId = 1;
            for quarter in self.quarterFinalsPlayers:
                fileContents += """
    <table class="tablesorter"><thead><tr><th align="left">Quarter Final """ + str(quarterFinalId) + """</th><th>&nbsp;</th></tr></thead><tbody>
""" 
                for player in quarter:
                    if player in self.quarterFinalsWinners:
                        self.scores[player] = 1
                    fileContents += """
      <tr>
       <td>""" + self.players2Bots['group' + player]  + """</td><td>""" + str(self.scores[player]) + """</td>
      </tr>
"""
                quarterFinalId += 1
                fileContents += """
    </tbody></table>
"""
            fileContents += """
    </div>
    </div>

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
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="js/jquery.tablesorter.js"></script>
  <script src="js/competition.js"></script>
    <title>
      PlanetWars Tournament
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div class="next"><a href='quarterFinalsDisplay0.html'><img src="imgs/next.png" height="16px" width="16px"></img></a></div>
    <div style='float:center'>
"""
        quarterFinalId = 1
        for quarter in self.quarterFinalsPlayers:
            fileContents += """
    <table class="tablesorter"><thead><tr><th align="left">Quarter Final """ + str(quarterFinalId) + """</th><th>&nbsp;</th></tr></thead><tbody>
""" 
            for player in quarter:
                fileContents += """
      <tr>
        <td>""" + self.players2Bots['group' + player]  + """</td><td>""" + str(self.scores[player]) + """</td>
      </tr>
"""
            fileContents += """
    </tbody></table>
"""
            quarterFinalId += 1
        fileContents += """
    </div>
    </div>

  </body>
</html>
"""
        htmlCoverQuarterFinalsPage.write(fileContents)
        htmlCoverQuarterFinalsPage.close()

    def doSemiFinals(self):
        print "Doing semi finals"
        for match in listdir_nohidden(self.semiFinalsDir):
            semiPlayers = set()
            semiPlayers.add(match.split('-')[0])
            semiPlayers.add(match.split('-')[1])
            matchDir = self.semiFinalsDir + match
            matchWinner = self.getMatchWinner(matchDir)
            self.semiFinalsWinners.append(matchWinner)
            #maxSizeRoundFile = self.getMapToDisplay(matchDir, matchWinner)
            semiMaps = []
            for rnd in listdir_nohidden(self.semiFinalsDir + match):
                if not rnd.endswith('.txt') and rnd != 'draw':
                    semiMaps.append(matchDir + '/' + rnd + '/generated.htm')
                if rnd == 'draw':
                    for rnd2 in listdir_nohidden(self.semiFinalsDir + match + '/' + rnd):
                        if not rnd2.endswith('.txt'):
                            semiMaps.append(matchDir + '/' + rnd + '/' + rnd2 + '/generated.htm')
            self.semiFinalsMaps.append(semiMaps)
            self.semiFinalsPlayers.append(list(semiPlayers))
        print self.semiFinalsMaps
        print self.semiFinalsPlayers

    def generateSemiFinalsDisplay(self):
        print "Generating semi finals display"
        indexPager = 0
        for smap in self.semiFinalsMaps:
            rnds = []
            if len(smap) == 8:
                rnds = [0,4]
            else:
                rnds = [0,4,8]
            for x in rnds:
                htmlSemiFinalsDisplay = open('semiFinalsDisplay' + str(indexPager)  + '.html', 'w')
                fileContents = """
<html>
  <head>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="js/jquery.tablesorter.js"></script>
  <script src="js/competition.js"></script>
    <title>
      PlanetWars Tournament
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div class="next"><a href="""
                if indexPager > 2:
                    fileContents += """'resultsSemiFinalsDisplay.html'"""
                else:
                    fileContents += """'semiFinalsDisplay""" + str(indexPager + 1) + """.html'"""
                fileContents += """><img src="imgs/next.png" height="16px" width="16px"></img></a></div>
    <iframe src='""" + smap[x] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + smap[x + 1] + """' height=1000 width=900 frameborder=0></iframe>
"""
                if len(smap) != 10 or x != 8:
                    fileContents += """
    <iframe src='""" + smap[x + 2] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + smap[x + 3] + """' height=1000 width=900 frameborder=0></iframe>
"""
                fileContents += """
  </body>
</html>
"""
    
                htmlSemiFinalsDisplay.write(fileContents)
                htmlSemiFinalsDisplay.close()
                indexPager += 1


            htmlResultsDisplayFile = open('resultsSemiFinalsDisplay.html', 'w')
            fileContents = """
<html>
  <head>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="js/jquery.tablesorter.js"></script>
  <script src="js/competition.js"></script>
    <title>
      PlanetWars Tournament
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div class="next"><a href='finalDisplayCover.html'><img src="imgs/next.png" height="16px" width="16px"></img></a><div>
    <div style='float:center'>
"""
            semiFinalId = 1
            for semi in self.semiFinalsPlayers:
                fileContents += """
    <table class="tablesorter"><thead><tr><th align="left">Semi Final """ + str(semiFinalId) + """</th><th>&nbsp;</th></tr></thead><tbody>
""" 
                for player in semi:
                    if player in self.semiFinalsWinners:
                        self.scores[player] = 1
                    fileContents += """
      <tr>
        <td>""" + self.players2Bots['group' + player]  + """</td><td>""" + str(self.scores[player]) + """</td>
      </tr>
"""
                fileContents += """
    </tbody></table>
"""
                semiFinalId += 1
            
            fileContents += """
    </div>
    </div>

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
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="js/jquery.tablesorter.js"></script>
  <script src="js/competition.js"></script>
    <title>
      PlanetWars Tournament
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div class="next"><a href='semiFinalsDisplay0.html'><img src="imgs/next.png" height="16px" width="16px"></img></a></div>
    <div style='float:center'>
"""
        semiFinalId = 1
        for semi in self.semiFinalsPlayers:
            fileContents += """
    <table class="tablesorter"><thead><tr><th align="left">Semi Final """ + str(semiFinalId) + """</th><th>&nbsp;</th></tr></thead><tbody>
""" 
            for player in semi:
                fileContents += """
      <tr>
        <td>""" + self.players2Bots['group' + player]  + """</td><td>""" + str(self.scores[player]) + """</td>
      </tr>
"""
            fileContents += """
    </tbody></table>
"""
            semiFinalId += 1
        fileContents += """
    </div>
    </div>

  </body>
</html>
"""

        htmlCoverSemiFinalsPage.write(fileContents)
        htmlCoverSemiFinalsPage.close()

    def doFinal(self):
        print "Doing final"
        for match in listdir_nohidden(self.finalDir):
            matchDir = self.finalDir + match
            self.finalPlayers.append(match.split('-')[0])
            self.finalPlayers.append(match.split('-')[1])
            for rnd in listdir_nohidden(matchDir):
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
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="js/jquery.tablesorter.js"></script>
  <script src="js/competition.js"></script>
    <title>
      PlanetWars Tournament
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div class="next"><a href='resultsFinalDisplay""" + str(x) + """.html'><img src="imgs/next.png" height="16px" width="16px"></img></a></div>
    <iframe src='""" + self.finalMaps[x] + """' height=1000 width=900 frameborder=0></iframe>
  </body>
</html>
"""
            htmlFinalDisplay.write(fileContents)
            htmlFinalDisplay.close()

            self.finalScores[self.finalMaps[x].split('/')[-2].split('_')[0][1:]] += 1
            
            htmlResultsDisplayFile = open('resultsFinalDisplay' + str(x) + '.html', 'w')
            if x < 7:
                fileContents = """
<html>
  <head>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="js/jquery.tablesorter.js"></script>
  <script src="js/competition.js"></script>
    <title>
      PlanetWars Tournament
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div class="next"><a href='finalDisplay""" + str(x + 1) + """.html'><img src="imgs/next.png" height="16px" width="16px"></img></a></div>
    <div align='center' style='width:900px; margin:20px auto;'>

    <table class="tablesorter"><thead><tr><th align="left">Final</th><th>&nbsp;</th></tr></thead><tbody>
      <tr>
        <td>""" + self.players2Bots['group' + self.finalPlayers[0]]  + """</td><td>""" + str(self.finalScores[self.finalPlayers[0]])  + """</td>
      </tr>
      <tr>
        <td>""" + self.players2Bots['group' + self.finalPlayers[1]]  + """</td><td>""" + str(self.finalScores[self.finalPlayers[1]])  + """</td>
      </tr>
    </tbody></table>

    </div>

  </body>
</html>
"""
            else:
                fileContents = """
<html>
  <head>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="js/jquery.tablesorter.js"></script>
  <script src="js/competition.js"></script>
    <title>
      PlanetWars Tournament
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div class="next"><a href='championDisplay.html'><img src="imgs/next.png" height="16px" width="16px"></img></a></div>
    <div align='center' style='width:900px; margin:20px auto;'>

    <table class="tablesorter"><thead><tr><th align="left">Final</th><th>&nbsp;</th></tr></thead><tbody>
      <tr>
        <td>""" + self.players2Bots['group' + self.finalPlayers[0]]  + """</td><td>""" + str(self.finalScores[self.finalPlayers[0]])  + """</td>
      </tr>
      <tr>
        <td>""" + self.players2Bots['group' + self.finalPlayers[1]]  + """</td><td>""" + str(self.finalScores[self.finalPlayers[1]])  + """</td>
      </tr>
    </tbody></table>

    </div>


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
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="js/jquery.tablesorter.js"></script>
  <script src="js/competition.js"></script>
    <title>
      PlanetWars Tournament
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div class="next"><a href='finalDisplay0.html'><img src="imgs/next.png" height="16px" width="16px"></img></a></div>
    <div align='center' style='width:900px; margin:20px auto;'>

    <table class="tablesorter"><thead><tr><th align="left">Final</th><th>&nbsp;</th></tr></thead><tbody>
      <tr>
       <td>""" + self.players2Bots['group' + self.finalPlayers[0]]  + """</td><td>0</td>
      </tr>
      <tr>
      <td>""" + self.players2Bots['group' + self.finalPlayers[1]]  + """</td><td>0</td>
      </tr>
    </tbody></table>

    </div>
  </body>
</html>
"""
        htmlCoverFinalPage.write(fileContents)
        htmlCoverFinalPage.close()

    def generateChampionDisplay(self):
        maxScore = 0
        for player,score in self.finalScores.iteritems():
            if score > maxScore:
                champion = player
                maxScore = score
        htmlChampionPage = open('championDisplay.html', 'w')
        fileContents = """
<html>
  <head>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="js/jquery.tablesorter.js"></script>
  <script src="js/competition.js"></script>
    <title>
      PlanetWars Tournament
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <h1>PlanetWars Champion!</h1>
    <h2>""" + self.players2Bots['group' + champion] + """</h2>
  </body>
</html>
"""
        htmlChampionPage.write(fileContents)
        htmlChampionPage.close()


        
dc = DisplayCompetition()
