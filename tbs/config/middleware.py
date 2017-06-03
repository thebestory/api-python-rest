"""
The Bestory Project
"""

from tbs.lib import session

# Functions which will be executed before each request to the server
request = [
    session.middleware
]

# Functions which will be executed after each request to the server
response = []

# Alternate way to access middleware lists
all = {
    "request": request,
    "response": response
}
