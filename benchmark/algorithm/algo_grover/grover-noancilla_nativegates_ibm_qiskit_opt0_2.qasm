// Used Gate Set: ['id', 'rz', 'rx(pi/2)', 'x', 'cx', 'measure', 'barrier']
OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
qreg flag[1];
s q[0];
rx(pi/2) q[0];
s q[0];
x flag[0];
