import dispy, random, time, sys
from decimal import getcontext, Decimal

# argv: [how many nodes][how many tests][how many rolls]

getcontext().prec = 40

global ip_master
global ip_nodes_raw

ip_master = ""
ip_nodes_raw = [""]

if ip_master == "" or len(ip_nodes_raw) == 0:
    print "First set ip_master and nodes' ip"
    exit()

realPi = "3.14159265358979323846264338327950288419716"

def leibniz (start, stop):
    from decimal import getcontext, Decimal
    getcontext().prec = 40

    result = Decimal(0.0)
    #result = 0.0
    for k in xrange(start, stop):
        result += Decimal(((-1.0)**(k))/(2*k+1.0))
        #result += ((-1.0)**(k))/(2*k+1.0)

    return result

def getDigit (pi):
    pi = str(pi)[2:]
    rPi = realPi[2:]
    for i in xrange(len(realPi)):
        if pi[i] != rPi[i]:
            return i

def run (nNodes, nTimes, nThrows):
    ip_nodes = []

    for i in range (nNodes):
        ip_nodes.append(ip_nodes_raw[i])

    cluster = dispy.JobCluster(
        leibniz,
        nodes = ip_nodes,
        ip_addr = ip_master
    )

    jobs = []

    for i in range(nTimes):
        jobs.append(cluster.submit(nThrows*i, nThrows*(i+1)))

    cluster.wait()
    cluster.stats()

    raw = Decimal(0.0)
    #raw = 0.0
    for j in jobs:
        raw += j.result    

    pi = 4*raw

    return pi 

if __name__ == "__main__":

    tStart = time.time()

    calculatedPi = run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))

    tEnd = time.time() - tStart

    print "Computation real time: " + str(tEnd)[:5] + " sec\n"

    print "Total loops: " + str(int(sys.argv[2]) * int(sys.argv[3]))

    print "Calculated PI: " + str(calculatedPi)
    print "Real PI:       " + str(realPi)
    print "Digit:         " + str(getDigit(calculatedPi)) + "\n"