"""
The Bestory Project
"""

from tbs import (
    db,
    snowflake_generator
)


# List of listeners, that will be iterated, and each listener will be
# invoked before server start.
before_start = [
    db.before_start_listener,
    snowflake_generator.before_start_listener
]

# List of listeners, that will be iterated, and each listener will be
# invoked after server start.
after_start = [
    db.after_start_listener
]

# List of listeners, that will be iterated, and each listener will be
# invoked before server stop.
before_stop = []

# List of listeners, that will be iterated, and each listener will be
# invoked after server stop.
after_stop = [
    db.after_stop_listener
]
