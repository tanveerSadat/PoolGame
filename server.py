import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future
import os
import math
import Physics
import json
import time

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler;

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl;


# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):    

    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        # check if the web-pages matches the list
        if parsed.path == '/StartGame':
            with open('StartGame.html', 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())

            # Read the PoolGame.html file
            with open("PoolGame.html", "r") as file:
                # Read the existing content
                html_content = file.read()

            # Find the index of <body> start and end tags
            start_body_index = html_content.find('<body onload="randomizePlayer()">')
            end_body_index = html_content.find('</body>')

            # Define the new body content for PoolGame.html
            old_body_content = f"""
<div id="player 1">
    <!-- Add player 1 name here -->
</div>
<svg id="poolTable" width="700" height="1370" xmlns="http://www.w3.org/2000/svg" 
xmlns:xlink="http://www.w3.org/1999/xlink"
onmousedown="startDrag(event);">
    <!-- SVG content will be dynamically loaded here -->
</svg>
<div id="player 2">
    <!-- Add player 2 name here -->
</div> 
"""

            # Replace the <body> content with the new body content
            updated_html_content = html_content[:start_body_index + len('<body onload="randomizePlayer()">')] + old_body_content + html_content[end_body_index:]

            # Write the updated content back to PoolGame.html
            with open("PoolGame.html", "w") as file:
                file.write(updated_html_content)
        
        if parsed.path == '/PoolGame':

            pos = Physics.Coordinate(Physics.TABLE_WIDTH / 2, Physics.TABLE_LENGTH - Physics.TABLE_WIDTH / 2)

            cue_ball = Physics.StillBall(0, pos)

            table = Physics.Table()
            table += cue_ball

            # Define the positions for the other fifteen balls using a for loop
            positions = [
                (Physics.TABLE_WIDTH / 2, Physics.TABLE_LENGTH / 4),
                (Physics.TABLE_WIDTH / 2 + 65, Physics.TABLE_LENGTH / 4),
                (Physics.TABLE_WIDTH / 2 - 65, Physics.TABLE_LENGTH / 4),
                (Physics.TABLE_WIDTH / 2 + 130, Physics.TABLE_LENGTH / 4),
                (Physics.TABLE_WIDTH / 2 - 130, Physics.TABLE_LENGTH / 4),
                (Physics.TABLE_WIDTH / 2 - (65 / 2), Physics.TABLE_LENGTH / 4 - 55),
                (Physics.TABLE_WIDTH / 2 + (65 / 2), Physics.TABLE_LENGTH / 4 - 55),
                (Physics.TABLE_WIDTH / 2, Physics.TABLE_LENGTH / 4 - 110),  # 8-ball in the middle
                (Physics.TABLE_WIDTH / 2 - (65 / 2 + 65), Physics.TABLE_LENGTH / 4 - 55),
                (Physics.TABLE_WIDTH / 2 + (65 / 2 + 65), Physics.TABLE_LENGTH / 4 - 55),
                (Physics.TABLE_WIDTH / 2 + 65, Physics.TABLE_LENGTH / 4 - 110),
                (Physics.TABLE_WIDTH / 2 - 65, Physics.TABLE_LENGTH / 4 - 110),
                (Physics.TABLE_WIDTH / 2 - (65 / 2), Physics.TABLE_LENGTH / 4 - 165),
                (Physics.TABLE_WIDTH / 2 + (65 / 2), Physics.TABLE_LENGTH / 4 - 165),
                (Physics.TABLE_WIDTH / 2, Physics.TABLE_LENGTH / 4 - 220)
            ]

            # Create and add balls to the table using the defined positions
            for i, pos in enumerate(positions, start=1):
                ball = Physics.StillBall(i, Physics.Coordinate(*pos))
                table += ball

            print("table:\n", table)

            count = 0

            with open("table-%d.svg" % (count,), "w") as file:
                file.write(table.svg())
            
            # Read the SVG content from the file
            with open("table-%d.svg" % (count,), "r") as file:
                content = file.read()
            
             # Serve the PoolGame.html file with the SVG content embedded
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("PoolGame.html", "rb") as file:
                html_content = file.read()
                html_content = html_content.replace(b'<!-- SVG content will be dynamically loaded here -->', content.encode())
                self.wfile.write(html_content)
            
        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


    def do_POST(self):
        # hanle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );            

        if parsed.path == '/StartGame':
            # Get the content length from the headers
            content_length = int(self.headers['Content-Length'])
            # Read the POST data
            post_data = self.rfile.read(content_length)
            # Parse the POST data
            post_data = post_data.decode('utf-8')
            post_data = json.loads(post_data)

            # Extract player names and assigned balls information
            player1 = post_data.get('player1')
            player2 = post_data.get('player2')

            print("Player 1 is ", player1)
            print("Player 2 is ", player2)

            # Read the PoolGame.html file
            with open("PoolGame.html", "r") as file:
                html_content = file.read()

            # Replace the placeholders with dynamic player names
            html_content = html_content.replace('<!-- Add player 1 name here -->', f'<p>Player 1: {player1}</p>')
            html_content = html_content.replace('<!-- Add player 2 name here -->', f'<p>Player 2: {player2}</p>')

            # Write the modified HTML content back to the file
            with open("PoolGame.html", "w") as file:
                file.write(html_content)

            # Respond to the client
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Player names updated successfully")
            

        if parsed.path in [ '/PoolGame' ]:

            # Parse the POST request data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_parameters = json.loads(post_data)

            # Extract velocity components from POST request data
            xvel = post_parameters.get('velocityX', 0)
            yvel = post_parameters.get('velocityY', 0)
            ball_data = post_parameters.get('ballData', [])

            table = Physics.Table()

            pool_game_instance = Physics.PoolGame()
            table = pool_game_instance.dataOrg(table, ball_data)

            svgs = pool_game_instance.shoot(table, xvel, yvel)

            # Set the HTTP response headers
            self.send_response(200)
            self.send_header('Content-type', 'image/svg+xml')
            self.end_headers()

            # Send the SVG data
            self.wfile.write(svgs.encode('utf-8'))

        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();
