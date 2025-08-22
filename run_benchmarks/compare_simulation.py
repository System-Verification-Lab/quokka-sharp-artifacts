import cmd
import shutil
import os, time
import pandas as pd
import quokka_sharp as qk
import re
import utils
from tqdm import tqdm
import matplotlib.pyplot as plt
import subprocess

benchmark_folder = os.path.join("algorithm")
benchmarks_list = utils.get_benchmark_list_from_file("compare_simulation_benchmarks_list.txt")

results_file_name = "compare_simulations.csv"
df_columns = ["qubits", "algo", "tool", "result", "time"]

quokka_bases = ["comp", "pauli"]
quokka_measurement = "allzero"

sliqsim_measurement = lambda qubits: f"amp {'0'*qubits};"

def get_results():
	return utils.get_results_from_file(results_file_name, df_columns)

def update_results(results_df):
	utils.save_results_to_file(results_file_name, results_df)

def sort_results():
	results_df = get_results()
	results_df.sort_values(by=["algo", "qubits", "tool"], inplace=True)
	update_results(results_df)

def check_results():
	results_df = get_results()
	time_over_timeout_allowed = 0 #seconds
	result_accuracy = 1e-6
	for exp, results in results_df.groupby(["qubits", "algo"]):
		assert len(results) == 3, f"Expected 3 results for {exp}, but found {len(results)}\n{results}"

		for timeout_result in results[results["result"] == "TIMEOUT"].itertuples():
			assert abs(timeout_result.time - utils.timeout) <= time_over_timeout_allowed, f"Timeout result for {exp} is not close to timeout: {timeout_result.time}"

		non_timeout_results = results[results["result"] != "TIMEOUT"]
		min_result = non_timeout_results["result"].min()
		max_result = non_timeout_results["result"].max()
		assert max_result - min_result <= result_accuracy, f"Non-timeout results for {exp} are not similar: {min_result} vs {max_result}\n{non_timeout_results}"

def draw_figures():
	results_df = get_results()

	def compute_to_print(row):
		if row["result"] == "TIMEOUT":
			return "TIMEOUT"
		return f"{row['time']:.3f}"

	results_df["Run Time (sec)"] = results_df.apply(compute_to_print, axis=1)

	results_df.pivot_table(
		values=["Run Time (sec)"], 
		index=["algo", "qubits"],
		columns=["tool"],
		aggfunc="sum"
		).to_latex(
		utils.get_results_file_path(results_file_name).replace(".csv", f".tex"),
		# column_format="lccc",
		multirow=True, multicolumn=True, na_rep=""
		)
	
def get_run_data(algo, qubits, tool):
	return {
		"algo": algo,
		"qubits": qubits,
		"tool": tool
	}

def run_QuokkaSharp(file_name):
	results_df = get_results()
	file_path = utils.get_file_path(file, "origin", benchmark_folder)
	algo_name, qubits = utils.get_data_from_algo_file_name(file_name)
	if not qubits:
		qubits = get_qubits_from_file(file_path)
	new = False
	for basis in quokka_bases:
		run_data = get_run_data(algo_name, qubits, f"quokka-sharp-{basis}")
		if utils.data_exists(run_data, results_df):
			continue

		start_time = time.time()
		result = qk.functionalities.sim(file_path, basis, quokka_measurement)
		end_time = time.time()

		results_df = utils.add_result_to_df(run_data, result, end_time-start_time, results_df)
		utils.save_results_to_file(results_file_name, results_df)
		new = True
	return new

def get_SliQSim_obs_file_path(qubits):
	obs_file_path = os.path.join(".", "temp", f"SliQSim_{qubits}_obs.obs")
	if not os.path.exists(obs_file_path):
		os.makedirs("temp", exist_ok=True)
		with open(obs_file_path, "w") as f:
			f.write(f"{sliqsim_measurement(qubits)};\n")
	return obs_file_path

def remove_temp_folder():
	temp_folder = os.path.join(".", "temp")
	if os.path.exists(temp_folder):
		shutil.rmtree(temp_folder)

def get_qubits_from_file(file_path):
	with open(file_path, "r") as f:
		for line in f:
			match = re.search(r"qreg q\[(\d+)\];", line)
			if match:
				return int(match.group(1))
	return None

def run_SliQSim(file_name):
	results_df = get_results()
	file_path = utils.get_file_path(file, "origin", benchmark_folder)
	algo_name, qubits = utils.get_data_from_algo_file_name(file_name)
	if not qubits:
		qubits = get_qubits_from_file(file_path)
	run_data = get_run_data(algo_name, qubits, "SliQSim")
	if utils.data_exists(run_data, results_df):
		return False
	obs_file_path = get_SliQSim_obs_file_path(qubits)

	cmd = [
		"../../SliQSim/SliQSim",
		"--sim_qasm", file_path,
		"--obs_file", obs_file_path,
		"--type", "2"
	]

	try:
		start_time = time.time()
		output = subprocess.check_output(cmd, universal_newlines=True, timeout=utils.timeout)
		end_time = time.time()
	except subprocess.TimeoutExpired as e:
		result = "TIMEOUT"
		runtime = end_time - start_time
	else:
		result_matches = re.search(r"\s*([-\d.e]+)\s", output)
		assert result_matches is not None, f"Could not find result in SliQSim output:\n{output}"
		assert len(result_matches.groups()) == 1, f"Expected one result match, got {len(result_matches.groups())} in output:\n{output}"
		runtime = end_time - start_time
		result = float(result_matches.group(1))**2

	results_df = utils.add_result_to_df(run_data, result, runtime, results_df)
	utils.save_results_to_file(results_file_name, results_df)
	return True


for file in tqdm(benchmarks_list, desc="Processing files", unit="file"):
	new = run_QuokkaSharp(file)
	new |= run_SliQSim(file)
	if new:
		draw_figures()

remove_temp_folder()
sort_results()
check_results()
draw_figures()

