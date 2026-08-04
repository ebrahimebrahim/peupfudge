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


# Make plot
ns = np.arange(-9,10,1)
get_ps = lambda N : [p(N,n) for n in ns]
plot_for_N = lambda N : plt.plot(ns, get_ps(N),label = str(N)+"dF")
plot_for_N(2)
plot_for_N(4)
plot_for_N(6)
plot_for_N(9)
plt.xticks(ns, labels=ns)
plt.legend()
plt.title("Probabilities when rolling NdF")
plt.savefig("ndf_plot.pdf")


# Make table
cols = range(-5,6)
rows = range(1,10)
col_colored = 0
row_colored = 4
color_str = '\\cellcolor{blue!20}'
with open("ndf_table.tex",'w') as f:
  f.write('\\begin{tabular}{')
  f.write('|' + '|'.join(['c']*(len(cols)+1)) + '|')
  f.write('}\n\hline\n')
  f.write(' '.join(f'& $\geq {c}$' for c in cols))
  f.write('\\\\ \hline\n')
  for r in rows:
    f.write(f'${r}$dF ')
    for c in cols:
      f.write('& $')
      cumulative_probability = sum(p(r,n) for n in range(c,r+1))
      cumulative_probability_formatted = "{:.2f}".format(cumulative_probability)
      f.write(cumulative_probability_formatted)
      f.write('$ ')
      if r==row_colored or c==col_colored:
        f.write(color_str)
    f.write('\\\\ \hline\n')
  f.write('\\end{tabular}\n')

