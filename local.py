"""
Local Predictor 

Please refer to the HW PDF for description of this task.
"""

from base import *

class LocalPredictor(AbstractPredictor):
    def Initialize(self):
        self.pht = Table(1 << 7) # DO NOT CHANGE VARIABLE NAME
        #Initialize PHT here
        for i in range(0, 128):
            self.pht.SetTableVal(i, 0b0111)

        #Initialize BHT here
        self.bht = Table(1 << 6) # DO NOT CHANGE VARIABLE NAME
        for i in range(0, 63):
            self.bht.SetTableVal(i, 0b0000000)

    def Update(self, target_address : int, predicted_result : BranchResult, actual_result : BranchResult):

        base_address = self._rf.GetRegVal(Reg.PC)
        bht_index = base_address >> 1 & 0b111111
        pht_index = self.bht.GetTableVal(bht_index)

        curr_pht_val = self.pht.GetTableVal(pht_index)

        if actual_result == BranchResult.TAKEN :
            # add one to pht
            if curr_pht_val != 0b1111:
                self.pht.SetTableVal(pht_index, curr_pht_val + 1)
            new_bht_val = ((pht_index << 1) & 0b01111111) + 1
            self.bht.SetTableVal(bht_index, new_bht_val)
        else:
            if curr_pht_val != 0b0000:
                self.pht.SetTableVal(pht_index, curr_pht_val - 1)
            new_bht_val = ((pht_index << 1) & 0b01111111)
            self.bht.SetTableVal(bht_index, new_bht_val)

            

    def Predict(self, target_address : int) -> BranchResult:

        base_address =self._rf.GetRegVal(Reg.PC)

        bht_index = (base_address >> 1) & 0b111111
        pht_index = self.bht.GetTableVal(bht_index)

        val = self.pht.GetTableVal(pht_index)

        if val >= 0b1000 :
            return BranchResult.TAKEN
        else:
            return BranchResult.NOT_TAKEN
        

