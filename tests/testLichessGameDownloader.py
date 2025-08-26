from app.LichessGameDownloader import LichessGameDownloader

def testLichessGameDownloader(getGameCode):
    try:
        testGameDownloader = LichessGameDownloader()
        testGameDownloader.get_game(getGameCode)
    except ValueError as e:
        print(f"Caught exception {e}")