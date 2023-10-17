from .base import AESBase
import numpy as np
from utils.converter import key_to_hex_array, array_shift, array_s_box, xor_array
from utils.gen_sbox import generate_s_box, inv_s_box_gen
from utils.constant import AES_s_box

class AES128(AESBase):
    def __init__(self):
        super().__init__(rounds=10, order=10)

    def add_round_key(self, key_str):
        order = 4
        hex_key = key_to_hex_array(key_str)
        self.ROUND_KEY.append(hex_key)

        for i in range(0, self.ROUND):
            prev_arr = self.ROUND_KEY[-1]
            self.S_BOX.append(generate_s_box(prev_arr.reshape(16), 16, i))
            self.INV_S_BOX.append(inv_s_box_gen(self.S_BOX[i]))

            last_col = prev_arr[order-1]
            shift_col = array_shift(last_col)
            if i == 0:
                s_box_col = array_s_box(shift_col, AES_s_box)
            else:
                s_box_col = array_s_box(shift_col, self.S_BOX[i])
            col_1 = xor_array(prev_arr[0], s_box_col, i)
            col_2 = xor_array(col_1, prev_arr[1])
            col_3 = xor_array(col_2, prev_arr[2])
            col_4 = xor_array(col_3, prev_arr[3])
            new_arr = np.array([col_1, col_2, col_3, col_4])
            self.ROUND_KEY.append(new_arr)
