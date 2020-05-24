import sys
from client import *

from utils.json_reader import *

def main(argv):

    client = HomestuckUpdater()

    jsonLoader = JsonReader()

    client.run(jsonLoader.getServerKey())
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
