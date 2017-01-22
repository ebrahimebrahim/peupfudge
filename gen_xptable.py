#!/usr/bin/env python

# This script generates the xp table to be included directly in the manual tex file

# b = skill level base
# s = xp scale factor
# d = discount factor
b = 1.7
s = 10.2
d = 0.125

# a = attribute bonus
# c = current skill level
xp_cost = lambda a,c : int(round(s*pow(b,c)*(1-d*(a-3))))

#list of current skill levels to put as rows of table:
clist = range(1,9)

#list of attribute bonuses to put as columns table:
alist = map(lambda x:x/(2.0),range(1,19))


colcolor = lambda color : ">{\\columncolor[HTML]{"+color+"}[\\tabcolsep][1.1\\tabcolsep]}"
blue = colcolor("67C4D8")
red  = colcolor("F67D75")
purp = colcolor("AFA1A7")


f = open("xptable.tex", "w")
f.write("\\setlength{\\minrowclearance}{6pt}\n")
f.write("\\begin{tabular}{cr"+(len(alist)*'l')+"}\n")

f.write("\\multicolumn{2}{"+purp+"c}{} & \\multicolumn{"+str(len(alist))+"}{"+blue+"c}{\\textbf{Attribute Bonus}} \\\\\n")
f.write("\\noalign{\\vspace{-1pt}}\n")

f.write("\\multicolumn{2}{"+purp+"c}{\multirow{-2}{*}{\\textbf{XP}}} &")
for a in alist:
  f.write(" \\multicolumn{1}{"+blue+"r}{\\textbf{"+str(a)+"}} ")
  if a!=alist[-1]:
    f.write(" & ")
f.write("\\\\ \\cline{3-"+str(2+len(alist))+"}\n")

for c in clist:
  if c!=clist[-1]:
    f.write(" \\multicolumn{1}{"+red+"r}{} & ")
  else:
    f.write("\\multicolumn{1}{"+red+"l}{")
    f.write("\\multirow{-"+str(len(clist))+"}{*}{")
    f.write("\\rotatebox[origin=c]{90}{\\textbf{Current Skill Level}}")
    f.write("}} & ")
  f.write(" \\multicolumn{1}{"+red+"r|}{\\textbf{"+str(c)+"}} & ")
  for a in alist:
    f.write(" \\multicolumn{1}{r|}{"+str(xp_cost(a,c))+"} ")
    if a!=alist[-1]:
      f.write(" & ")
  f.write("\\\\ \\cline{3-"+str(2+len(alist))+"}\n")
  f.write("\\noalign{\\vspace{-1pt}}\n")

f.write("\\end{tabular}\n")
f.close()
