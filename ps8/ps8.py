# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:



import numpy
import random
import pylab
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a 
        drug.        

        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.resistances[drug]

    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        for d in activeDrugs:
            if not self.isResistantTo(d):
                raise NoChildException
        if random.random() < self.maxBirthProb * (1 - popDensity):
            newResistances = {}
            for r in self.resistances.keys():
                if random.random() < self.mutProb:
                    newResistances[r] = not self.resistances[r]
                else:
                    newResistances[r] = self.resistances[r]
            return ResistantVirus(self.maxBirthProb, self.clearProb,
                                  newResistances, self.mutProb)
        else:
            raise NoChildException

## def test_resistant_virus():
##     v1 = ResistantVirus(0.5, 0.05, {'Bergozol':True}, 0.5)
##     v2 = ResistantVirus(0.99, 0.05, {'Bergozol':False}, 0.5)
##     def test_reproduce(virus):
##         return virus.reproduce(0, ['Bergozol',])
##     return test_reproduce(v1)
##     
## test_resistant_virus()
 
class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        SimplePatient.__init__(self, viruses, maxPop)
        self.drugs = []

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)

    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.drugs

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        resistantViruses = 0
        for virus in self.viruses:
            for drug in drugResist:
                if virus.isResistantTo(drug):
                    resistantViruses += 1
                    break
        return resistantViruses

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
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
                newViruses.append(virus.reproduce(popDensity, 
                                                  self.getPrescriptions()))
            except NoChildException:
                pass
        # update self.viruses with new list of viruses
        self.viruses = newViruses[:]
        # return total virus population
        return len(self.viruses)

## def test_patient():
##     v1 = ResistantVirus(0.5, 0.05, {'Bergozol':True, 'Dotoxil':True}, 0.5)
##     v2 = ResistantVirus(0.99, 0.05, {'Bergozol':False, 'Dotoxil':False}, 0.5)
##     viruses = [v1, v2]
##     p = Patient(viruses, 1000)
##     p.addPrescription('Bergozol')
##     p.addPrescription('Dotoxil')
##     assert p.getPrescriptions() == ['Bergozol', 'Dotoxil']
##     assert p.getResistPop(p.getPrescriptions()) == 1
##     print 'test_patient(): all tests passed!'
##     print p.update()
## 
## test_patient()


#
# PROBLEM 2
#
# Constant Definitions and Variable Initializations
RESISTANCES = {'guttagonol':False}
NUM_TRIALS = 100
MAX_POP = 1000
REPRO_RATE = 0.1
CLEAR_RATE = 0.05
MUT_RATE = 0.005
VIRUSES = []
for v in xrange(100):
    VIRUSES.append(ResistantVirus(REPRO_RATE,CLEAR_RATE,RESISTANCES,MUT_RATE))

def simulationWithDrug():

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    totalPops = [0 for i in xrange(300)]
    resistantPops = [0 for i in xrange(300)]
    # Run simulation
    for trial in xrange(NUM_TRIALS):
        patient = Patient(VIRUSES[:], MAX_POP)
        # simulate pre-treatment time steps
        for time in xrange(150):
            totalPops[time] += patient.update()
            resistantPops[time] += patient.getResistPop(RESISTANCES.keys())
        # add prescription and simulate post-treatment time steps
        patient.addPrescription('guttagonol')
        for time in xrange(150, 300):
            totalPops[time] += patient.update()
            resistantPops[time] += patient.getResistPop(RESISTANCES.keys())
            
    # cjalculate average populations
    avgTotalPops = [100]
    avgResistantPops = [0]
    for i in xrange(len(totalPops)):
        avgTotalPops.append(totalPops[i] / NUM_TRIALS)
        avgResistantPops.append(resistantPops[i] / NUM_TRIALS)

    # plot results
    pylab.plot(avgTotalPops, label='Total Virus Population')
    pylab.plot(avgResistantPops, label='Resistant Virus Population\n' +\
                                       'mutation rate = ' + str(MUT_RATE))
    pylab.xlabel('time steps')
    pylab.ylabel('number of viruses')
    pylab.title('Average (of ' + str(NUM_TRIALS) + ' trials) ' +\
                'growth of a virus population with max reproduction\n' +\
                'prob ' + str(REPRO_RATE) + ' and max clearance prob ' +\
                str(CLEAR_RATE) + ' in a patient treated after 150 time steps')
    pylab.legend(loc='upper right')
    pylab.show()

#
# PROBLEM 3
#        
def runSimulation(delay):
    totalTime = delay + 150
    totalPops = [0 for i in xrange(totalTime)]
    patient = Patient(VIRUSES[:], MAX_POP)
    # simulate pre-treatment time steps
    for time in xrange(delay):
        totalPops[time] = patient.update()
    # add prescription and simulate post-treatment time steps
    patient.addPrescription('guttagonol')
    for time in xrange(delay, totalTime):
        totalPops[time] = patient.update()
    return totalPops[-1]
            
def simulationDelayedTreatment():
    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    histBins = [i*50 for i in range(11)]
    delays = [0, 75, 150, 300]
    subplot = 1
    for d in delays:
        results = []
        for t in xrange(NUM_TRIALS):
            results.append(runSimulation(d))
        pylab.subplot(2, 2, subplot)
        subplot += 1
        pylab.hist(results, bins=histBins, label='delayed ' + str(d))
        pylab.xlim(0, 500)
        pylab.ylim(0, NUM_TRIALS)
        pylab.ylabel('number of patients')
        pylab.xlabel('total virus population')
        pylab.title(str(d) + ' time step delay')
        ##print str(d) + ' step delay: ' + str(results)
    pylab.suptitle('Patient virus populations after 150 time steps when ' +\
                   'prescription\n' +\
                   'is applied after delays of 0, 75, 150, 300 time steps')
    pylab.show()    

simulationDelayedTreatment()   


#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment():

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    # TODO



#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations():

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """
    #TODO



