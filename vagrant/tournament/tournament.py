#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection and cursor."""
    # https://review.udacity.com/#!/reviews/334258
    try:
        conn = psycopg2.connect("dbname=tournament")
        cursor = conn.cursor()
        return conn, cursor
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""
    conn, cursor = connect()
    cursor.execute("truncate table matches cascade;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, cursor = connect()
    cursor.execute("truncate table players cascade;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, cursor = connect()
    # https://discussions.udacity.com/t/countplayers-returning-non-zero/26638/5
    query = """Select Count(*) From players;"""
    cursor.execute(query)
    player_count = cursor.fetchall()
    return int(player_count[0][0])


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn, cursor = connect()
    cursor.execute("Insert into players(name) values(%s)", (name,))
    return conn.commit()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    query = '''select * from scores;'''

    conn, cursor = connect()
    cursor.execute(query)
    return list(cursor.fetchall())


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    insert = '''insert into matches (winner, loser) values(%s, %s)'''
    values = [winner, loser]
    conn, cursor = connect()
    cursor.execute(insert, values)

    return conn.commit()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    query = '''
    select a.player_id, a.name, b.player_id, b.name 
    from scores a, scores b
    where a.player_id > b.player_id
    and a.wins = b.wins
    order by a.player_id'''
    
    conn, cursor = connect()
    cursor.execute(query)
    match_list = list(cursor.fetchall())

    def merge(x):
        s = set()
        for i in x:
            if not s.intersection(i):
                yield i
                s.update(i)

    return list(merge(match_list))


