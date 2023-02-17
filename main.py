import os

import numpy as np
import pandas as pd
from scipy.io import loadmat, savemat

new_file_dict = {}
ignore_keys = ['__header__', '__version__', '__globals__', '__version__', '__globals__', 'save_mat', 'filenames'
    , 'save_path', 'avgframe_reshape', 'avgmotion_0', 'avgmotion_reshape', 'motMask_0', 'motMask_1',
               'motMask_reshape_0',
               'motMask_reshape_1', 'motMask', 'motMask_reshape', 'running', 'running_0', 'blink', 'blink_0']
stack_on = False


def mergefiles(dict_1, dict_2):
    dict_3 = {}
    # Check for missing keys
    missing_keys = {1: [], 2: []}
    for i in dict_1.keys():
        if i not in ignore_keys:
            if i not in dict_2.keys():
                missing_keys[2].append(i)

    for i in dict_2.keys():
        if i not in ignore_keys:
            if i not in dict_1.keys():
                missing_keys[1].append(i)

    for key, value in dict_1.items():
        if key not in ignore_keys:
            if not stack_on:
                dfAlpha = pd.DataFrame({"a": [value]})
                dict_3[key] = dfAlpha
                if value.size == 0:
                    dict_3[key] = value
            else:
                dict_3[key] = value
    for i in missing_keys[1]:
        dfAlpha = pd.DataFrame({"a": [np.empty_like(dict_2.get(i))]})
        dict_3[i] = dfAlpha

    for key, value in dict_2.items():
        if key not in ignore_keys:
            if value.size == 0:
                continue
            dfAlpha = pd.DataFrame({"b": [value]})
            dict_3[key] = np.concatenate((dict_3.get(key), dfAlpha), axis=1)

    for i in missing_keys[2]:
        dfAlpha = pd.DataFrame({"b": [np.empty_like(dict_1.get(i))]})
        dict_3[i] = np.concatenate((dict_3.get(i), dfAlpha), axis=1)

    return dict_3


if __name__ == '__main__':
    list_of_files = []
    mouse_number = ["1", "2", "3", "8", "14", "16"]
    files_to_convert = ["Day 9", "Day 10", "Immediately after Stroke", "Post D1", "Post D3", "Post D7", "Post D10"]
    stage_number = [*range(3)]

    current_directory = os.getcwd()
    root_directory = os.path.dirname(current_directory)
    # print(current_directory)
    for stage_num in stage_number:
        for mouse_num in mouse_number:
            for i in files_to_convert:
                current_directory = root_directory + "/Experiment 2/Face Videos/" + i + "/"+mouse_num
                os.chdir(current_directory)
                list_of_files.append(loadmat(f'stage{stage_num +1}_proc.mat'))
        first_file = list_of_files[0]
        second_file = list_of_files[1]
        third_file = mergefiles(first_file, second_file)
        stack_on = True
        for remaining_rounds in range(3, len(list_of_files)-1):
            first_file = third_file
            second_file = list_of_files[remaining_rounds]
            third_file = mergefiles(first_file, second_file)

        savemat(f'stage{str(stage_num +1)}_file.mat', third_file)


    # current_directory = os.getcwd()
    # print(current_directory)

    # first_file = loadmat('testMat.mat')
    # second_file = loadmat('stage2_proc_2.mat')
    # stack_on = True
    # # print(first_file)
    #
    # third_file = mergefiles(first_file, second_file)
    #
    # savemat("testMat.mat", third_file)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
