"""
THIS FILE IS NOT GRADED.

Please refer to the HW PDF for description of this file.
"""

import argparse
import os
import sys

from base import *

_ARG_DESC = """
CS 433 Spring 2024 HW 2 Runner
 """
_HELP_MSG = """
This runner calls your branch prediction code on a trace. You can find an example traces in the traces/ directory.
For any questions, you can reach the course staff by making a post on Ed. Enjoy coding!
"""
_USAGE_MSG = """Please use python3 bpred.py -h to print help commands"""
_PREDICTION_ALGOS = ["static", "local", "gskew"]

def main():
    parser = argparse.ArgumentParser(add_help = False, description = _ARG_DESC, epilog = _HELP_MSG, usage = _USAGE_MSG)
    parser.add_argument("-h", "--help", action = "help", default = argparse.SUPPRESS, help = "Documentation")
    parser.add_argument("-p", "--predictor", help = "Branch prediction algorithm to test " + str(_PREDICTION_ALGOS), metavar = "", required = True, nargs = 1)
    parser.add_argument("-t", "--trace", help = "Path to trace file", metavar="", required=True, nargs=1)
    args = parser.parse_args()

    prediction_algorithm = args.predictor[0]

    if prediction_algorithm not in _PREDICTION_ALGOS:
        print("Incorrect predictor \"{}\" passed".format(prediction_algorithm))
        sys.exit(1)

    trace_path = args.trace[0]

    if not os.path.isfile(trace_path):
        print("Trace file path \"{}\" invalid".format(trace_path))
        sys.exit(1)

    pred = PredRunner(prediction_algorithm)
    pred.Run(trace_path)

if __name__=="__main__":
    main()
