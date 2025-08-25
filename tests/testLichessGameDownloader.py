from app.LichessGameDownloader import LichessGameDownloader

def testLichessGameDownloader():
    testGameDownloader = LichessGameDownloader()
    testGameDownloader.get_game('aLP7JnzH')
    testPGN = testGameDownloader.pgn
    print(testPGN)