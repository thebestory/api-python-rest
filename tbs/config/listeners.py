"""
The Bestory Project
"""

# List of listeners, that will be iterated, and each listener will be
# invoked before server start.
before_start = [
    'tbs.db.before_start_listener',
    'tbs.snowflake.before_start_listener'
]

# List of listeners, that will be iterated, and each listener will be
# invoked after server start.
after_start = []

# List of listeners, that will be iterated, and each listener will be
# invoked before server stop.
before_stop = []

# List of listeners, that will be iterated, and each listener will be
# invoked after server stop.
after_stop = [
    'tbs.db.after_stop_listener'
]
