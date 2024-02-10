"""
THIS FILE IS NOT GRADED.

Please refer to the HW PDF for description of this file.
"""

import sys

from abc import ABC, abstractmethod
from collections import Counter
from enum import Enum
from typing import List

class Component(Enum):
    PHT = 0
    BHT = 1

class BranchResult(Enum):
    NOT_TAKEN = 0
    TAKEN = 1

class Reg(Enum):
    PC = 0
    BHR = 1

class Table():
    def __init__(self, n):
        self._data = [0b0] * n

    def GetTableVal(self, idx):
        return self._data[idx]

    def SetTableVal(self, idx, val):
        self._data[idx] = val

class MultiTable():
    def __init__(self, num_tables, n):
        self._data = [Table(n) for i in range(num_tables)]

    def GetTableVal(self, tid, idx):
        return self._data[tid].GetTableVal(idx)

    def SetTableVal(self, tid, idx, val):
        self._data[tid].SetTableVal(idx, val)

class RegisterFile():
    _REG_LEN = (1 << 16)
    
    def __init__(self):
        self._rf = Table(len(Reg))

    def GetRegVal(self, reg):
        return self._rf.GetTableVal(reg.value)

    def SetRegVal(self, reg, val):
        self._rf.SetTableVal(reg.value, val % self._REG_LEN)

class AbstractPredictor(ABC):
    def __init__(self):
        self._rf = RegisterFile()
        self.Initialize()

    def GetRegVal(self, reg):
        return self._rf.GetRegVal(reg)

    def SetRegVal(self, reg, val):
        self._rf.SetRegVal(reg, val)

    @abstractmethod
    def Initialize(self):
        pass

    @abstractmethod
    def Predict(self, target_address : int) -> BranchResult:
        pass
    
    @abstractmethod
    def Update(self, target_address : int, predicted_result : BranchResult, actual_result : BranchResult):
        pass

class PredRunner():
    def __init__(self, pred_name):
        self._pred_name = pred_name.lower()
        if self._pred_name == "static":
            from static import StaticPredictor
            self._predictor = StaticPredictor()
        elif self._pred_name == "local":
            from local import LocalPredictor
            self._predictor = LocalPredictor()
        elif self._pred_name == "gskew":
            from gskew import GskewPredictor
            self._predictor = GskewPredictor()
        else:
            print("Unknown predictor " + self._pred_name + "\n")
            sys.exit(1);
        self._trace_list = list()

    def ParseTrace(self, trace_line):
        trace = [int(s) for s in trace_line.strip().split(",")]
        pc = trace[0]
        t_addr = trace[1]
        b_result = dict()
        b_result["actual"] = BranchResult(trace[2])
        b_result["static"] = BranchResult(trace[3])
        b_result["local"] = BranchResult(trace[4])
        b_result["gskew"] = BranchResult(trace[5])
        return pc, t_addr, b_result

    def ParseFile(self, trace_file_path : str) -> List:
        self._trace_list = list()
        with open(trace_file_path) as trace:
            for line in trace:
                self._trace_list.append(line)

    def Iteration(self, trace) -> List[bool]:
        pc, t_addr, b_result = self.ParseTrace(trace)
        self._predictor.SetRegVal(Reg.PC, pc)
        pred_result = self._predictor.Predict(t_addr)
        self._predictor.Update(t_addr, pred_result, b_result["actual"])
        return pred_result.value == b_result["actual"].value, pred_result.value == b_result[self._pred_name].value

    def ExecuteTrace(self) -> List[int]:
        count_same_as_expected = 0
        count_same_as_actual = 0
        for trace in self._trace_list:
            same_as_actual, same_as_expected = self.Iteration(trace)
            if same_as_actual:
                count_same_as_actual += 1
            if same_as_expected:
                count_same_as_expected += 1
        return count_same_as_expected, count_same_as_actual
    
    def PrintResult(self, same_as_expected : int, same_as_actual : int):
        accuracy = (float(same_as_actual) / float(len(self._trace_list))) * 100.0
        print("=============={} Results==============".format(self._pred_name.capitalize()))
        print("[{}/{}] {}% predictions match expected".format(same_as_expected, len(self._trace_list), round(float(same_as_expected * 100.00) / float(len(self._trace_list))), 2))
        print("{}% prediction accuracy".format(round(accuracy, 2)))

    def Run(self, trace_file_path : str):
        self.ParseFile(trace_file_path)
        same_as_expected, same_as_actual = self.ExecuteTrace()
        self.PrintResult(same_as_expected, same_as_actual)
