class Skip:
    '''
    Singleton that represents a 'skip' move in the game 

    Returns: 
        skip: Skip
    '''
    class __Skip:
        def __init__(self):
            pass

        def __eq__(self, other):
            return self is other

        def __repr__(self):
            return "SKIP"

        def __hash__(self):
            return 0

    instance = None
    def __new__(self):
        if not Skip.instance:
            Skip.instance = Skip.__Skip()
        return Skip.instance
