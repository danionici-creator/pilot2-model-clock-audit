"""Conceptual countermodels for Perspective claims; not a simulation of deployed hardware."""
import numpy as np
x=np.array([-1.,-1.,1.,1.]); z=np.array([-1.,1.,-1.,1.]); candidate=x+.1*z
print('D01 reconstruction R2:',1-np.sum((candidate-x)**2)/np.sum((candidate-candidate.mean())**2))
print('Residual predicts outcome perfectly:',np.allclose((candidate-x)/.1,z))
# This countermodel violates atomicity of N with state, while preserving atomicity of state+seal.
# It shows why the scope of the paper's assumed atomicity must explicitly include N.
live=4; saved=4
live+=1
print('D02 crash after hardware increment but before state+seal commit:',{'live_N':live,'sealed_N':saved,'classifier':'restoration','event':'crash'})
print('D03 information: if raw=(time,N,sealed time,sealed N), a local monitor can transmit the full same tuple; a binary flag is lossy by design.')
