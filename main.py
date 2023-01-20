
import numpy as np
import pandas as pd
from scipy.io import loadmat, savemat

new_file_dict = {}
ignore_keys = ['__header__', '__version__', '__globals__', '__version__', '__globals__', 'save_mat', 'filenames'
               ,'save_path', 'avgframe_reshape', 'avgmotion_0', 'avgmotion_reshape']

def mergefiles(dict_1, dict_2):
    dict_3 = {}
    for key, value in dict_1.items():
        if key not in ignore_keys:
            dfAlpha = pd.DataFrame({"a": [value]})
            dict_3[key] = dfAlpha
            if value.size == 0:
                dict_3[key] = value
    for key, value in dict_2.items():
        if key not in ignore_keys:
            if type(value) is np.ndarray:
                print(str(value.ndim))
                if value.size == 0:
                    continue
                dfAlpha = pd.DataFrame({"b": [value]})
                dict_3[key] = np.concatenate((dict_3.get(key), dfAlpha), axis=1)

    return dict_3


if __name__ == '__main__':
    first_file = loadmat('stage1_proc 1.mat')
    second_file = loadmat('stage1_proc 2.mat')

    third_file = mergefiles(first_file, second_file)

    savemat("testMat.mat", third_file)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
