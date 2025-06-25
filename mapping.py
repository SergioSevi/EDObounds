import numpy as np
from scipy.special import erf


def lognormal(sigma,M,Mc):
    M = np.asarray(M)
    psi = 1/(np.sqrt(2*np.pi)*sigma*M)*np.exp(-np.log(M/Mc)**2/(2*sigma**2))
    return psi

def skew_lognormal(sigma,alpha,M,Mc):
    M = np.asarray(M)
    psi = 1/(np.sqrt(2*np.pi)*sigma*M)*np.exp(-np.log(M/Mc)**2/(2*sigma**2))*(1 + erf(alpha*np.log(M/Mc)/(np.sqrt(2)*sigma))),
    return psi


def mapping_fn(m,f,mass_distribution):
    if mass_distribution.startswith('lognormal'):
        #Take the input value for sigma. Default value = 1
        try:
            sigma=float(mass_distribution[len('lognormal('):-len(')')])
        except:
            sigma=1
        Mc_array = np.linspace(np.log10(m[0])-2*sigma, np.log10(m[-1])+2*sigma, 300)
        integrals = [1/np.trapz(lognormal(sigma, m, 10**Mc) / f, m) for Mc in Mc_array]
    elif mass_distribution.startswith('skew_lognormal'):
        #Take the input value for sigma. Default value = 1
        try:
            inner = mass_distribution[len('skew_lognormal('):-len(')')]
            sigma_str, alpha_str = inner.split(",")
            sigma = float(sigma_str.strip())
            alpha = float(alpha_str.strip())
        except:
            sigma=1
            alpha=0.1
        Mc_array = np.linspace(np.log10(m[0])-2*sigma, np.log10(m[-1])+2*sigma, 300)
        integrals = [1/np.trapz(skew_lognormal(sigma,alpha, m, 10**Mc)[0] / f, m) for Mc in Mc_array]
    else:  
        integrals = f
        Mc_array = np.log10(m)

    return 10**Mc_array, integrals