Python BioSystem Framework
==========================

The aim of the project was to create simple, easy accessible and editable framework for synthetic biology research,  based on freely available libraries and programming languages. 

The tool was inspired by MIT university course „20.305x Principles of Synthetic Biology“ provided tool „Part-compositor framework“ which is based on „MatLab“ framework. 

Python programming language and its non-standard libraries: Sympy, Numpy, and Scipy were used to implement the goal, due to the similarity of the MatLab functionality required.
The created tool can simulate concentrations of substances in time using chemical reaction differential equitations with the specified initial concentration conditions of substances.

The implementation is available on the public github webpage: 
https://github.com/eglepl/pybiosystem_framwork


----------


Requirements
-------------

- Linux (might work with other OS)
- Python 2.7
- Python libraries:
	- SymPy v1.0
	- NumPy v1.11.1
	- SciPy v0.18.1
	- Matplotlib v1.5.3 (optional for data plotting)

----------

Documentation
-------------

See the docs/html/index.php file for documentation reference and
examples.

The PDF version can be found in docs/latex/refman.pdf 

----------

Usage
-----

```
from Biosystem import *
from Part import *
from Rate import *
from Pulse import *
import matplotlib.pyplot as plt # optional for plotting

sys = BioSystem()
sys.addConstant('k', 0.05)
dAdt = sys.addCompositor('A', 10)
dBdt = sys.addCompositor('B', 0)
dEdt = sys.addCompositor('E', 1)
reaction  = Part(
'A + E -k> B + E',
[dAdt, dBdt, dEdt],
[Rate('-k * A * E'), Rate('k * A * E'), Rate('0')])
sys.addPart(reaction)
T = None
Y = None
(T, Y) = sys.run([0, 25])

# Plot the simulation data (optional if You want to plot data)
plt.figure()
plt.plot(T, Y[:, sys.compositorIndex('A')], label="A")
plt.plot(T, Y[:, sys.compositorIndex('B')], label="B")
plt.plot(T, Y[:, sys.compositorIndex('E')], label="E")
plt.legend()
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.show()
```
