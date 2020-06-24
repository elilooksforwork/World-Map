# WorldMap
A Spherical World Map between 2 points, or via city to display a flight graphically

The Html file works with the flightVia.js 

You'll need to install the procs for SQL Server found in WorldMap_MSSQL_Part.sql
The cities data is found in arcCity.txt (bcp or in SSMS paste inside an edit table grid)
The Python_Server.py is a bare bones python/flask server to get the data - there is some validation, not much
(You'll need to setup py pages in IIS - google it)

Put the 1B.htm file along with World4.htm and flightVia.js in a IIS virtual directory
The 110-countries.json file should be under virtual directory in json folder

World-Globe.png a snapshot of how flight is tracked; via city is in red and departure and arrival in white.





