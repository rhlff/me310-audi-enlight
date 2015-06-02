import sys

def enoughScans(values, numberOfScans):
    numberOfMissingAreas = len(filter(lambda x: len(x) < numberOfScans, values))

    sys.stdout.write("### Still waiting for %d areas to have enough values \r ###" % ( numberOfMissingAreas ))
    sys.stdout.flush()

    return False if numberOfMissingAreas > 0 else True