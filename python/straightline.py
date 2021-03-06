import copy
import numpy as np
import numpy.random as rng
from utils import randh
from numba import jit

# How many parameters are there?
num_params = 3

# Some data
data = np.loadtxt("road.txt")
N = data.shape[0] # Number of data points

# Plot the data
import matplotlib.pyplot as plt
plt.plot(data[:,0], data[:,1], "o")
plt.xlabel("Age of person (years)")
plt.ylabel("Maximum vision distance (feet)")
plt.show()

# Some idea of how big the Metropolis proposals should be
jump_sizes = np.array([1000.0, 1000.0, 20.0])

@jit
def from_prior():
    """
    A function to generate parameter values from the prior.
    Returns a numpy array of parameter values.
    """

    m = 1000.0*rng.randn()
    b = 1000.0*rng.randn()
    log_sigma = -10.0 + 20.0*rng.rand()

    return np.array([m, b, log_sigma])



@jit
def log_prior(params):
    """
    Evaluate the (log of the) prior distribution
    """
    # Rename the parameters
    m, b, log_sigma = params

    logp = 0.0

    # Normal prior for m and b
    # Metropolis only needs the ratio, so I've left out the 2pi bits
    logp += -0.5*(m/1000.0)**2
    logp += -0.5*(b/1000.0)**2

    if log_sigma < -10.0 or log_sigma > 10.0:
        return -np.Inf

    return logp

@jit
def log_likelihood(params):
    """
    Evaluate the (log of the) likelihood function
    """
    # Rename the parameters
    m, b, log_sigma = params

    # Get sigma
    sigma = np.exp(log_sigma)

    # First calculate the straight line
    line = m*data[:,0] + b

    # Normal/gaussian distribution
    return -0.5*N*np.log(2*np.pi) - N*log_sigma \
                        -0.5*np.sum((data[:,1] - line)**2/sigma**2)

@jit
def proposal(params):
    """
    Generate new values for the parameters, for the Metropolis algorithm.
    """
    # Copy the parameters
    new = copy.deepcopy(params)

    # Which one should we change?
    which = rng.randint(num_params)
    new[which] += jump_sizes[which]*randh()
    return new

