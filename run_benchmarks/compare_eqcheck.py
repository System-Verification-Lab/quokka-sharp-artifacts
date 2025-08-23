import shutil
import os, time
import quokka_sharp as qk
import re
import utils
from tqdm import tqdm
import subprocess
from mqt import qcec


benchmark_folder = os.path.join("algorithm")
benchmarks_list = utils.get_benchmark_list_from_file("compare_benchmarks_list.txt")

results_file_name = "compare_eqcheck.csv"
df_columns = ["modification", "qubits", "algo", "tool", "result", "time"]

modifications = ["opt", "gm"]
quokka_bases = ["comp", "pauli"]
quokka_checks = {
	"comp": "cyclic",
	"pauli": "linear"
}
quokka_threads = {
	"comp": 1,
	"pauli": 16
}

def get_results():
	return utils.get_results_from_file(results_file_name, df_columns)

def update_results(results_df):
	utils.save_results_to_file(results_file_name, results_df)

def sort_results():
	results_df = get_results()
	results_df.sort_values(by=["modification", "algo", "qubits", "tool"], inplace=True)
	update_results(results_df)

def check_results():
	results_df = get_results()
	assert all(results_df[results_df["modification"] == "opt"]["result"].isin(["TIMEOUT", "True", True])), "Opt results are not valid\n{}".format(results_df[results_df["modification"] == "opt"])
	assert all(results_df[results_df["modification"] != "opt"]["result"].isin(["TIMEOUT", "False", False])), "GM results are not valid\n{}".format(results_df[results_df["modification"] != "opt"])

def draw_figures():
	results_df = get_results()

	def compute_to_print(row):
		if row["result"] == "TIMEOUT":
			return "TIMEOUT"
		if (row["modification"] == "opt") and (row["result"] == "False"):
			return "wrong"
		if (row["modification"] == "gm") and (row["result"] == "True"):
			return "wrong"
		return f"{row['time']:.3f}"

	results_df["Run Time (sec)"] = results_df.apply(compute_to_print, axis=1)

	for mod in modifications:
		results_df[results_df["modification"] == mod].pivot_table(
			values=["Run Time (sec)"],
			index=["algo", "qubits"],
			columns=["tool"],
			aggfunc="sum"
			).to_latex(
			utils.get_results_file_path(results_file_name).replace(".csv", f"_{mod}.tex"),
			# column_format="lccc",
			multirow=True, multicolumn=True, na_rep=""
			)
	
def get_run_data(mod, algo, qubits, tool):
	return {
		"modification": mod,
		"algo": algo,
		"qubits": qubits,
		"tool": tool
	}

def run_QuokkaSharp(file_name, mod):
	results_df = get_results()
	origin_file = utils.get_file_path(file, "origin", benchmark_folder)
	mod_file = utils.get_file_path(file, mod, benchmark_folder)
	algo_name, qubits = utils.get_data_from_algo_file_name(file_name)
	if not qubits:
		qubits = get_qubits_from_file(origin_file)
	new = False
	for basis in quokka_bases:
		run_data = get_run_data(mod, algo_name, qubits, f"quokka-sharp-{basis}")
		if utils.data_exists(run_data, results_df):
			continue

		start_time = time.time()
		result = qk.functionalities.eq(origin_file, mod_file, basis, quokka_checks[basis], N=quokka_threads[basis])
		end_time = time.time()

		results_df = utils.add_result_to_df(run_data, result, end_time-start_time, results_df)
		utils.save_results_to_file(results_file_name, results_df)
		new = True
	return new

def run_QCEC(file_name, mod):
	results_df = get_results()
	origin_file = utils.get_file_path(file, "origin", benchmark_folder)
	mod_file = utils.get_file_path(file, mod, benchmark_folder)
	algo_name, qubits = utils.get_data_from_algo_file_name(file_name)
	if not qubits:
		qubits = get_qubits_from_file(origin_file)

	run_data = get_run_data(mod, algo_name, qubits, f"QCEC")
	if utils.data_exists(run_data, results_df):
		return False
	
	start_time = time.time()

	result = (str(qcec.verify(origin_file, mod_file).equivalence) == "EquivalenceCriterion.equivalent_up_to_global_phase")
	end_time = time.time()

	results_df = utils.add_result_to_df(run_data, result, end_time-start_time, results_df)
	utils.save_results_to_file(results_file_name, results_df)
	return True

def get_qubits_from_file(file_path):
	with open(file_path, "r") as f:
		for line in f:
			match = re.search(r"qreg q\[(\d+)\];", line)
			if match:
				return int(match.group(1))
	return None

def run_SliQSim(file_name, mod):
	results_df = get_results()
	origin_file = utils.get_file_path(file, "origin", benchmark_folder)
	mod_file = utils.get_file_path(file, mod, benchmark_folder)
	algo_name, qubits = utils.get_data_from_algo_file_name(file_name)
	if not qubits:
		qubits = get_qubits_from_file(origin_file)
	run_data = get_run_data(mod, algo_name, qubits, "SliQEC")
	if utils.data_exists(run_data, results_df):
		return False

	cmd = [
		"../../SliQEC/SliQEC",
		"--circuit1", origin_file,
		"--circuit2", mod_file,
	]

	try:
		start_time = time.time()
		output = subprocess.check_output(cmd, universal_newlines=True, timeout=utils.timeout)
		end_time = time.time()
	except subprocess.TimeoutExpired:
		end_time = time.time()
		result = "TIMEOUT"
		runtime = end_time - start_time
	else:
		result_matches = re.search(r"Is equivalent\? (Yes|No)", output)
		assert result_matches is not None, f"Could not find result in SliQSim output:\n{output}"
		assert len(result_matches.groups()) == 1, f"Expected one result match, got {len(result_matches.groups())} in output:\n{output}"
		runtime = end_time - start_time
		result = result_matches.group(1) == "Yes"

	results_df = utils.add_result_to_df(run_data, result, runtime, results_df)
	utils.save_results_to_file(results_file_name, results_df)
	return True


for file in tqdm(benchmarks_list, desc="Processing files", unit="file"):
	new = False
	for mod in modifications:
		new |= run_QuokkaSharp(file, mod)
		new |= run_SliQSim(file, mod)
		new |= run_QCEC(file, mod)
	if new:
		draw_figures()

sort_results()
check_results()
draw_figures()

