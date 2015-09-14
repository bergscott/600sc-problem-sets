# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared 
        from the  patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """

        return random.random() < self.clearProb

    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        if random.random() < self.maxBirthProb * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException

class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):

        """

        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop

    def getTotalPop(self):

        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """

        return len(self.viruses)

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        # determine whether each virus particle survives
        survivingViruses = []
        for virus in self.viruses:
            if not virus.doesClear():
                survivingViruses.append(virus)
        # calculate current population density
        popDensity = len(survivingViruses) / float(self.maxPop)
        # determine whether each virus reproduces, if so add to list
        newViruses = survivingViruses[:]
        for virus in survivingViruses:
            try:
                newViruses.append(virus.reproduce(popDensity))
            except NoChildException:
                pass
        # update self.viruses with new list of viruses
        self.viruses = newViruses[:]
        # return total virus population
        return len(self.viruses)

def test_simple():
    zeroCount = 0
    for x in range(50):          
        vs = [SimpleVirus(.5,.2),]
        p = SimplePatient(vs, 100)
        for t in range(100):
            p.update()
        numv = len(p.viruses)
        if numv == 0:
            zeroCount += 1
        print len(p.viruses)
    print 'Zero count: ' + str(zeroCount)

#
# PROBLEM 2
#
def simulationWithoutDrug():

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    NUMTRIALS = 100
    numViruses = [0 for x in range(300)]
    hundredViruses = []
    for x in range(100):
        hundredViruses.append(SimpleVirus(0.1, 0.05))
    for trial in range(NUMTRIALS):
        viruses = hundredViruses[:]
        patient = SimplePatient(viruses, 1000)
        for t in range(300):
            numViruses[t] += patient.update()
    avgNumViruses = [100]
    for i in range(len(numViruses)):
        avgNumViruses.append(numViruses[i] / float(NUMTRIALS))
    pylab.plot(avgNumViruses, label='average of 100 trials')
    pylab.xlabel('time steps')
    pylab.ylabel('virus population')
    pylab.title('Growth over time of a virus population with max reproduction\n'+\
                'prob 0.1 and max clearance prob 0.05 in untreated patient')
    pylab.legend(loc='lower right')
    pylab.show()

def testSimulationWithoutDrug(repro, clear, trials):
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    numViruses = [0 for x in range(300)]
    hundredViruses = []
    for x in range(100):
        hundredViruses.append(SimpleVirus(repro, clear))
    for trial in range(trials):
        viruses = hundredViruses[:]
        patient = SimplePatient(viruses, 1000)
        for t in range(300):
            numViruses[t] += patient.update()
    avgNumViruses = [100]
    for i in range(len(numViruses)):
        avgNumViruses.append(numViruses[i] / float(trials))
    pylab.plot(avgNumViruses, label='average of ' + str(trials) + ' trials')
    pylab.xlabel('time steps')
    pylab.ylabel('virus population')
    pylab.title('Average growth of a virus population with max reproduction\n' +\
                'prob ' + str(repro) + ' and max clearance prob ' + str(clear) +\
                ' in untreated patient')
    pylab.legend(loc='lower right')
    pylab.show()
    

