import phylib
import os
import sqlite3
import math
import random
import copy

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS

FRAME_INTERVAL = 0.01

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",
    "MEDIUMPURPLE",
    "LIGHTSALMON",
    "LIGHTGREEN",
    "SANDYBROWN",
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg( self ):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])

################################################################################

class RollingBall( phylib.phylib_object ):

    def __init__( self, number, pos , vel, acc):

        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        self.__class__ = RollingBall;


    # add an svg method here
    def svg( self ):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])


################################################################################
class Hole( phylib.phylib_object ):

    def __init__( self, pos ):

        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        self.__class__ = Hole;

    # add an svg method here
    def svg( self ):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)


################################################################################
class HCushion( phylib.phylib_object ):

    def __init__( self, y ):

        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y );
        self.__class__ = HCushion;

    # add an svg method here
    def svg( self ):
        if (self.obj.hcushion.y == 0):
            return """ <rect width="1400" height="25" x="-25" y="-25" fill="darkgreen" />\n"""
        elif (self.obj.hcushion.y == TABLE_LENGTH):
            return """ <rect width="1400" height="25" x="-25" y="2700" fill="darkgreen" />\n"""


################################################################################
class VCushion( phylib.phylib_object ):

    def __init__( self, x):

        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0 );
      
        self.__class__ = VCushion;
        self.x = x


    # add an svg method here
    def svg( self ):
        if (self.obj.vcushion.x == 0):
            return """ <rect width="25" height="2750" x="-25" y="-25" fill="darkgreen" />\n"""
        elif (self.obj.vcushion.x == TABLE_WIDTH):
            return """ <rect width="25" height="2750" x="1350" y="-25" fill="darkgreen" />\n"""


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg( self ):
        visual = ""
        visual += HEADER
        for obj in self:
            if obj != None:
                visual += obj.svg()
        visual += FOOTER
        return visual
    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );

                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                        Coordinate( ball.obj.still_ball.pos.x,
                                        ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

    def cueBall(self):
        for ball in self:
            if isinstance(ball, StillBall) and ball.obj.still_ball.number == 0:
                return ball
        return None

################################################################################

class Database:

    def __init__( self, reset=False ):
                    
        if reset and os.path.exists('phylib.db'):
            os.remove('phylib.db')
        
        self.conn = sqlite3.connect('phylib.db')

    def createDB( self ):
        cur = self.conn.cursor()
    
        cur.execute("""CREATE TABLE IF NOT EXISTS Ball
                (BALLID INTEGER NOT NULL,
                 BALLNO INTEGER NOT NULL,
                 XPOS   FLOAT NOT NULL,
                 YPOS   FLOAT NOT NULL,
                 XVEL   FLOAT,
                 YVEL   FLOAT,
                 PRIMARY KEY (BALLID));""")

        cur.execute("""CREATE TABLE IF NOT EXISTS TTable
                        (TABLEID    INTEGER NOT NULL,
                        TIME       FLOAT NOT NULL,
                        PRIMARY KEY (TABLEID));""")

        cur.execute("""CREATE TABLE IF NOT EXISTS BallTable
                        (BALLID     INTEGER NOT NULL,
                        TABLEID    INTEGER NOT NULL,
                        FOREIGN KEY (BALLID) REFERENCES Ball,
                        FOREIGN KEY (TABLEID) REFERENCES TTable);""")

        cur.execute("""CREATE TABLE IF NOT EXISTS Shot
                        (SHOTID     INTEGER NOT NULL,
                        PLAYERID   INTEGER NOT NULL,
                        GAMEID     INTEGER NOT NULL,
                        PRIMARY KEY (SHOTID),
                        FOREIGN KEY (PLAYERID) REFERENCES Player,
                        FOREIGN KEY (GAMEID) REFERENCES Game);""")

        cur.execute("""CREATE TABLE IF NOT EXISTS TableShot
                        (TABLEID    INTEGER NOT NULL,
                        SHOTID     INTEGER NOT NULL,
                        FOREIGN KEY (TABLEID) REFERENCES TTable,
                        FOREIGN KEY (SHOTID) REFERENCES Shot);""")

        cur.execute("""CREATE TABLE IF NOT EXISTS Game
                        (GAMEID     INTEGER NOT NULL,
                        GAMENAME   VARCHAR (64) NOT NULL,
                        PRIMARY KEY (GAMEID));""")

        cur.execute("""CREATE TABLE IF NOT EXISTS Player
                        (PLAYERID       INTEGER NOT NULL,
                        GAMEID         INTEGER NOT NULL,
                        PLAYERNAME     VARCHAR (64) NOT NULL,
                        PRIMARY KEY (PLAYERID),
                        FOREIGN KEY (GAMEID) REFERENCES Game);""")
        
        cur.close()
        self.conn.commit()

    def readTable( self, tableID ):
        cur = self.conn.cursor()

        check = cur.execute("""SELECT TABLEID FROM BallTable WHERE TABLEID = ?;""", ((tableID + 1),)).fetchone()

        if check is not None:
            table = Table()
            balls_data = cur.execute("""SELECT Ball.* FROM Ball
                                        JOIN BallTable ON Ball.BALLID = BallTable.BALLID
                                        WHERE BallTable.TABLEID = ?;""", (tableID + 1,)).fetchall()

            for ball_data in balls_data:
                ball_id, ball_no, xpos, ypos, xvel, yvel = ball_data
                pos = Coordinate(xpos, ypos)
                vel = Coordinate(xvel, yvel) if xvel is not None and yvel is not None else None

                if xvel is not None and yvel is not None:
                    speed = math.sqrt((float(xvel) ** 2) + (float(yvel) ** 2))
                else:
                    speed = 0

                if (speed > VEL_EPSILON ):
                    rb_ax = (-float(xvel) / speed * DRAG)
                    rb_ay = (-float(yvel) / speed * DRAG)
                    acc = Coordinate(rb_ax, rb_ay)

                if vel is not None:
                    ball = RollingBall(ball_no, pos, vel, acc)
                else:
                    ball = StillBall(ball_no, pos)

                table += ball

            time = cur.execute("SELECT TIME FROM TTable WHERE TABLEID = ?", (tableID + 1,)).fetchone()[0]

            table.time = time

            cur.close()
            return table
        else:
            return None
    

    def writeTable( self, table ):
        
        cur = self.conn.cursor()

        cur.execute("""INSERT INTO TTable (TIME)
                                    VALUES (?);""", (table.time,))
        table_id = cur.lastrowid

        for ball in table:
            if isinstance(ball, RollingBall):
                cur.execute("""INSERT INTO BALL (BALLNO, XPOS, YPOS, XVEL, YVEL)
                    VALUES (?, ?, ?, ?, ?);""", (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y))
                
                ball_id = cur.lastrowid
                cur.execute("""INSERT INTO BallTable    (BALLID,    TABLEID)
                                VALUES (?, ?);""",  (ball_id,   table_id))
            elif isinstance(ball, StillBall):
                cur.execute("""INSERT INTO BALL (BALLNO, XPOS, YPOS)
                            VALUES (?, ?, ?);""", (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y))

                ball_id = cur.lastrowid
                cur.execute("""INSERT INTO BallTable    (BALLID,    TABLEID)
                                    VALUES (?, ?);""",  (ball_id,   table_id))
        
        self.conn.commit()
        cur.close()

        return (table_id - 1)

    def close( self ):
        self.conn.commit() 
        self.conn.close()

    def newShot(self, playerName, gameName):
        cur = self.conn.cursor()

        playerID = cur.execute("""SELECT PLAYERID FROM Player WHERE PLAYERNAME = ?;""", (playerName,)).fetchone()[0]
        gameID = cur.execute("SELECT GAMEID FROM Game WHERE GAMENAME = ?", (gameName,)).fetchone()[0]

        cur.execute("""INSERT INTO Shot (PLAYERID, GAMEID) 
                    VALUES (?, ?);""", (playerID, gameID))
        shotID = cur.lastrowid

        self.conn.commit()
        cur.close()

        return shotID
        
################################################################################
        
class Game:

    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):
        if isinstance(gameID, int) and gameName is None and player1Name is None and player2Name is None:
            self.gameID = gameID + 1
            self.gameName, self.player1Name, self.player2Name = self.getGame(self.gameID)
        elif gameID is None and gameName is not None and player1Name is not None and player2Name is not None:
            self.gameName, self.player1Name, self.player2Name = gameName, player1Name, player2Name
            self.gameID = self.setGame(gameName, player1Name, player2Name)
        else:
            raise TypeError("Incorrect input for constructor")

    def getGame(self, gameID):
        conn = sqlite3.connect( 'phylib.db' )
        cur = conn.cursor()
        
        game_data = cur.execute("""SELECT g.GAMENAME, p1.PLAYERNAME AS player1Name, p2.PLAYERNAME AS player2Name
                                    FROM Game g JOIN Player p1 ON g.GAMEID = p1.GAMEID
                                    JOIN Player p2 ON g.GAMEID = p2.GAMEID AND p1.PLAYERID < p2.PLAYERID
                                    WHERE g.GAMEID = ?;""", (gameID,)).fetchone()
        conn.commit()
        cur.close()

        return game_data
    
    def setGame (self, gameName, player1Name, player2Name):
        conn = sqlite3.connect( 'phylib.db' )
        cur = conn.cursor()

        cur.execute("""INSERT INTO Game (GAMENAME) 
                        VALUES (?);""", (gameName,))
        gameID = cur.lastrowid

        cur.execute("""INSERT INTO Player (GAMEID, PLAYERNAME) 
                    VALUES (?, ?);""", (gameID, player1Name))
        cur.execute("""INSERT INTO Player (GAMEID, PLAYERNAME) 
                    VALUES (?, ?);""", (gameID, player2Name))

        conn.commit()
        cur.close()
        return gameID

    def shoot( self, gameName, playerName, table, xvel, yvel ):
        database = Database()
        
        shotID = database.newShot(playerName, gameName)

        cue_ball = table.cueBall()

        xpos = cue_ball.obj.still_ball.pos.x
        ypos = cue_ball.obj.still_ball.pos.y

        cue_ball.type = phylib.PHYLIB_ROLLING_BALL

        cue_ball.obj.rolling_ball.pos.x = xpos
        cue_ball.obj.rolling_ball.pos.y = ypos

        cue_ball.obj.rolling_ball.vel.x = xvel
        cue_ball.obj.rolling_ball.vel.y = yvel

        speed = math.sqrt((float(xvel) ** 2) + (float(yvel) ** 2))


        if (speed > VEL_EPSILON ):
            rb_ax = (-float(xvel) / speed * DRAG)
            rb_ay = (-float(yvel) / speed * DRAG)
        else:
            rb_ax = 0
            rb_ay = 0

        cue_ball.obj.rolling_ball.acc.x = rb_ax
        cue_ball.obj.rolling_ball.acc.y = rb_ay
        cue_ball.obj.rolling_ball.number = 0

        timeA = table.time
        copy = table

        while (copy != None):
            timeB = copy.time
            copy = Table.segment(copy)

        time = timeB - timeA

        frames = int(time / FRAME_INTERVAL)

        for a in range(frames):
            time_passed = FRAME_INTERVAL * (a + 1)
            new_table = table.roll(time_passed)
            new_table.time = timeA + time_passed
            database.writeTable(new_table)

            conn = sqlite3.connect( 'phylib.db' )
            cur = conn.cursor()
            cur.execute("""INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)""",
                            (database.writeTable(new_table), shotID))
            cur.close()
            conn.commit()

################################################################################
            
################################################################################
        
class PoolGame:

    def shoot( self, table, xvel, yvel ):        

        for ball in table:
            if isinstance(ball, StillBall) and ball.obj.still_ball.number == 0:
                cue_ball = ball

        xpos = cue_ball.obj.still_ball.pos.x
        ypos = cue_ball.obj.still_ball.pos.y

        copyCueBall = StillBall(0, Coordinate(xpos, ypos))

        cue_ball.type = phylib.PHYLIB_ROLLING_BALL

        cue_ball.obj.rolling_ball.pos.x = xpos
        cue_ball.obj.rolling_ball.pos.y = ypos

        cue_ball.obj.rolling_ball.vel.x = xvel
        cue_ball.obj.rolling_ball.vel.y = yvel

        speed = math.sqrt((float(xvel) ** 2) + (float(yvel) ** 2))

        if (speed > VEL_EPSILON ):
            rb_ax = (-float(xvel) / speed * DRAG)
            rb_ay = (-float(yvel) / speed * DRAG)
        else:
            rb_ax = 0
            rb_ay = 0

        cue_ball.obj.rolling_ball.acc.x = rb_ax
        cue_ball.obj.rolling_ball.acc.y = rb_ay
        cue_ball.obj.rolling_ball.number = 0

        svgList = []
        segment = table.segment()

        while segment is not None:
            segmentLen = segment.time - table.time

            frames = int(segmentLen / FRAME_INTERVAL)

            for a in range(frames):
                passed_time = FRAME_INTERVAL * a
                new_table = table.roll(passed_time)
                new_table.time = table.time + passed_time
                svgList.append(new_table.svg())
            
            table = segment
            segment = table.segment()
            svgList.append(table.svg())

        cue_ball = None
        for ball in table:
            if isinstance(ball, StillBall) and ball.obj.still_ball.number == 0:
                cue_ball = ball

        if cue_ball is None:
            table += copyCueBall
            svgList.append(table.svg())
        
        delimiter = "<!-- hello -->"
        svgDelimiter = delimiter.join(svgList)
        return svgDelimiter
    
    def dataOrg (self, table, ball_data):
        print("Received ball data:", ball_data)

        for ball in ball_data:
            color = ball['color']
            ball_number = BALL_COLOURS.index(color)

            x_pos = ball['x']
            y_pos = ball['y']
            pos = Coordinate(x_pos, y_pos)

            sb = StillBall(ball_number, pos)

            table += sb

        return table

    def copyTable (self, table):
        copied_table = Table()

        for ball in table:
            if isinstance(ball, StillBall):
                pos = Coordinate(ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y)
                number = ball.obj.still_ball.number
                sb = StillBall(number, pos)
                copied_table += sb
            if isinstance(ball, RollingBall):
                pos = Coordinate(ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y)
                vel = Coordinate(ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y)
                acc = Coordinate(ball.obj.rolling_ball.acc.x, ball.obj.rolling_ball.acc.y)
                number = ball.obj.rolling_ball.number
                rb = RollingBall(number, pos, vel, acc)
                copied_table += rb

        return copied_table
        
################################################################################