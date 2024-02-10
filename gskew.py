"""
Gskew Predictor

Please refer to the HW PDF for description of this task.
"""

from base import *

class GskewPredictor(AbstractPredictor):
    _BHR_LEN = 4
    _PHT_SIZE = 1 << 4

    def Initialize(self):
        self.pht = MultiTable(3, self._PHT_SIZE) # DO NOT CHANGE VARIABLE NAME
        # iterate through all three tables and each pht and set correct values
        for i in range (3):
            for j in range(0, 16):
                self.pht.SetTableVal(i, j, 0b01)



    def MajorityVote(self, val_1, val_2, val_3):
        # this function might seem complex but remember that if any two values here equal each other, then you have a majority vote!
        if (val_1 == 2 or val_1 == 3) and (val_2 == 2 or val_2 == 3):
            return BranchResult.TAKEN
        elif (val_1 == 2 or val_1 == 3) and (val_3 == 2 or val_3 == 3):
            return BranchResult.TAKEN
        elif (val_2 == 2 or val_2 == 3) and (val_3 == 2 or val_3 == 3):
            return BranchResult.TAKEN
        else:
            return BranchResult.NOT_TAKEN
        
    def ParseCounter(self, counter : int) -> BranchResult:
        # check if counter is above the specific limit
        if counter > 0b01:
            return BranchResult.TAKEN
    
        return BranchResult.NOT_TAKEN
    
    def UpdateCounter(self, counter : int, predicted_result : BranchResult, actual_result : BranchResult) -> int:
        # refer to lecture slides on how to update the counter

        # you can use predicted_result == BranchResult.TAKEN to compare values
        if predicted_result == BranchResult.TAKEN:
            if counter != 0b11:
                counter += 1
        
        if predicted_result == BranchResult.NOT_TAKEN:
            if counter != 0b00:
                counter -= 1

    def f0(self, t_addr : int, bhr : int):
        # compute xor on first 4 bits of the target address (t_addr) ignoring the least significant bit
        first_four = (t_addr >> 1) & 0b01111
        xor = first_four ^ bhr
        return xor
    
    def f1(self, t_addr : int, bhr : int):
        # compute xor on second 4 bits of the target address (t_addr) ignoring the least significant bit
        next_four = (t_addr >> 5) & 0b01111
        xor = next_four ^ bhr
        return xor

    def f2(self, t_addr : int, bhr : int):
        # compute xor on third 4 bits of the target address (t_addr) ignoring the least significant bit
        last_four = (t_addr >> 9) & 0b01111
        xor = last_four ^ bhr
        return xor

    def Update(self, target_address : int, predicted_result : BranchResult, actual_result : BranchResult):
        # you can access BHR register using Reg.BHR (example, self.GetRegVal(Reg.BHR))

        bhr = self.GetRegVal(Reg.BHR)

        #get index to access pht tables using the bhr and target address
        index_1 = self.f0(target_address, bhr)
        index_2 = self.f1(target_address, bhr)
        index_3 = self.f2(target_address, bhr)

        # as the PHT is multi-dimensional table, make sure you use following function to access it self.pht.GetTableVal(table ID, row number within a table)
    
        #fetch pht values to get majority
        pht_val_1 = self.pht.GetTableVal(0, index_1)
        pht_val_2 = self.pht.GetTableVal(1, index_2)
        pht_val_3 = self.pht.GetTableVal(2, index_3)

        curr_bhr = self.GetRegVal(Reg.BHR)

        #if majority is taken then increment counter by one for all pht. 
        if actual_result == BranchResult.TAKEN:
            # as the PHT is multi-dimensional table, make sure you use following function to access it self.pht.SetTableVal(table ID, row number within a table, new data
            if pht_val_1 != 0b11:
                self.pht.SetTableVal(0, index_1, pht_val_1 + 1)
            if pht_val_2 != 0b11:
                self.pht.SetTableVal(1, index_2, pht_val_2 + 1)
            if pht_val_3 != 0b11:
                self.pht.SetTableVal(2, index_3, pht_val_3 + 1)
            new_bhr = (curr_bhr << 1) & 0b01111 + 1
            self.SetRegVal(Reg.BHR, new_bhr)
            
        else:
            if pht_val_1 != 0b00:
                self.pht.SetTableVal(0, index_1, pht_val_1 - 1)
            if pht_val_2 != 0b00:
                self.pht.SetTableVal(1, index_2, pht_val_2 - 1)
            if pht_val_3 != 0b00:
                self.pht.SetTableVal(2, index_3, pht_val_3 - 1)
            new_bhr = (curr_bhr << 1) & 0b01111 
            self.SetRegVal(Reg.BHR, new_bhr)
            
    

    def Predict(self, target_address : int) -> BranchResult:
        # get bhr and get values from each function f0, f1 and f2
        bhr = self.GetRegVal(Reg.BHR)

        index_1 = self.f0(target_address, bhr)
        index_2 = self.f1(target_address, bhr)
        index_3 = self.f2(target_address, bhr)

        #fetch pht values to get majority
        pht_val_1 = self.pht.GetTableVal(0, index_1)
        pht_val_2 = self.pht.GetTableVal(1, index_2)
        pht_val_3 = self.pht.GetTableVal(2, index_3)

        # do majority vote
        majority = self.MajorityVote(pht_val_1, pht_val_2, pht_val_3)

        return majority