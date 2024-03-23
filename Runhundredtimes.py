import subprocess
import os
import sys

BASE_PATH = "E:/project/PLL/ChinaTelecom"
LOG_PATH = os.path.join(BASE_PATH, "FinalLog.txt")

def run_script(script_name, output_file):
    full_script_path = os.path.join(BASE_PATH, script_name)
    os.environ["MPLBACKEND"] = "Agg"
    with open(output_file, 'w') as f:
        subprocess.run(['python', full_script_path], stdout=f, stderr=subprocess.DEVNULL)

def extract_values_from_file(output_file):
    max_utilization = None
    avg_hop_count = None
    with open(output_file, 'r') as f:
        lines = f.readlines()[-10:]  # Consider the last 10 lines
        for line in lines:
            if "Maximum utilization:" in line:
                max_utilization = float(line.split(":")[1].strip().rstrip('%')) / 100
            elif "Average hop count:" in line:
                avg_hop_count = float(line.split(":")[1].strip())
    return max_utilization, avg_hop_count

def dual_output(message):
    """Prints to both cmd and the log file."""
    print(message)
    with open(LOG_PATH, "a") as log_file:
        log_file.write(message + "\n")

def clear_log_file():
    """Clears the content of the log file."""
    with open(LOG_PATH, "w") as log_file:
        log_file.write("")

def main():
    clear_log_file()

    scripts = [
        #"V30dijkstra_ChinaTelecom_ECMP_hop.py",
        #"V30dijkstra_ChinaTelecom_hop.py",
        #"V30dijkstra_ChinaTelecom_kshortest_hop.py",
        "V30pll_heuristic_ChinaTelecom_hop.py",
        "V30pll_heuristic_ChinaTelecom_ECMP1_hop.py",
        "V30pll_heuristic_ChinaTelecom_ECMP2_hop.py",
        "V30pll_heuristic2_ChinaTelecom_hop.py",
        "V31pll_heuristic2_ChinaTelecom_ECMP1_hop.py",
        "V31pll_heuristic2_ChinaTelecom_ECMP2_hop.py",
        "V30pll_heuristic3_ChinaTelecom_hop.py",
        "V31pll_heuristic3_ChinaTelecom_ECMP1_hop.py",
        "V31pll_heuristic3_ChinaTelecom_ECMP2_hop.py",
        #"V30pll_heuristic_ChinaTelecom_ECMP3_hop.py",

    ]
    

    total_runs = 10
    temp_output_file = "temp_output.txt"

    for script in scripts:
        total_max_utilization = 0
        total_avg_hop_count = 0
        dual_output(f"Running {script}...")
        for i in range(total_runs):
            run_script(script, temp_output_file)
            max_utilization, avg_hop_count = extract_values_from_file(temp_output_file)
            if max_utilization is not None:
                total_max_utilization += max_utilization
            if avg_hop_count is not None:
                total_avg_hop_count += avg_hop_count
            # Print progress
            dual_output(f"Progress: {i+1}/{total_runs} runs completed")

        avg_max_utilization = total_max_utilization / total_runs
        avg_avg_hop_count = total_avg_hop_count / total_runs

        dual_output(f"\nScript: {script}")
        dual_output(f"Average Maximum Utilization: {avg_max_utilization:.2%}")
        dual_output(f"Average Hop Count: {avg_avg_hop_count:.2f}")
        dual_output("-------------------------------")

    # Clean up the temporary file
    os.remove(temp_output_file)

if __name__ == "__main__":
    main()
