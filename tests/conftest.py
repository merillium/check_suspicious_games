import pytest

@pytest.fixture(params=['aLP7JnzH','XXXXXXX-'])
def getGameCode(request):
    """
    aLP7JnzH = suspicious game
    XXXXXXX- = invalid game
     = non suspicious game
    """
    return request.param