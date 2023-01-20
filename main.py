# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from scipy.io import loadmat, savemat

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    first_file = loadmat('stage1_proc.mat')
    second_file = loadmat
    print(first_file.keys())
    print(first_file['Ly'][0][0])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
