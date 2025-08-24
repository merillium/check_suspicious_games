from venv import LichessGameDownloader, GameAnalysisEngine

def testGameAnalysisEngine():
    testEngine = GameAnalysisEngine()

def testLichessGameDownloader():
    testGameDownloader = LichessGameDownloader()
    testPGN = testGameDownloader.get_game('aLP7JnzH')
    