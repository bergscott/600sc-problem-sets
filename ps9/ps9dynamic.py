# 6.00 Problem Set 9
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """
    inputFile = open(filename)
    subjectDict = {}
    for line in inputFile:
        line = line.strip()
        splitLine = line.split(',')
        subjectDict[splitLine[0]] = (int(splitLine[1]), int(splitLine[2]))
    return subjectDict

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    return subInfo1[0] > subInfo2[0]

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    return subInfo1[1] < subInfo2[1]

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    return subInfo1[0]/float(subInfo1[1]) > subInfo2[0]/float(subInfo2[1])

def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    result = {}
    subjects = subjects.copy()
    while subjects != {} and maxWork > 0:
        bestSubjectKey = None
        for s in subjects.keys():
            if subjects[s][1] > maxWork:
                del subjects[s]
            elif bestSubjectKey == None or \
                    comparator(subjects[s], bestSubjectValue):
                bestSubjectKey = s
                bestSubjectValue = subjects[s]
        if bestSubjectKey != None:
            result[bestSubjectKey] = bestSubjectValue
            del subjects[bestSubjectKey]
            maxWork -= bestSubjectValue[1]
    return result

#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    allCombinations = get_combinations(subjects.keys())
    bestCombination = []
    bestValue = 0
    for combination in allCombinations:
        if total_work(combination, subjects) <= maxWork:
            totVal = total_value(combination, subjects)
            if totVal > bestValue:
                bestCombination = combination
                bestValue = totVal
    result = {}
    for subj in bestCombination:
        result[subj] = subjects[subj]
    return result

def total_value(subjectList, subjectDict):
    """
    Returns the total value of all of the subjects in SUBJECTLIST.  Values are
    derived from entries in SUBJECTDICT.

    subjectList: a list
    subjectDict: a dict mapping subject name to (value, work)
    returns: an int
    """
    value = 0
    for subj in subjectList:
        value += subjectDict[subj][0]
    return value

def total_work(subjectList, subjectDict):
    """
    Returns the total work of all of the subjects in SUBJECTLIST.  Work 
    values are derived from entries in SUBJECTDICT.

    subjectList: a list
    subjectDict: a dict mapping subject name to (value, work)
    returns: an int
    """
    work = 0
    for subj in subjectList:
        work += subjectDict[subj][1]
    return work

def get_combinations(l):
    """
    Returns a list of all combinations (without repitition)
    of the elements in the given list.

    l: a list
    returns: a list
    """
    if len(l) == 0:
        return [[],]
    else:
        restCombs = get_combinations(l[1:])
        firstCombs = [[l[0]] + restCombs[i] for i in range(len(restCombs))]
        return firstCombs + restCombs

def bruteForceAdvisorDynamic(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    bestVal, bestSubjects = bfaDynamicHelper(subjects, maxWork)
    result = {}
    for subj in bestSubjects:
        result[subj] = subjects[subj]
    return result

def bfaDynamicHelper(subjects, maxWork, subjectList = None, memo = None):
    if memo == None:
        subjectList = subjects.keys()
        memo = {}
    if (len(subjectList), maxWork) in memo.keys():
        return memo[(len(subjectList), maxWork)]
    elif subjectList == [] or maxWork == 0:
        result = (0, ())
    elif subjects[subjectList[0]][1] > maxWork:
        result = bfaDynamicHelper(subjects, maxWork, 
                                  subjectList[1:], memo)
    else:
        curSub = subjects[subjectList[0]]
        withVal, withSubs = bfaDynamicHelper(subjects, 
                                             maxWork - curSub[1], 
                                             subjectList[1:], memo)
        withVal += curSub[0]
        withoutVal, withoutSubs = bfaDynamicHelper(subjects,
                                                   maxWork,
                                                   subjectList[1:], memo)
        if withVal > withoutVal:
            result = (withVal, withSubs + (subjectList[0],))
        else:
            result = (withoutVal, withoutSubs)
    memo[(len(subjectList), maxWork)] = result
    return result

## shortSubs = loadSubjects(SHORT_SUBJECT_FILENAME)
## printSubjects(shortSubs)
## mw = 8
## printSubjects(bruteForceAdvisor(shortSubs, mw))
## printSubjects(greedyAdvisor(shortSubs, mw, cmpRatio))
## printSubjects(bruteForceAdvisorDynamic(shortSubs, mw))
## longSubs = loadSubjects(SUBJECT_FILENAME)
## printSubjects(bruteForceAdvisorDynamic(longSubs, mw))
