import numpy as np
import lal
import lalsimulation

print("running...")


#######################################################
#  hOfF  (m1, m2)
#
#	Generates a template in strain data 
#	for a given set of parameters. 
# 	In this current case, m1 and m2 
#	are the parameters with which 
#	the template's strain data is 
#	generated.
#
#     Parameters Passed:
#        m1       --> Guess for mass of the larger BH
#        m2       --> Guess for mass of the smaller BH
#
#     Return Value:
#       Given parameters (in this case m1, m2), 
#	the template's strain data is calculated 
# 	and returned.
#
######################################################
def hOfF(m1, m2):

	m1 *= lal.lal.MSUN_SI
	m2 *= lal.lal.MSUN_SI

	fmin = 10
	fmax = 512
	deltaF = 1.0/8
	dist = 100

	H = lalsimulation.SimIMRPhenomP(0, 0, 0, 0, m1, m2, 1000*1e6*lal.lal.PC_SI, 0, 0, deltaF, fmin, fmax, 20, 1, None)

	return H[0].data.data + H[1].data.data

#######################################################
#  lnLikelihood (m1, m2, Lcomplex, LNoise, Hcomplex, HNoise)
#
#     Calculates the log of the Likihood, the
#     log P( d1,d2 | theta).
#
# 	[Check paper :				]
#	[ http://arxiv.org/pdf/0911.3820v2.pdf  ]
#	[ appendix eq A19 and A20		]
#
#
#     Parameters Passed:
#        m1 	  --> Guess for mass of the larger BH
#        m2 	  --> Guess for mass of the smaller BH
#	 Lcomplex --> Livingston's Strain real+img part
#	 LNoise	  --> Livingston's Noise Varience 	
#        Hcomplex --> Hanford's Strain real+img part
#        HNoise   --> Hanford's Noise Varience  
#
#     Return Value:
#       Given parameters (in this case m1, m2), 
#	the likilihood for the strain data 
#       to match the template h is returned 
#
######################################################
def logLikelihood (m1, m2, Lcomplex, LNoise, Hcomplex, HNoise):


''' OLD VERSION TO CALCULATE LnL --- depricated 

        # hOfF generates the template in strain 
        #Return value of the hOfF function
        hOfF_value = hOfF(m1,m2)



	lnLikelihoodConstant = 1.0 # should be np.log(......)

	#  UNSURE OF THE lnLikelihoodExp FORMULA!! CHECK!!!!
	T = 8.0

	# Z = a+ib
	# C = x+iy
	#
	# (Z-C)^2
	# = ((a+ib) - (x+iy))^2
	# = ((a-x)  + i(b-y))^2
	# = ((a-x)^2 + (-1)(b-y)^2 +2(a-x)(b-y))


	Hr_hOfFr = np.real(Hcomplex)- np.real(hOfF_value)
	Hi_hOfFi = np.imag(Hcomplex)- np.imag(hOfF_value)
	Hi_hOfF_sqr = np.absolute(Hr_hOfFr**2.0 - Hi_hOfFi**2.0 + 2.0*Hr_hOfFr*Hi_hOfFi)
	lnLikelihoodExp_H= (-2.0/T)* np.sum( Hi_hOfF_sqr * (1.0/HNoise['noiseVar']))

	Lr_hOfFr = np.real(Lcomplex)- np.real(hOfF_value)
	Li_hOfFi = np.imag(Lcomplex)- np.imag(hOfF_value)


	Li_hOfF_sqr = np.absolute(Lr_hOfFr**2.0 - Li_hOfFi**2.0 + 2.0*Lr_hOfFr*Li_hOfFi)

	lnLikelihoodExp_L= (-2.0/T)* np.sum(Li_hOfF_sqr * (1.0/LNoise['noiseVar']) )

	lnLikelihoodExp = lnLikelihoodExp_H+lnLikelihoodExp_L
	lnLikelihood =  lnLikelihoodExp #+ lnLikelihoodConstant

'''
	
	# hOfF generates the template in strain 
        hOfF_value = hOfF(m1,m2)

	# Hf_hofF and Lf_hofF are the  |data-h|^2   /  noise 
	# Calculating the (data - template) for H and L 
	Hf_hofF= np.zeros(len(hOfF_value))
	Hf_hofF = Hcomplex - hOfF_value

	Lf_hofF= np.zeros(len(hOfF_value))
	Lf_hofF = Lcomplex - hOfF_value

	#vdot-> dot prod that takes the The vdot(a, b) function handles complex numbers differently than dot(a, b).
	#	 If the first argument is complex the complex conjugate of the first argument is used for the calculation of the dot product.

	# Calculating the (data - template)^2 / Noise 
	lnLikelihoodExp_Ha = (-2.0/T) * np.absolute(np.vdot(Hf_hofF,Hf_hofF/ HNoise['noiseVar']))
	
	# print ( lnLikelihoodExp_Ha)
	# print ( np.absolute(np.vdot(Hcomplex,Hcomplex)) )
	#print("without subtraction %f" %lnLikelihoodExp_Ha)

	
	lnLikelihoodExp_Ha = lnLikelihoodExp_Ha + (2.0/T)*np.absolute(np.vdot(Hcomplex,Hcomplex/ HNoise['noiseVar']))
	
	#print("after subtraction %f" %lnLikelihoodExp_Ha)
	#print("the constant:")
	
	# x is just a test variable 
	#x = ( np.absolute(np.vdot(Hcomplex,Hcomplex/ HNoise['noiseVar'])))
	#print (x)

	lnLikelihoodExp_La = (-2.0/T) * np.absolute(np.vdot(Lf_hofF,Lf_hofF/ LNoise['noiseVar']))


	# Only calculated for Hanford Data set 
	lnLikelihood_new = lnLikelihoodExp_Ha#+lnLikelihoodExp_La

	return lnLikelihood_new





#######################################################
#  Importing the raw data files into numpy arrays

Freq = np.dtype([ ('f', np.float), ('real', np.float),('imag', np.float)])
Noise = np.dtype([('f',np.float),('noiseVar',np.float)])

from numpy import *
HFreq = loadtxt('H1-freqDataWithInj.dat',dtype=Freq)
LFreq = loadtxt('L1-freqDataWithInj.dat',dtype=Freq)
HNoise = loadtxt('H1-noiseVar.dat', dtype = Noise)
LNoise = loadtxt('H1-noiseVar.dat', dtype = Noise)
Hcomplex = HFreq['real'] + 1j*HFreq['imag']
Lcomplex = LFreq['real'] + 1j*LFreq['imag']

#print(HFreq['f'][1])




#######################################################

# List of Solar Masses (20~50 solar masses)
SolarMass = float(1.989e+30)
dm = 0.1
mass_list = np.arange(20,50,dm)

# mass_list = mass_list * SolarMass

############## Posterior Distribution Calculation  ##############



################# MODEL 1 : Data = signal + noise #################



numMassVals = len(mass_list)**2.0### len(mass_list)**2 is excessive!
MASS1= 0
MASS2= 1
mass = np.zeros((2,numMassVals))


lnLikelihood = 0.0 # one value of the likilihood for each set of m1, m2
lnPrior = np.log(1.0/numMassVals)     # should this be --> np.log(1/(numMassVals) or  np.log( 1 / (len(mass_list) * len(mass_list[:i])) ) ??? # Did not understand how I would be able to implement Jeffories Prior : https://en.wikipedia.org/wiki/Jeffreys_prior
evidence = 0.0
lnEvidence = 0.0
lnPosterior = np.zeros(numMassVals) ##### numMassVals IS EXCESSIVE
lnPosteriorValue = 0.0
count = 0

# Iterating through the mass list so m1 > m2
# For each set of m1 and m2, we will calculate the log of the lnLikelihood of each value
for i, m1 in enumerate(mass_list):
    for j, m2 in enumerate(mass_list[:i]): # we do not need to look past m1 for the mass of m2 as m1>m2 always
		# now have 1 set of m1 and m2 (st m1>m2)

		#Calculating the log of the Likihood <- f() return one lnLikelihood for current m1, m2
		lnLikelihood = logLikelihood(m1,m2,Lcomplex,LNoise,Hcomplex,HNoise)    # Check  the formula for the exponents!

		lnPosterior[count] = lnLikelihood +lnPrior

		mass[MASS1][count] = m1
		mass[MASS2][count] = m2
		count+=1



# Calculating the posterior of each value

# Incorrect! Cant sum like this!
# lnEvidence = np.sum(lnPosterior + np.log(dm))

#MadeUpConstant = 4500


#print(lnPosterior)
lnPosterior = lnPosterior #+ MadeUpConstant#- lnEvidence
#print(lnPosterior)


posterior = np.zeros(count, dtype = float64)
for i in range(count):
	posterior[i] = np.exp(lnPosterior[i])

print ("\n posterior is ")
print(posterior)

evidence = np.sum(posterior*dm)
posterior = posterior / evidence


####################  END OF MODEL 1 #################



#####  MODEL 2 : data = Gaussian Noise ###############
T = 8.0

lnPriorNoise = lnPrior # Same prior as previous model
lnEvidenceNoise = 0.0
lnPosteriorNoise = np.zeros(numMassVals)
lnPosteriorNoise = 0.0

# Calculating the lnLikelihoodNoise
Hsigma_2 = HNoise['noiseVar']

Hconstant = (np.log(1/np.sqrt(2*Hsigma_2*np.pi)))

# print(Hcomplex)
Hexpo = (-2.0/T) * np.vdot(Hcomplex,Hcomplex / (Hsigma_2))
# print("h expo")
# print (Hexpo)
HlnLikelihoodNoise =  Hexpo  + (2.0/T)*np.absolute(np.vdot(Hcomplex,Hcomplex/(Hsigma_2)))


Lsigma_2 = LNoise['noiseVar']

Lconstant = (np.log(1/np.sqrt(2*Lsigma_2*np.pi)))

Lexpo = (-2.0/T) * np.vdot(Lcomplex,Lcomplex/ (Lsigma_2))
LlnLikelihoodNoise =  Lexpo -  np.absolute(np.vdot(Lcomplex,Lcomplex/ (Lsigma_2)))


lnLikelihoodNoise = LlnLikelihoodNoise+HlnLikelihoodNoise
lnPosteriorNoise = lnPriorNoise + lnLikelihoodNoise

posteriorNoise = np.exp(lnPosteriorNoise)
lnEvidenceNoise = np.sum(lnPosteriorNoise+ np.log(dm))
evidenceNoise = np.sum(posteriorNoise * dm)

#posteriorNoise = posteriorNoise / evidenceNoise


####################  END OF MODEL 2 #################


####################  BAYES FACTOR #################

lnBayesFactor = lnEvidence - lnEvidenceNoise
print("lnBayesFactor: %f" %lnBayesFactor.real)
####################################################


####### CALCULAING THE PROB OF EACH MASS  ##########
logPostMass = np.zeros((2,len(mass_list)))
PostMass = np.zeros((2,len(mass_list)))
# P(a) = int_b [ P(a,b)*db]
# integrating out m2 to calculate prob(m1)

#print(lnPosterior)

for massIndex, m in enumerate(mass_list): # we need to check each mass value
	for i in range(count):		# at each mass value, we need to add up posteriors

		if (mass[MASS1][i] == m):
			logPostMass[MASS1][massIndex] += lnPosterior[i] + np.log(dm)
			PostMass[MASS1][massIndex]+= posterior[i]*dm
			Statment = "mass: " + str(m) + ", "+str(mass[MASS1][i])+" lnPosterior[i]: " + str(lnPosterior[i]) + " lnPostMass: " +str(logPostMass[MASS1][massIndex])
			#print(Statment)
		if (mass[MASS2][i] == m):
			logPostMass[MASS2][massIndex] += lnPosterior[i] + np.log(dm)
			PostMass[MASS2][massIndex]+= posterior[i]*dm



####################################################




## OUTPUTING THE DATA INTO A FILE
file = open("LogPosteriorDistribution.txt", "w")
file.write("log Posterior Distribution \t m1 \t m2 \n")
for i in range(count):
	posteriorData = str(posterior[i]) + '\t' + str(mass[MASS1][i]) + '\t' + str(mass[MASS2][i])
	StringToPrint = posteriorData + '\n'
	file.write(StringToPrint)
file.close()

file = open("massPosteriors.txt", "w")
file.write("mass1 \t log posteriorMass1 \t mass2 \t log posteriorMass2\n")
for i, m in enumerate(mass_list ):
	mass1Post= str(m) + '\t' + str(PostMass[MASS1][i])
	mass2Post= str(m) + '\t' + str(PostMass[MASS2][i])
	StringToPrint = mass1Post + '\t' + mass2Post + '\n'
	file.write(StringToPrint)
file.close()



#
# # # Plotting a histogram of the Posterior Distributuion
# fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
# ax.plot(mass_list, posterior)
# fig.savefig('/home/avi.vajpeyi/public_html/PlotOfMasses.png')   # save the figure to file
# plt.close(fig)    # close the figure
