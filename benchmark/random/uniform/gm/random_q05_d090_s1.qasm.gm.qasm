OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
cx q[1], q[3];
cx q[3], q[1];
cx q[1], q[3];
cx q[0], q[3];
cx q[3], q[0];
cx q[0], q[3];
h q[3];
h q[1];
h q[0];
rz(0.5*pi) q[4];
h q[4];
h q[3];
cz q[0], q[4];
cz q[0], q[3];
rz(1.5*pi) q[0];
h q[0];
h q[1];
cz q[3], q[4];
cz q[1], q[2];
cz q[0], q[4];
rz(1.25*pi) q[4];
h q[4];
h q[2];
cz q[2], q[3];
rz(1.75*pi) q[4];
rz(0.25*pi) q[3];
h q[4];
h q[3];
cz q[2], q[4];
cz q[2], q[3];
cz q[0], q[2];
rz(1.25*pi) q[2];
h q[2];
rz(0.25*pi) q[2];
h q[2];
cz q[2], q[4];
rz(1.25*pi) q[4];
h q[4];
cx q[4], q[0];
h q[2];
rz(0.75*pi) q[2];
h q[2];
cx q[2], q[4];
cz q[1], q[4];
cz q[0], q[4];
rz(0.75*pi) q[4];
h q[4];
cz q[2], q[4];
rz(1.75*pi) q[4];
h q[4];
cz q[2], q[4];
cz q[1], q[2];
cz q[0], q[1];
rz(0.25*pi) q[0];
rz(1.25*pi) q[2];
h q[0];
h q[2];
h q[3];
cz q[2], q[3];
cz q[0], q[2];
rz(0.75*pi) q[3];
rz(0.25*pi) q[0];
h q[3];
h q[0];
cz q[2], q[3];
cz q[1], q[2];
cz q[0], q[2];
rz(1.25*pi) q[2];
h q[2];
cz q[3], q[4];
cz q[2], q[3];
cz q[1], q[3];
rz(0.25*pi) q[3];
h q[3];
rz(1.75*pi) q[3];
h q[3];
cx q[3], q[2];
cx q[3], q[4];
rz(0.25*pi) q[1];
h q[1];
cx q[1], q[4];
rz(0.75*pi) q[1];
h q[1];
cx q[1], q[2];
cx q[2], q[0];
h q[1];
rz(0.75*pi) q[1];
h q[1];
cx q[1], q[0];
cz q[1], q[4];
cz q[1], q[3];
cz q[1], q[2];
rz(0.75*pi) q[1];
h q[1];
cx q[1], q[0];
cz q[0], q[3];
rz(0.75*pi) q[3];
h q[3];
cx q[3], q[2];
cz q[0], q[3];
rz(0.25*pi) q[0];
h q[0];
cx q[0], q[1];
h q[3];
cz q[1], q[3];
rz(0.25*pi) q[3];
h q[3];
cx q[3], q[2];
cz q[1], q[4];
cz q[0], q[1];
rz(1.25*pi) q[1];
h q[1];
h q[3];
cz q[3], q[4];
cz q[1], q[3];
cz q[0], q[3];
rz(1.25*pi) q[3];
h q[3];
cx q[3], q[2];
h q[0];
cz q[0], q[2];
rz(0.25*pi) q[0];
h q[0];
cx q[0], q[1];
rz(1.25*pi) q[2];
h q[2];
h q[0];
cz q[0], q[3];
cz q[0], q[2];
rz(1.75*pi) q[0];
h q[0];
cz q[1], q[4];
cz q[0], q[1];
rz(1.25*pi) q[1];
h q[1];
rz(0.75*pi) q[1];
h q[1];
cx q[1], q[2];
cx q[2], q[0];
cz q[2], q[3];
cz q[1], q[3];
rz(1.25*pi) q[3];
h q[3];
cx q[3], q[0];
cz q[3], q[4];
rz(0.75*pi) q[3];
h q[3];
cx q[3], q[0];
cz q[3], q[4];
rz(1.75*pi) q[4];
h q[4];
cx q[4], q[0];
h q[3];
cz q[0], q[3];
cz q[0], q[2];
rz(1.75*pi) q[3];
rz(1.75*pi) q[1];
rz(0.25*pi) q[0];
h q[3];
h q[1];
h q[0];
cz q[0], q[3];
h q[3];
cz q[1], q[4];
cz q[1], q[2];
cz q[0], q[4];
rz(1.5*pi) q[4];
rz(0.25*pi) q[3];
rz(1.75*pi) q[2];
h q[2];
rz(1.0*pi) q[1];
h q[1];
rz(0.5*pi) q[0];
