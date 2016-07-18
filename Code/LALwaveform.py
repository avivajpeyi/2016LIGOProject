import lal
import lalsimulation

def hOfF(m1, m2):

	m1 *= lal.lal.MSUN_SI
	m2 *= lal.lal.MSUN_SI

	fmin = 10
	fmax = 512
	deltaF = 1./8
	dist = 100

	H = lalsimulation.SimIMRPhenomP(0, 0, 0, 0, m1, m2, 1000*1e6*lal.lal.PC_SI, 0, 0, deltaF, fmin, fmax, 20, 1)

	return H[0].data.data + H[1].data.data
