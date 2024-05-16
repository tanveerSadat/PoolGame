import math
import Physics

table = Physics.Table()

pos = Physics.Coordinate(Physics.TABLE_WIDTH / 2 - math.sqrt(Physics.BALL_DIAMETER * Physics.BALL_DIAMETER / 2), 
                         Physics.TABLE_WIDTH / 2 - math.sqrt(Physics.BALL_DIAMETER * Physics.BALL_DIAMETER / 2))

sb = Physics.StillBall(1, pos)

pos = Physics.Coordinate(Physics.TABLE_WIDTH /2, Physics.TABLE_LENGTH - Physics.TABLE_WIDTH / 2)
vel = Physics.Coordinate(0.0, -1000.0)
acc = Physics.Coordinate(0.0, 180.0)

rb = Physics.RollingBall(0, pos, vel, acc)

table += sb
table += rb

count = 0

with open("table-%d.svg" % (count,), "w") as file:
    file.write(table.svg())

while (table != None):
    count += 1
    table = Physics.Table.segment(table)
    if (table != None):
        with open("table-%d.svg" % (count,), "w") as file:
            file.write(table.svg())
    
