"""
Static Predictor

Please refer to the HW PDF for description of this task.
"""

from base import *

class StaticPredictor(AbstractPredictor):
    def Initialize(self):
        pass

    def Update(self, target_address : int, predicted_result : BranchResult, actual_result : BranchResult):
        pass

    def Predict(self, target_address : int) -> BranchResult:
        
        branch_address = self.GetRegVal(Reg.PC)

        print(branch_address)
        if target_address > branch_address:
            return BranchResult.TAKEN
        
        return BranchResult.NOT_TAKEN