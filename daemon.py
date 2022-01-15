def RunRss():
    from datetime import datetime, timedelta
    import os, time

    hoursdiff = 3
    currentdir = os.path.dirname(__file__)
    while True:
        now = datetime.utcnow() + timedelta(hours=8)  # Beijing time
        if now.hour in set(
                range(0, 24, hoursdiff)
        ) and now.minute <= 5:  # every 3 hours, 0~5 second is ok
            os.system('python3 ' + os.path.join(currentdir, 'thepaperRSS.py'))
            os.system('python3 ' + os.path.join(currentdir, 'reutersRSS.py'))
            os.system('python3 ' + os.path.join(currentdir, 'jwviewRSS.py'))
            time.sleep(hoursdiff * 3600)
        else:
            time.sleep(5 * 60)


def createDaemon():
    import os, sys
    # first fork
    try:
        if os.fork():
            sys.exit(1)
    except OSError as e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
    # it separates the son from the father
    os.chdir('/')
    os.setsid()
    os.umask(0)

    # second fork
    try:
        if os.fork():
            sys.exit(1)
    except OSError as e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    RunRss()


if __name__ == '__main__':
    createDaemon()
