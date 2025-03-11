import pytest
import subprocess
from pathlib import Path
import os
import allure
import shutil

allure_results_dir = 'allure-results'
if os.path.exists(allure_results_dir):
    shutil.rmtree(allure_results_dir)

allure_report_dir = 'allure-report'
if os.path.exists(allure_report_dir):
    shutil.rmtree(allure_report_dir)

logs_dir = 'logs'
if os.path.exists(logs_dir):
    shutil.rmtree(logs_dir)

feature_files_End_End = [
    ('features/tc_01_solar_sunnova.feature', 1),
    ('features/tc_02_roof_sunnova.feature', 2),
    ('features/tc_03_roof_cash.feature', 3),
    ('features/tc_04_battery_cash.feature', 4),
    ('features/tc_05_rrr_sunnova.feature', 5)
]

all_feature_files = (feature_files_End_End)

# Sort the feature files based on the order attribute
all_feature_files.sort(key=lambda x: x[1])

# Create a list of feature files in the sorted order
all_feature_files = [x[0] for x in all_feature_files]


@pytest.mark.parametrize("feature_file", all_feature_files)
def test_run_feature(feature_file):

    command = f"behave -f allure_behave.formatter:AllureFormatter -o allure-results {feature_file}"
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Check if the Behave test run was successful (return code 0)
    assert result.returncode == 0, f"Feature file {feature_file} failed:\n{result.stdout}\n{result.stderr}"


if __name__ == "__main__":
    # Use pytest-xdist to run tests in parallel (adjust the -n parameter as needed)
    pytest.main(["-v", "runner.py", "-n", "5"])

    # Generate Allure report
    allure_results_dir = 'allure-results'

    subprocess.call(
        "allure generate --clean --single-file -o allure-report allure-results", shell=True)
