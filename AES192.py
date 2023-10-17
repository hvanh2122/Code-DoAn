from .base import AESBase
import numpy as np
from utils.converter import key_to_hex_array, array_shift, array_s_box, xor_array
from utils.gen_sbox import generate_s_box, inv_s_box_gen
from utils.constant import AES_s_box

class AES192(AESBase):
    def __init__(self):
        super().__init__(rounds=12, order=8)

    def add_round_key(self, key):
        row, col = 6, 4
        expansion = 8
        hex_key = key_to_hex_array(key, row, col)
        self.ROUND_KEY.append(hex_key)
        for i in range(0, expansion):
            prev_arr = self.ROUND_KEY[-1]
            self.S_BOX.append(generate_s_box(hex_key.reshape(24), 24, i))
            self.INV_S_BOX.append(inv_s_box_gen(self.S_BOX[i]))
            last_col = prev_arr[row-1]
            shift_col = array_shift(last_col)
            if i == 0:
                s_box_col = array_s_box(shift_col, AES_s_box)
            else:
                s_box_col = array_s_box(shift_col, self.S_BOX[i])
            col_1 = xor_array(prev_arr[0], s_box_col, i)
            col_2 = xor_array(col_1, prev_arr[1])
            col_3 = xor_array(col_2, prev_arr[2])
            col_4 = xor_array(col_3, prev_arr[3])
            col_5 = xor_array(col_4, prev_arr[4])
            col_6 = xor_array(col_5, prev_arr[5])
            new_arr = np.array([col_1, col_2, col_3, col_4, col_5, col_6])
            self.ROUND_KEY.append(new_arr)
        super().convert_round_key()
