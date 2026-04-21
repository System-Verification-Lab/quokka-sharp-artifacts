// Benchmark was created by MQT Bench on 2024-03-18
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 1.1.0
// Qiskit version: 1.0.2
// Used Gate Set: ['id', 'rz', 'rx(pi/2)', 'x', 'cx', 'measure', 'barrier']

OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
creg meas[2];
s q[1];
rx(pi/2) q[1];
s q[1];
t q[1];
cx q[1],q[0];
tdg q[0];
cx q[1],q[0];
t q[0];
s q[0];
rx(pi/2) q[0];
s q[0];
cx q[0],q[1];
cx q[1],q[0];
cx q[0],q[1];
