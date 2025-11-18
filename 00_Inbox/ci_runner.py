import os, sys, re, glob, yaml
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import pandas as pd
import subprocess
import signal
import time

# ---- Define Test Result Root Path ----
test_result_path = os.path.join(os.path.dirname(__file__), 'test_result')
if not os.path.exists(test_result_path):
    os.makedirs(test_result_path)

# ---- Define Global Variables ----
junit_result_xml = None
xml_filename = None
xlsx_filename = None
result_dir = None
test_datetime = None
result_basename = None
test_script_array = None
test_suite_name = None
test_count = [0, 0, 0, 0]  # Total, Pass, Fail, Skip
testsummary = {}

def signal_handler(signum, frame):
    print('User Exit!')
    exit()

def get_testsuite_extended():
    global test_script_array, test_suite_name
    
    for test in test_script_array:
        if isinstance(test, dict) and test.get('name'):
            test_name = test.get('name')
            param_array = test.get('param')
            if param_array == None or param_array == []:
                yield test_name, None, 0
            else:
                for idx, param in enumerate(param_array):
                    yield test_name, param, idx
        else:
            yield test, None, 0

def make_testcase(test_name, stats, err_message=None):
    global junit_result_xml
    
    testsuite = junit_result_xml.find('testsuite')
    testcase = ET.SubElement(testsuite, 'testcase')
    testcase.set('classname', 'CI Test')
    testcase.set('name', test_name)
    testcase.set('time', '%.3f' % stats[0])
    
    if stats[1] != 0:
        failure = ET.SubElement(testcase, 'failure')
        failure.set('message', 'Test Failure')
        failure.text = err_message
    
    return testcase

def add_system_out(testcase, output_text):
    system_out = ET.SubElement(testcase, 'system-out')
    system_out.text = output_text
    return system_out

def run_command(command, verbose=True, timeout=600):
    print('> Running: %s' % command)
    FNULL = open(os.devnull, 'w')
    start_time = time.time()
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output_text = ""
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                process.terminate()
                print('Command timeout after %d seconds' % timeout)
                return (elapsed_time, 1, '', 'Command Timeout')
            
            # Handle process stdout/stderr
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                output_line = output.decode('utf-8', errors='ignore').rstrip()
                if verbose:
                    print(output_line)
                output_text += output_line + '\n'
        
        return_code = process.poll()
        elapsed_time = time.time() - start_time
        return (elapsed_time, return_code, output_text, '')
    except Exception as e:
        elapsed_time = time.time() - start_time
        return (elapsed_time, 1, '', str(e))

def run_test_script(test):
    global test_count, testsummary
    
    if test.startswith("#"):
        return
    
    command = 'python %s' % test
    
    # -- Running Command --
    (elapsed_time, exit_code, output_text, err_msg) = run_command(command)
    
    # -- Handling Exit Code --
    if exit_code == 0:
        test_status = 'Pass'
        test_count[1] += 1
    else:
        test_status = 'Fail'
        test_count[2] += 1
    
    return (elapsed_time, exit_code, output_text, err_msg)

def save_result_xml():
    global junit_result_xml, xml_filename
    
    testsuite = junit_result_xml.find('testsuite')
    testsuite.set('tests', str(test_count[0]))
    testsuite.set('failures', str(test_count[2]))
    testsuite.set('skipped', str(test_count[3]))
    
    xmlstr = minidom.parseString(ET.tostring(junit_result_xml)).toprettyxml(indent="  ")
    with open(xml_filename, "w") as f:
        f.write(xmlstr)

def save_report_xlsx():
    global testsummary, xlsx_filename
    
    df = pd.DataFrame.from_dict(testsummary, orient='index', 
                               columns=['Time(s)', 'Exit Code', 'Result', 'Detail'])
    df.index.name = 'Test Name'
    
    with pd.ExcelWriter(xlsx_filename) as writer:
        df.to_excel(writer, sheet_name='Test Report')

def init_result_xml():
    global junit_result_xml, test_suite_name
    
    junit_result_xml = ET.Element("testsuites")
    testsuite = ET.SubElement(junit_result_xml, "testsuite")
    testsuite.set('name', test_suite_name)
    testsuite.set('timestamp', datetime.now().isoformat())

def ci_runner(test_suites):
    global test_script_array, test_suite_name, result_basename
    global junit_result_xml, xml_filename, xlsx_filename
    global test_datetime, result_dir
    
    print("--- CI Test Started ---")
    test_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # --- Load CI Test Config ---
    if isinstance(test_suites, list):
        test_script_array = test_suites
        test_suite_name = 'CI_Test'
        result_basename = test_suite_name
    else:
        with open(test_suites, 'r') as f:
            cfg = yaml.safe_load(f)
        test_script_array = cfg.get('script', [])
        test_suite_name = cfg.get('name', 'CI_Test')
        result_basename = os.path.basename(test_suites).replace('.yaml', '')
    
    # --- Prepare Result Files ---
    result_dir = os.path.join(test_result_path, '%s_%s' % (result_basename, test_datetime))
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    
    xml_filename = os.path.join(result_dir, 'junit-report.xml')
    xlsx_filename = os.path.join(result_dir, 'test-report.xlsx')
    
    # --- Init Result XML ---
    init_result_xml()
    
    # --- Run Tests ---
    for test, param, param_index in get_testsuite_extended():
        if param == None:
            testName = '%s' % test.replace('.py', '')
        else:
            testName = '%s_%02d' % (test.replace('.py', ''), param_index)
        
        testsummary[testName] = [0, 0, 0, 0]
        
        if test.startswith('#'):
            print('Skip test: %s' % test)
            testsummary[testName] = [0, 0, 'Skip', '']
            test_count[3] += 1
            testcase = make_testcase(testName, [0, 0])
            add_system_out(testcase, 'Test Skipped')
            continue
        
        test_count[0] += 1
        print('\n=== Running Test: %s ===' % testName)
        
        # --- Run Test Command ---
        if param == None:
            (elapsed_time, return_code, output_text, err_msg) = run_test_script(test)
        else:
            # Handle parameterized test...
            (elapsed_time, return_code, output_text, err_msg) = [0, 0, '', '']  # Placeholder
        
        # --- Process Test Results ---
        testResult = 'Pass' if return_code == 0 else 'Fail'
        testsummary[testName] = [elapsed_time, return_code, testResult, err_msg]
        
        testcase = make_testcase(testName, [elapsed_time, return_code], err_msg)
        add_system_out(testcase, output_text)
        
        # --- Save intermediate results ---
        save_result_xml()
        save_report_xlsx()
    
    # --- Test Complete ---
    print('\n--- Test Complete ---')
    print('Total: %d, Pass: %d, Fail: %d, Skip: %d' % 
          (test_count[0], test_count[1], test_count[2], test_count[3]))
    
    save_result_xml()
    save_report_xlsx()
    
    return test_count[2] == 0

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    if len(sys.argv) > 1:
        test_suites = sys.argv[1]
    else:
        test_suites = "ci_test.yaml"
    
    success = ci_runner(test_suites)
    exit(0 if success else 1)


# 动态调整Y轴上限 - 关键修改部分
                if normal_values:
                    max_value = max(normal_values)
                    min_value = min(normal_values)
                    
                    if max_value > 0:
                        # 计算合适的上限，确保数据变化可见
                        # 对于非常小的值，设置一个合理的范围
                        if max_value < 1e-5:
                            # 找到最小和最大值的数量级
                            if min_value > 0:
                                min_power = np.floor(np.log10(min_value))
                                max_power = np.ceil(np.log10(max_value))
                                
                                # 如果数量级相差不大，使用实际范围
                                if max_power - min_power <= 2:
                                    ymax = max_value * 1.5
                                else:
                                    # 否则使用最大值的合适倍数
                                    ymax = max_value * 10
                            else:
                                # 如果最小值为0，使用最大值的合适倍数
                                ymax = max_value * 10
                        else:
                            # 对于较大的值，使用实际范围
                            ymax = max_value * 1.2
                    else:
                        ymax = 1e-10  # 默认一个小的正值
                else:
                    ymax = 1e-10  # 默认一个小的正值
            
            # 设置Y轴范围
            self.ax.set_ylim(ymin, ymax)