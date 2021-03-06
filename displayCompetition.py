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

#checks if the directory exist if not make them  
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

class DisplayCompetition(object):
    submissionsDir = 'submissions/'
    tournamentResultsDir = 'tournamentResults/'
    leaguesDir = tournamentResultsDir + '0/'
    quarterFinalsDir = tournamentResultsDir + '1/'
    semiFinalsDir = tournamentResultsDir + '2/'
    finalDir = tournamentResultsDir + '3/'

    ensure_dir(submissionsDir)
    ensure_dir(tournamentResultsDir)
    ensure_dir(leaguesDir)
    ensure_dir(quarterFinalsDir)
    ensure_dir(semiFinalsDir)
    ensure_dir(finalDir)

    quarterFinalsRound = 1
    semiFinalsRound = 2
    finalRound = 4
    numberOfLeagues = 4
    gamesPerMatch = 10

    players2Bots = {}
    leaguesMaps = []
    quarterFinalsMaps = []
    semiFinalsMaps = []
    finalMaps = []

    allPlayers = []
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
    fakeFlag = False
    fakeMaps = []
    
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
        # self.generateChampionDisplay()

    def initPlayers2Bots(self):
        for d in listdir_nohidden(self.submissionsDir):
            f = open(self.submissionsDir + d + '/bot.txt', 'r')
            self.players2Bots[d] = f.readline()
            self.scores[d.split('group')[1]] = 0
        print self.players2Bots

    def doLeagues(self):
        for league in range(1, self.numberOfLeagues + 1):
            leaguePlayers = set()

            
            if not os.path.isdir(self.leaguesDir + str(league)):
                os.makedirs(self.leaguesDir + str(league))

            for match in listdir_nohidden(self.leaguesDir + str(league)):
                leaguePlayers.add(match.split('-')[0])
                leaguePlayers.add(match.split('-')[1])
                matchDir = self.leaguesDir + str(league) + '/' + match
                if not os.path.isdir(matchDir):
                    os.makedirs(matchDir)
                matchWinner = self.getMatchWinner(matchDir)
                maxSizeRoundFile = self.getMapToDisplay(matchDir, matchWinner)
                if maxSizeRoundFile:
                    self.leaguesMaps.append(matchDir + '/' + maxSizeRoundFile +  '/generated.htm')
            self.leaguesPlayers.append(list(leaguePlayers))

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
            matchWinner = playerA
            matchLooser = playerB
            self.drawFlag = True
        #print "Group {} wins against group {}".format(matchWinner, matchLooser)
        return matchWinner

    def getMatchesWinners(self, matchDir):
        winnerSequence = []
        match = matchDir.split('/')[-1]
        playerA = match.split('-')[0]
        playerAWins = 0
        playerB = match.split('-')[1]
        playerBWins = 0
        for rnd in listdir_nohidden(matchDir):
            winner = -1
            if not rnd.endswith('.txt') and rnd != 'draw':
                if os.path.isdir(self.semiFinalsDir + match + '/draw/') and rnd in listdir_nohidden(self.semiFinalsDir + match + '/draw/'):
                    winner = 0
                else:
                    winner = rnd.split('_')[0][1:]
                winnerSequence.append(winner)
        return winnerSequence

    def earlyWinner(self, players):
        for p in players:
            if self.scores[p] == self.gamesPerMatch/2 + 1:
                return True
        return False

    def getMapToDisplay(self, matchDir, matchWinner):
        wonRoundFiles = [rnd for rnd in listdir_nohidden(matchDir) if rnd.split('_')[0] == 'w' + matchWinner and rnd.split('.')[-1] != 'txt']
        if len(wonRoundFiles) == 0:
            self.fakeFlag = True
            wonRoundFiles = [rnd.split('.')[0] for rnd in listdir_nohidden(matchDir) if rnd.split('_')[0] == 'w' + matchWinner]
        # Probably all draws, select random map
        if len(wonRoundFiles) == 0:
            wonRoundFiles = [rnd for rnd in listdir_nohidden(matchDir) if rnd.split('.')[-1] != 'txt']
        randomPointer = randint(0,len(wonRoundFiles)-1)
        selectedMap = wonRoundFiles[randomPointer]
        if self.drawFlag:
            self.drawMaps.append(matchDir + '/' + selectedMap + '/generated.htm')
            self.drawFlag = False
        if self.fakeFlag:
            self.fakeMaps.append(selectedMap)
            self.fakeFlag = False
        return selectedMap


    def resetScores(self):
        for x,y in self.scores.iteritems():
            self.scores[x] = 0

    def generateLeaguesDisplay(self):
        #roundDisplayParser = RoundDisplayHTMLParser()
        #roundDisplayParser.feed()

        n = len(self.leaguesPlayers[0]) - 1 if self.numberOfLeagues > 0 else 0
        m = len(self.leaguesPlayers[1]) - 1 if self.numberOfLeagues > 0 else 0
        maxMatchesLargestLeague = (n * (n + 1))/2
        maxMatchesRegularLeagues = (m * (m + 1))/2
        for x in range(maxMatchesLargestLeague):
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
"""
            print self.leaguesMaps
            if x < maxMatchesRegularLeagues:
                fileContents += """
    <iframe src='""" + self.leaguesMaps[x + 6] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + self.leaguesMaps[x + 12] + """' height=1000 width=900 frameborder=0></iframe>
    <iframe src='""" + self.leaguesMaps[x + 18] + """' height=1000 width=900 frameborder=0></iframe>
"""
            fileContents += """
  </body>
</html>
"""
            htmlLeagueDisplayFile.write(fileContents)
            htmlLeagueDisplayFile.close()
            
            winner1 = self.leaguesMaps[x].split('/')[-2].split('_')[0][1:]
            if x < maxMatchesRegularLeagues:
                winner2 = self.leaguesMaps[x+6].split('/')[-2].split('_')[0][1:]
                winner3 = self.leaguesMaps[x+12].split('/')[-2].split('_')[0][1:]
                winner4 = self.leaguesMaps[x+18].split('/')[-2].split('_')[0][1:]

            if self.leaguesMaps[x] not in self.drawMaps:
                self.scores[winner1] += 3
            else:
                onePlayer = self.leaguesMaps[x].split('/')[-2].split('_')[1].split('-')[0]
                otherPlayer = self.leaguesMaps[x].split('/')[-2].split('_')[1].split('-')[1]
                self.scores[onePlayer] += 1
                self.scores[otherPlayer] += 1
            if self.leaguesMaps[x+6] not in self.drawMaps:
                self.scores[winner2] += 3
            else:
                onePlayer = self.leaguesMaps[x+6].split('/')[-2].split('_')[1].split('-')[0]
                otherPlayer = self.leaguesMaps[x+6].split('/')[-2].split('_')[1].split('-')[1]
                self.scores[onePlayer] += 1
                self.scores[otherPlayer] += 1
            if self.leaguesMaps[x+12] not in self.drawMaps:
                self.scores[winner3] += 3
            else:
                onePlayer = self.leaguesMaps[x+12].split('/')[-2].split('_')[1].split('-')[0]
                otherPlayer = self.leaguesMaps[x+12].split('/')[-2].split('_')[1].split('-')[1]
                self.scores[onePlayer] += 1
                self.scores[otherPlayer] += 1
            if x < 10:
                if self.leaguesMaps[x+18] not in self.drawMaps:
                    self.scores[winner4] += 3
                else:
                    onePlayer = self.leaguesMaps[x+18].split('/')[-2].split('_')[1].split('-')[0]
                    otherPlayer = self.leaguesMaps[x+18].split('/')[-2].split('_')[1].split('-')[1]
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
            if x < maxMatchesLargestLeague - 1:
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
        nextPage = 'leagueDisplay0.html' if self.numberOfLeagues > 0 else 'quarterFinalsDisplayCover.html'
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
    <div class="next"><a href=""" + nextPage  + """><img src="imgs/next.png" height="16px" width="16px"></img></a></div>
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
            matchesWinners = self.getMatchesWinners(matchDir)
            self.quarterFinalsWinners.append(matchesWinners)
            #maxSizeRoundFile = self.getMapToDisplay(matchDir, matchWinner)
            quarterMaps = []
            for rnd in listdir_nohidden(self.quarterFinalsDir + match):
                if not rnd.endswith('.txt') and rnd != 'draw':
                    if os.path.isdir(self.quarterFinalsDir + match + '/draw/') and rnd  in listdir_nohidden(self.quarterFinalsDir + match + '/draw/'):
                         quarterMaps.append(matchDir + '/draw/' + rnd + '/generated.htm')
                    else:
                        quarterMaps.append(matchDir + '/' + rnd + '/generated.htm')
            self.quarterFinalsMaps.append(quarterMaps)
            self.quarterFinalsPlayers.append(list(quarterPlayers))
        print self.quarterFinalsPlayers
        print self.quarterFinalsMaps
        print self.quarterFinalsWinners

    def generateQuarterFinalsDisplay(self):
        print "Generating quarter finals display"
        indexPager = 0
        maxQuarterFinalsMatches = 0
        for qmap in self.quarterFinalsMaps:
            if len(qmap) > maxQuarterFinalsMatches:
                maxQuarterFinalsMatches = len(qmap)
        print maxQuarterFinalsMatches
        for x in range(maxQuarterFinalsMatches):
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
    <div class="next"><a href='resultsQuarterFinalsDisplay""" + str(x) + """.html'><img src="imgs/next.png" height="16px" width="16px"></img></a></div>"""

            print self.quarterFinalsWinners
            if not self.earlyWinner(self.quarterFinalsPlayers[0]) and  x < len(self.quarterFinalsMaps[0]):
                fileContents += """        
    <iframe src='""" + self.quarterFinalsMaps[0][x] + """' height=1000 width=900 frameborder=0></iframe>"""
            if not self.earlyWinner(self.quarterFinalsPlayers[1]) and x < len(self.quarterFinalsMaps[1]):
                fileContents += """        
    <iframe src='""" + self.quarterFinalsMaps[1][x] + """' height=1000 width=900 frameborder=0></iframe>"""
            if not self.earlyWinner(self.quarterFinalsPlayers[2]) and x < len(self.quarterFinalsMaps[2]):
                fileContents += """        
    <iframe src='""" + self.quarterFinalsMaps[2][x] + """' height=1000 width=900 frameborder=0></iframe>"""
            if not self.earlyWinner(self.quarterFinalsPlayers[3]) and x < len(self.quarterFinalsMaps[3]):
                fileContents += """        
    <iframe src='""" + self.quarterFinalsMaps[3][x] + """' height=1000 width=900 frameborder=0></iframe>"""

            fileContents += """
  </body>
</html>
"""
    
            htmlQuarterFinalsDisplay.write(fileContents)
            htmlQuarterFinalsDisplay.close()
            indexPager += 1


            htmlResultsDisplayFile = open('resultsQuarterFinalsDisplay' + str(x) + '.html', 'w')
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
"""
            if x < maxQuarterFinalsMatches - 1:
                fileContents +="""
    <div class="next"><a href='quarterFinalsDisplay""" + str(x + 1)  + """.html'>
"""
            else:
                fileContents +="""
    <div class="next"><a href='semiFinalsDisplayCover.html'>
"""

            fileContents +="""
<img src="imgs/next.png" height="16px" width="16px"></img></a></div>
    <div style='float:center'>
"""
            quarterFinalId = 1;
            for quarter in self.quarterFinalsPlayers:
                fileContents += """
    <table class="tablesorter"><thead><tr><th align="left">Quarter Final """ + str(quarterFinalId) + """</th><th>&nbsp;</th></tr></thead><tbody>
""" 
                for player in quarter:
                    if x < len(self.quarterFinalsWinners[quarterFinalId-1]) and player == self.quarterFinalsWinners[quarterFinalId-1][x] and not self.earlyWinner(quarter):
                        self.scores[player] += 1
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
            matchesWinners = self.getMatchesWinners(matchDir)
            self.semiFinalsWinners.append(matchesWinners)
            #maxSizeRoundFile = self.getMapToDisplay(matchDir, matchWinner)
            semiMaps = []
            for rnd in listdir_nohidden(self.semiFinalsDir + match):
                if not rnd.endswith('.txt') and rnd != 'draw':
                    if os.path.isdir(self.semiFinalsDir + match + '/draw/') and rnd in listdir_nohidden(self.semiFinalsDir + match + '/draw/'):
                        semiMaps.append(matchDir + '/draw/' + rnd + '/generated.htm')
                    else:
                        semiMaps.append(matchDir + '/' + rnd + '/generated.htm')
            self.semiFinalsMaps.append(semiMaps)
            self.semiFinalsPlayers.append(list(semiPlayers))
        print self.semiFinalsMaps
        print self.semiFinalsPlayers

    def generateSemiFinalsDisplay(self):
        print "Generating semi finals display"
        indexPager = 0
        maxSemiFinalsMatches = 0
        for smap in self.semiFinalsMaps:
            if len(smap) > maxSemiFinalsMatches:
                maxSemiFinalsMatches = len(smap)
        print maxSemiFinalsMatches
        for x in range(maxSemiFinalsMatches):
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
    <div class="next"><a href='resultsSemiFinalsDisplay""" + str(x) + """.html'><img src="imgs/next.png" height="16px" width="16px"></img></a></div>"""

            if not self.earlyWinner(self.semiFinalsPlayers[0]) and x < len(self.semiFinalsMaps[0]):
                fileContents += """        
    <iframe src='""" + self.semiFinalsMaps[0][x] + """' height=1000 width=900 frameborder=0></iframe>"""
            if not self.earlyWinner(self.semiFinalsPlayers[1]) and x < len(self.semiFinalsMaps[1]):
                fileContents += """        
    <iframe src='""" + self.semiFinalsMaps[1][x] + """' height=1000 width=900 frameborder=0></iframe>"""

            fileContents += """
  </body>
</html>
"""
    
            htmlSemiFinalsDisplay.write(fileContents)
            htmlSemiFinalsDisplay.close()
            indexPager += 1


            htmlResultsDisplayFile = open('resultsSemiFinalsDisplay' + str(x) + '.html', 'w')
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
"""
            if x < maxSemiFinalsMatches - 1:
                fileContents +="""
    <div class="next"><a href='semiFinalsDisplay""" + str(x + 1)  + """.html'>
"""
            else:
                fileContents +="""
    <div class="next"><a href='finalDisplayCover.html'>
"""

            fileContents +="""
<img src="imgs/next.png" height="16px" width="16px"></img></a></div>
    <div style='float:center'>
"""
            semiFinalId = 1;
            print self.semiFinalsWinners
            for semi in self.semiFinalsPlayers:
                fileContents += """
    <table class="tablesorter"><thead><tr><th align="left">Semi Final """ + str(semiFinalId) + """</th><th>&nbsp;</th></tr></thead><tbody>
""" 
                for player in semi:
                    if x < len(self.semiFinalsWinners[semiFinalId-1]) and player == self.semiFinalsWinners[semiFinalId-1][x] and not self.earlyWinner(semi):
                        self.scores[player] += 1
                    fileContents += """
      <tr>
       <td>""" + self.players2Bots['group' + player]  + """</td><td>""" + str(self.scores[player]) + """</td>
      </tr>
"""
                semiFinalId += 1
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
            if x < len(self.finalMaps) - 1 and self.finalScores[self.finalPlayers[0]] < len(self.finalMaps)/2 + 1 and self.finalScores[self.finalPlayers[1]] < len(self.finalMaps)/2 + 1:
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
    <div align='center' style='width:900px; margin:20px auto;'>
    <img src="imgs/winnertext.png"></img><br>
    <img src="imgs/marvin.jpg"></img><br>
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
