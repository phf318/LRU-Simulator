"""
@author  pzx
CS- Operating Systems
Summer June 2022

Usage:  python lrutest.py -n <numframes> -a <counter|stack|arb|second_chance>  <tracefile>

"""
import sys
import parseInput as parse
import pageTable as pt
import counter as counter
import stack as stack
import ARB as arb
import Second_Chance as sc
import time

####################################
### PARSE INPUT FROM TRACE FILES ###
####################################



####################
### CONTROL FLOW ###
####################
def main():
    # get user input from command line args, store it in a list
    cmdLineArgs = getUserInput()

    # get the user input from our list, so we can use it in main
    try:
        num_frames = int(cmdLineArgs[0])
    except:
        print "Number of frames not specified properly."
        print "Usage:  python lrutest.py -n <numframes> -a <counter|stack|arb|second_chance> <tracefile>"

    algorithm = cmdLineArgs[1]
    if cmdLineArgs[2] is not None:
        refresh = float(cmdLineArgs[2])
    traceFile = cmdLineArgs[3]


    # parse the input and store it
    memory_addresses = parse.parse_trace_file(traceFile)

    # build the model for our page table, 32bit address space
    # initialize our table
    pageTable = pt.PageTable(num_frames)


    # write stack algorithm
    if algorithm == "stack":
        t0 = time.time()
        OptAlgorithm = stack.LRU(pageTable, memory_addresses)
        OptAlgorithm.run_algorithm()
        t1 = time.time()
        total = t1 - t0
        print "TOTAL RUNNING TIME IN MINUTES: " + str(total * 0.0166667)

    # write ARB algorithm
    if algorithm == "arb":
        t0 = time.time()
        clock_algorithm = arb.LRU(pageTable, memory_addresses)
        clock_algorithm.run_algorithm()
        t1 = time.time()
        total = t1 - t0
        print "TOTAL RUNNING TIME IN MINUTES: " + str(total * 0.0166667)


    # write second chance algorithm
    if algorithm == "second_chance":
        t0 = time.time()
        clock_algorithm = sc.LRU(pageTable, memory_addresses)
        clock_algorithm.run_algorithm()
        t1 = time.time()
        total = t1-t0
        print "TOTAL RUNNING TIME IN MINUTES: " + str(total*0.0166667)



    # write counter algorithm
    elif algorithm == "counter":
        t0 = time.time()
        LRU_algorithm = counter.LRU(pageTable, memory_addresses)
        LRU_algorithm.run_algorithm()
        t1 = time.time()
        total = t1-t0
        print "TOTAL RUNNING TIME IN MINUTES: " + str(total*0.0166667)


    else:
        print "Invalid algorithm name. Acceptable choices are:" \
              "\n\t- 'counter' \n\t- 'arb' \n\t- 'stack' \n\t- 'second_chance' " \
              "\n\n\tNote: algorithm names are case sensitive\n"

        print "Usage:  python lrutest.py -n <numframes> -a <counter|stack|arb|second_chance> <tracefile>\n"
    return


# NOTE:  Need to change this later... because once we start using -n, etc., the arg values will change
def getUserInput():
    """ Gets user input and saves as class level variables
        :return A list of arguments passed in by the user
    """
    # create a list of argumenst to return, and index variables, so we can find args
    arglist = []
    counter = 0
    num_frames_index = 0
    algorithm_index = 0
    refresh_index = 0
    args = sys.argv

    # parse command line arguments and get our argument indices
    for elem in sys.argv:
        element = elem
        if elem == "-n":
            num_frames_index = counter + 1
        if elem == "-a":
            algorithm_index = counter + 1
        if elem == "-r":
            refresh_index = counter + 1
        counter += 1

    # check that input is okay
    if algorithm_index == 0:
        print "Usage:  python lrutest.py -n <numframes> -a <counter|stack|arb|second_chance> <tracefile>"



    # get the num frames and algorithm selection
    num_frames = sys.argv[2]
    algorithm = sys.argv[algorithm_index]
    # and append them to the list
    arglist.append(num_frames)
    arglist.append(algorithm)

    arglist.append(None)

    # append the tracefile last, since it is always our final argument
    tracefile = sys.argv[-1]
    arglist.append(tracefile)

    # return the list we've built
    return arglist



###################
### ENTRY POINT ###
###################

if __name__ == "__main__":
    main()

