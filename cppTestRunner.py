# cppTestRunner.py
# v1.0
# run a small piece of cpp code with given test inputs and match them with given test outputs
# by Alex Yu

import subprocess as sp
import os
import re
import timeout_decorator


@timeout_decorator.timeout(2, use_signals=False)
def run_single_test(param, cpp_program, test_id):
    test_input = param["testInput_dir"] + "/" + str(test_id) + ".in"
    test_output = param["testOutput_dir"] + "/" + str(test_id) + ".out"
    sentence_1 = "cd " + param["cppOut_dir"] + " && " \
                 + "./" + re.sub('.cpp', '.o', cpp_program, flags=re.I)\
                 + " < " + test_input
    try:
        cmd_1 = sp.check_output(sentence_1, shell=True)
    except Exception as e:
        return "WA"
    else:
        sentence_2 = "cat " + test_output
        try:
            cmd_2 = sp.check_output(sentence_2, shell=True)
        except Exception as ee:
            return "WA: weird"
        else:
            if cmd_1 == cmd_2:
                return "PASS"
            else:
                return "WA"


def run_single_cpp_program(param, cpp_program):
    correct_count = 0
    target_obj = param["cppOut_dir"] + "/" + re.sub('.cpp', '.o', cpp_program, flags=re.I)
    print("Running " + cpp_program + " ...")
    try:
        sentence = "g++ " + param["cppSrc_dir"] + "/" + cpp_program + " -o " + target_obj
        cmd = sp.check_output(sentence, shell=True)
    except sp.CalledProcessError:
        print("cannot compile " + cpp_program + "!")
        return 0.0
    else:
        input_dir = param["testInput_dir"]
        testNum = len([name for name in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, name))])
        for i in range(1, testNum + 1):
            try:
                print("TestCase " + str(i) + ": ", end="")
                result = run_single_test(param, cpp_program, i)
                print(result)
                if result == "PASS":
                    correct_count += 1
            except Exception as te:
                print(str(te))
                print("TLE")
        correctness = correct_count / testNum
        return correctness


def run_task(param):
    """
    run all cpp programs in src dir
    :param param: the dict of initialized parameters
    :return:
    """
    for root, dirs, files in os.walk(param["cppSrc_dir"]):
        for file in files:
            correctness = run_single_cpp_program(param, file)
            print("the correctness of " + file + " is " + str(correctness * 100) + "%")


def initialize_param(taskName):
    """
    initialize the directories for the following task
    :param taskName: the name of the task
    :return: the dict of initialized parameters
    """
    project_dir = os.path.dirname(os.path.realpath(__file__))
    cppSrc_dir = project_dir + "/CppSrc/" + taskName
    cppOut_dir = project_dir + "/CppOut/" + taskName
    testInput_dir = project_dir + "/TestCases/TestInputs/" + taskName
    testOutput_dir = project_dir + "/TestCases/TestOutputs/" + taskName
    param = {
        "cppSrc_dir":       cppSrc_dir,
        "cppOut_dir":       cppOut_dir,
        "testInput_dir":    testInput_dir,
        "testOutput_dir":   testOutput_dir
    }
    return param


def main():
    param = initialize_param("sort")
    run_task(param)


if __name__ == '__main__':
    main()
