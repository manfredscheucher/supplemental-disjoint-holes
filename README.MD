# On Disjoint Holes in Point Sets

This repository provides programs to verify the computer-assisted results from my paper "On Disjoint Holes in Point Sets".

## Abstract of the paper

Given a set of points $S \subseteq \mathbb{R}^2$, a subset $X \subseteq S$, $|X|=k$, is called _$k$-gon_ if all points of $X$ lie on the boundary of the convex hull $\mathrm{conv} (X)$, and _$k$-hole_ if, in addition, no point of $S \setminus X$ lies in $\mathrm{conv} (X)$. We use computer assistance to show that every set of 17 points in general position admits two disjoint 5-holes, that is, holes with disjoint respective convex hulls. This answers a question of [Hosono and Urabe (2001)](http://doi.org/10.1016/S0925-7721(01)00023-2). We also provide new bounds for three and more pairwise disjoint holes. Moreover, our program can be used to verify that every set of 17 points contains a 6-gon within significantly smaller computation time than the original program by [Szekeres and Peters (2006)](http://doi.org/10.1017/S144618110000300X).

## Short description of the programs

We provide a python program "h55.py" to formulate a SAT instance to verify that every set of 17 points contains two disjoint 5-holes. To execute the program, run

```python h55.py 17```

The SAT instance is written to a cnf-file, which then can be solved using a SAT solver such as [glucose](http://www.labri.fr/perso/lsimon/glucose/) or [picosat](http://fmv.jku.at/picosat/).  
(The programs for interior-disjoint 5-holes and 6-gons are analogously.)

## Downloads

*   The source code of the program "h55.py" to verify that every set of 17 points contains two disjoint 5-holes, i.e., $h(5,5)=17$. \[[download](h55.py)\]
*   The source code of the program "h55_interior.py" to verify that every set of 15 points contains two interior-disjoint 5-holes. \[[download](h55_interior.py)\]
*   The source code of the program "g6.py" to verify that every set of 17 points contains a 6-gon, i.e., $g(6)=17$. \[[download](g6.py)\]