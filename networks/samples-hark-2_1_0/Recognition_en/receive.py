import socket
import sys,re

host = "localhost"
port = 10500

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
print "Connection to Julius succeeded"
sys.stdout.flush()

# clear the log file
#handle = open("julius_out.txt", "w")
#handle.close()

word = {}
angle = {}
parsed = []
currentID = None

line = ""
while True:
    # build a valid line
    tmpline = sock.recv(1024).replace(".\n", "").rstrip()
    line += tmpline
    if not tmpline[-1] == ">":
        continue

    # parse it.
    print line
    res = re.search(
        '<SOURCEINFO SOURCEID="([^"]*)".*AZIMUTH="([^"]*)".*', line)
    if not res is None:
        angle[int(res.group(1))] = float(res.group(2))

    res = re.search(
        '<RECOG(OUT|FAIL) SOURCEID="([0-9]*)".*', line)
    if not res is None:
        currentID = int(res.group(2))

    if not currentID is None and "<WHYPO" in line:
        res = re.search('<WHYPO.*WORD="([^<][^"]+)".*', line)
        if not res is None:
            word[currentID] = res.group(1)
            parsed.append((currentID, angle[currentID], res.group(1)))

            out = "%d, %f, %s\n" % (currentID, angle[currentID], res.group(1))
            #handle = open("julius_out.txt", "a")
            #handle.write(out)
            #handle.close()
            #print out
            print 'source_id = %d, azimuth = %f' % (currentID, angle[currentID])
            print 'sentence1: <s> %s </s>' % res.group(1)
            sys.stdout.flush()
    line = ""

"""
for p in parsed:
    if abs(p[1] - target) < tolerance:
        print p
"""