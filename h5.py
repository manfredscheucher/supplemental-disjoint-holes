#!/usr/bin/python
"""
	This program can be used to generate a CNF
	to verify that every set of 10 points contains a 5-holes.
	(c) 2018 Manfred Scheucher <scheucher@math.tu-berlin.de>
"""


from itertools import combinations, permutations
from sys import *

n = int(argv[1]) # run program with command line parameter 10
N = range(n)


all_variables = []
all_variables += [('trip',I) for I in permutations(N,3)]
all_variables += [('extr_ab',I) for I in combinations(N,4)]
all_variables += [('extr_cd',I) for I in combinations(N,4)]
all_variables += [('convpos',I) for I in combinations(N,4)]
all_variables += [('b_inner',I) for I in combinations(N,4)]
all_variables += [('c_inner',I) for I in combinations(N,4)]
all_variables += [('emptytr',I) for I in combinations(N,3)]

all_variables_index = {}

_num_vars = 0
for v in all_variables:
	all_variables_index[v] = _num_vars
	_num_vars += 1

def var(L):	return 1+all_variables_index[L]
def var_trip(*L): return var(('trip',L))
def var_extr_ab(*L): return var(('extr_ab',L))
def var_extr_cd(*L): return var(('extr_cd',L))
def var_convpos(*L): return var(('convpos',L))
def var_b_inner(*L): return var(('b_inner',L))
def var_c_inner(*L): return var(('c_inner',L))
def var_emptytr(*L): return var(('emptytr',L)) 


constraints = []



print "(1) Alternating axioms",len(constraints)
for a,b,c in combinations(N,3):
	for sgn in [+1,-1]:
		constraints.append([sgn*var_trip(a,b,c),-sgn*var_trip(b,c,a)])
		constraints.append([sgn*var_trip(a,b,c),-sgn*var_trip(c,a,b)])
		constraints.append([sgn*var_trip(a,b,c),sgn*var_trip(c,b,a)])
		constraints.append([sgn*var_trip(a,b,c),sgn*var_trip(b,a,c)])
		constraints.append([sgn*var_trip(a,b,c),sgn*var_trip(a,c,b)])



print "(2) Signotope Axioms",len(constraints)
# forbid invalid configuartions in the signature
for I4 in combinations(N,4):
	I4_triples = list(combinations(I4,3))
	for t1,t2,t3 in combinations(I4_triples,3): 
		# for any three lexicographical ordered triples t1 < t2 < t3
		# the signature must not be "+-+" or "-+-"
		for sgn in [+1,-1]:
			constraints.append([sgn*var_trip(*t1),-sgn*var_trip(*t2),sgn*var_trip(*t3)])



print "(3) Sorted around first point",len(constraints)
# without loss of generality, points sorted around 0
for b,c in combinations(range(1,n),2):
	constraints.append([var_trip(0,b,c)])



print "(4) Bounding segments",len(constraints)
# assert extremal points
for I in combinations(N,4):
	[a,b,c,d] = I
	# if ab extremal, then abc = abd
	# if ab not extremal, then abc != abd 
	constraints.append([-var_extr_ab(*I), var_trip(a,b,c),-var_trip(a,b,d)])
	constraints.append([-var_extr_ab(*I),-var_trip(a,b,c), var_trip(a,b,d)])
	constraints.append([ var_extr_ab(*I), var_trip(a,b,c), var_trip(a,b,d)])
	constraints.append([ var_extr_ab(*I),-var_trip(a,b,c),-var_trip(a,b,d)])

	constraints.append([-var_extr_cd(*I), var_trip(a,c,d),-var_trip(b,c,d)])
	constraints.append([-var_extr_cd(*I),-var_trip(a,c,d), var_trip(b,c,d)])
	constraints.append([ var_extr_cd(*I), var_trip(a,c,d), var_trip(b,c,d)])
	constraints.append([ var_extr_cd(*I),-var_trip(a,c,d),-var_trip(b,c,d)])



print "(5) 4-Gons and containments",len(constraints)
# assert crossings and inner points
for I in combinations(N,4):
	[a,b,c,d] = I
	# if convex position, then ab and cd all extremal 
	constraints.append([-var_convpos(*I),var_extr_ab(*I)])
	constraints.append([-var_convpos(*I),var_extr_cd(*I)])

	# if not convex position, ab or cd is not extremal
	constraints.append([var_convpos(*I),-var_extr_ab(*I),-var_extr_cd(*I)])

	# inner-outer relations of each 4-tuple:
	# either convex, or b is inner, or c is inner (exclusive or!)
	constraints.append([var_b_inner(*I),var_c_inner(*I),var_convpos(*I)])
	constraints.append([-var_b_inner(*I),-var_c_inner(*I)])
	constraints.append([-var_b_inner(*I),-var_convpos(*I)])
	constraints.append([-var_c_inner(*I),-var_convpos(*I)])

	constraints.append([ var_b_inner(*I), var_extr_ab(*I)])
	constraints.append([-var_b_inner(*I),-var_extr_ab(*I)])
	constraints.append([ var_c_inner(*I), var_extr_cd(*I)])
	constraints.append([-var_c_inner(*I),-var_extr_cd(*I)])



print "(6) 3-Holes",len(constraints)
# assert empty triangles
for a,b,c in combinations(N,3):
	# if not empty, then there must be an inner point i
	constraints.append(
		 [var_emptytr(a,b,c)]
		+[var_b_inner(a,i,b,c) for i in range(a+1,b)]
		+[var_c_inner(a,b,i,c) for i in range(b+1,c)]
		)

	# if empty, then there is no inner point i
	for i in range(a+1,b):
		constraints.append([-var_emptytr(a,b,c),-var_b_inner(a,i,b,c)])
	for i in range(b+1,c):
		constraints.append([-var_emptytr(a,b,c),-var_c_inner(a,b,i,c)])



print "(7) 5-Holes",len(constraints)
for I in combinations(N,5):
	# if I is not a 5-hole,
	# then there must be 4 points not in convex position
	# or some non-empty triangle (i.e., there are inner points) 
	constraints.append(
		 [-var_convpos(*J) for J in combinations(I,4)]
		+[-var_emptytr(*J) for J in combinations(I,3)]
		)


print "Total number of constraints:",len(constraints)


fp = "instance_h5_"+str(n)+".in"
f = open(fp,"w")
f.write("p cnf "+str(_num_vars)+" "+str(len(constraints))+"\n")
for c in constraints:
	f.write(" ".join(str(v) for v in c)+" 0\n")
f.close()

print "Created CNF-file:",fp
