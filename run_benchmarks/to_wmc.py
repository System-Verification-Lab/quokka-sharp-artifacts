import quokka_sharp as qk
import sys
import os
import utils
import copy

benchmarks_list = utils.get_benchmark_list_from_file("benchlist-eq-phaseshift-ganak.txt")
print(benchmarks_list)
wmc_bench_route = "your/benchmark/route/here"


def basis(i, Z_or_X, cnf, cnf_file_root, qasmfile):
    """
    Create cnf file for each of the basis in the linear check
    Args:
        i         :  the index of the qubit
        Z_or_X    :  True if in Z basis otherwise in X basis
        cnf       :  the encoded CNF object of a circuit
        cnf_file_root : the path where the current cnf file will be stored.
    Returns:
        cnf_file  :  the path of the generated cnf file
    """
    cnf_temp = copy.deepcopy(cnf)
    cnf_temp.rightProjectZXi(Z_or_X, i)
    cnf_temp.leftProjectZXi(Z_or_X, i)

    cnf_file = os.path.join(cnf_file_root, f"{qasmfile}_eq_linear_"+ ("Z" if Z_or_X else "X") + str(i) + ".cnf")
    cnf_temp.write_to_file(cnf_file)
    print(f"Writing CNF to {cnf_file}...")

    return cnf_file

def get_simulation_cnf(basis):
    for qasmfile in benchmarks_list:
        print(f"Processing {qasmfile}...")
        filepath = utils.get_file_path(qasmfile, "origin", "algorithm")
        circuit1 = qk.encoding.QASMparser(filepath) 
        # Encode the circuit
        cnf = qk.encoding.QASM2CNF(circuit1, computational_basis = (basis == "comp"), weighted=True)
        cnf.leftProjectAllZero()
        cnf.add_measurement("allzero")
        cnf_file = os.path.join(wmc_bench_route, f"{qasmfile}_{basis}_simulation.cnf")
        print(f"Writing CNF to {cnf_file}...")
        cnf.write_to_file(cnf_file)

def get_eqcheck_cyclic_cnf(basis, mod):
    for qasmfile in benchmarks_list:
        print(f"Processing {qasmfile}...")
        origin_file = utils.get_file_path(qasmfile, "origin", "algorithm")
        mod_file = utils.get_file_path(qasmfile, mod, "algorithm")
        # Parse the circuit
        circuit1 = qk.encoding.QASMparser(origin_file)
		# Parse another circuit
        circuit2 = qk.encoding.QASMparser(mod_file)      
		# Get (circuit1)^dagger(circuit2)
        circuit2.dagger()
        circuit1.append(circuit2)
		# Get CNF for the merged circuit (for computational base instaed of cliffordt, use `computational_basis = True`)
        cnf = qk.encoding.QASM2CNF(circuit1, computational_basis = (basis == "comp"))
        cnf.add_identity_clauses(constrain_2n = False, constrain_no_Y = False)
        cnf_file = os.path.join(wmc_bench_route, f"{qasmfile}_eq_cyclic.cnf")
        print(f"Writing CNF to {cnf_file}...")
        cnf.write_to_file(cnf_file)

def get_eqcheck_linear_cnf(mod):
    for qasmfile in benchmarks_list:
        print(f"Processing {qasmfile}...")
        mod_file = utils.get_file_path(qasmfile, mod, "algorithm")
        filepath = utils.get_file_path(qasmfile, "origin", "algorithm")
        # Parse the circuit
        circuit1 = qk.encoding.QASMparser(filepath)
        # Parse another circuit
        circuit2 = qk.encoding.QASMparser(mod_file)      
        # Get (circuit1)^dagger(circuit2)
        circuit2.dagger()
        circuit1.append(circuit2)
        cnf = qk.encoding.QASM2CNF(circuit1, computational_basis = (basis == "comp"))
        # create a folder for qasmfiles :
        wmc_bench_qasmfile = os.path.join(wmc_bench_route, qasmfile)
        os.makedirs(os.path.join(wmc_bench_route, qasmfile), exist_ok=True)
        for i in range(cnf.n):
            basis(i, True, cnf, wmc_bench_qasmfile, qasmfile)
            basis(i, False, cnf, wmc_bench_qasmfile, qasmfile)
            
if __name__ == "__main__":
    benchmarks_list = utils.get_benchmark_list_from_file("benchlist-sim.txt")
    get_simulation_cnf("comp")
    get_simulation_cnf("pauli")

    benchmarks_list = utils.get_benchmark_list_from_file("benchlist-eq-phaseshift.txt")
    get_eqcheck_cyclic_cnf("comp","shift4")
    benchmarks_list = utils.get_benchmark_list_from_file("benchlist-eq-gatemissing.txt")
    get_eqcheck_cyclic_cnf("comp","gm")
    
    benchmarks_list = utils.get_benchmark_list_from_file("benchlist-eq-phaseshift.txt")
    get_eqcheck_linear_cnf("shift4")
    benchmarks_list = utils.get_benchmark_list_from_file("benchlist-eq-gatemissing.txt")
    get_eqcheck_linear_cnf("gm")