
After doing a weak attempt at understanding how structlog works, I gave up and wrote my own logger.

Working features:

Cool potential features:
    - Individual loggers with unique names which can do any combination of printing to terminal saving to a master
     log file to which all loggers save to, & to an individual file to which this particular logger saves to.

    - Holding all log lines in memory until a certain amount of time elapses, after which all lines are saved to their
    corresponding files.

    - Hold all log files in a log directory

    - Create a new directory every time the program is run

    - Hold a maximum number of dirs & delete the oldest dir if more than the max has been created

    - Instead of deleting old dirs, move them to some other dir and compress them

    - In addition to creating a new dir & deleting old ones when the program is run, do the same thing
    when a log file exceeds a maximum number of lines

    - Save error & specially flagged logs, & some number of context lines before & after into some special place

    - Log truncated timestamps, because I don't need 100000 copies of the year, yet, do log full stamps if the
    eliminated part changes

    - Deactivate logging is some way that leaves performance in the same state as if there was no logging ever,
    also do the deactivation granularly

    - Add support for multiple gunicorn workers to save to the same log files
