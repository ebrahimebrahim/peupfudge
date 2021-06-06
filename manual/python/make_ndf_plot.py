import numpy as np
import matplotlib.pyplot as plt


num_cache = {}

def num(N,n):
  "Number of ways of getting a sum of n when rolling NdF"
  if (N,n) in num_cache.keys():
    return num_cache[(N,n)]
  if n>N or n<-N:
    return 0
  if N==1:
    return 1
  ans = num(N-1,n-1) + num(N-1,n) + num(N-1,n+1)
  num_cache[(N,n)] = ans
  return ans

def p(N,n):
  "Probability of the outcome n when rolling NdF"
  return num(N,n) / (3**N)


ns = np.arange(-10,11,1)

get_ps = lambda N : [p(N,n) for n in ns]

plot_for_N = lambda N : plt.plot(ns, get_ps(N),label = str(N)+"dF")
plot_for_N(2)
plot_for_N(4)
plot_for_N(9)
plt.xticks(ns, labels=ns)
plt.legend()
plt.title("Probabilities when rolling NdF")
plt.savefig("ndf_plot.png")
