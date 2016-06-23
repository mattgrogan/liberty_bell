class Events:
    """ These are the events that can be raised during play

    UI Events
    -------------
    SPIN: The UI spin button was pressed
    INCREMENT_BET: The UI increment bet button was pressed
    DECREMENT_BET: The UI decrement bet button was pressed

    Model Events
    -------------
    CREDITS_CHANGED: The number of credits the player has has changed
    PAYOUT: The player has won and is receiving a payout
    PLACE_BET: The player has spun the reels and must pay!
    BET_CHANGED: The amount bet has changed
    """
    SPIN, INCREMENT_BET, DECREMENT_BET,  CREDITS_CHANGED, PAYOUT, PLACE_BET, BET_CHANGED = range(7)
