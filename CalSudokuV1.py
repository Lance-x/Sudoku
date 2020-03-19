# -*- coding: utf-8 -*-
"""
CalSudoku.py
Created on Mon Mar 16 17:20:56 2020.

@author: Lance.Xu
"""
from time import perf_counter
from copy import deepcopy

Tmp1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],    # 空白模板，测试用
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]
Tmp2 = [[1, 0, 0, 0, 0, 0, 0, 0, 0],    # 非标准数独，测试用
        [0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 9]]
Tmp3 = [[8, 0, 0, 0, 0, 0, 0, 0, 0],    # 芬兰数学家 因·卡拉（Arto Inkala）设计的号称“最难数独”
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]]
AnswerArr = []


def ini_Candidate():
    """
    初始化候选数字典列表
    二维列表，每个元素是一个字典类型
    字典中的 key 是候选数，Value 无关
    初始时所有位置候选数都是 1 到 9
    :param: 无参
    :return: 初始化后的候选数列表
    """
    Candidate = []
    tmp = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: ""}
    for i in range(9):
        Candidate.append(deepcopy(tmp))
    tmp = deepcopy(Candidate)
    Candidate = []
    for i in range(9):
        Candidate.append(deepcopy(tmp))
    return Candidate


def DelCan(Candidate, row: int, column: int, key: int):
    """
    根据在指定位置填入的数字，删除所在行、列、宫的其它位置的候选数
    如：在（1，2）位置写入 7，则第 1 行、第 2 列和该位置所在的宫格内所有的候选数7都删除
    :param Candidate: 候选数列表
    :param row: 行
    :param column: 列
    :param key: 填入的数字
    :return: 删除完成的候选数列表
    """
    MySqu = 3 * (row // 3) + column // 3            # 根据行、列计算所在宫格
    for k in range(9):                              # 每行，每列，每宫格都是9个位置，放进同一个循环中处理
        Candidate[row][k].pop(key, "")              # 同一行中如果存在候选数 key 则删除
        Candidate[k][column].pop(key, "")           # 同一列中如果存在候选数 key 则删除
        MyRow1 = 3 * (MySqu // 3) + k // 3          # 根据宫格和序列 k 计算所在行
        MyColumn1 = 3 * (MySqu % 3) + k % 3         # 根据宫格和序列 k 计算所在列
        Candidate[MyRow1][MyColumn1].pop(key, "")   # 同一宫中如果存在候选数 key 则删除
    return Candidate


def CandidateGen(Candidate, Sudoku):
    """
    根据数独生成候选数列表
    :param Candidate: 候选数列表
    :param Sudoku: 需要计算的数独
    :return: 根据数独生成的候选数列表
    """
    for i in range(9):                      # 双重循环，遍历数独中每一个元素
        for j in range(9):
            if Sudoku[i][j] != 0:           # 如果该位置不是0
                Candidate[i][j].clear()     # 则删除这个位置所有的候选数
                Candidate = DelCan(Candidate, i, j, Sudoku[i][j])   # 调用 DelCan 函数删除所在行、列、宫对应的候选数
    return Candidate


def Check(Candidate, Sudoku):
    """
    根据数独和候选数判断数独状态是成功、失败还是未完成
    :param Candidate: 候选数列表
    :param Sudoku: 需要计算的数独
    :return:-1：失败，0:未完成，1：成功
    """
    count = 0       # 统计数独中空白位置数量
    # 生成一个 3x9 的字典列表 CheCan 辅助判断，3分别表示：行、列、宫，9表示每一个行（列、宫）中有9个位置
    tmp = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: ""}
    CheCan = []
    for i in range(3):
        CheCan.append([])
        for j in range(9):
            CheCan[i].append(deepcopy(tmp))

    for i in range(9):                              # 双重循环遍历数独中每一个位置
        for j in range(9):
            if Sudoku[i][j] == 0:                 # 如果该位置为空
                count = count + 1                   # 统计空白位置数量
                if len(Candidate[i][j]) == 0:       # 如果候选数数量为 0
                    return -1                       # 空格无候选数，返回失败
            else:                                 # 如果该位置有数字
                if Sudoku[i][j] in CheCan[0][i]:    # 如果辅助列表CheCan行中存在
                    del CheCan[0][i][Sudoku[i][j]]  # 则从辅助列表CheCan行中删除他
                else:                               # 如果不存在（之前被删除过一次）
                    return -1                       # 行中重复返回失败
                if Sudoku[i][j] in CheCan[1][j]:    # 如果辅助列表CheCan列中存在
                    del CheCan[1][j][Sudoku[i][j]]  # 则从辅助列表CheCan列中删除他
                else:                               # 如果不存在（之前被删除过一次）
                    return -1                       # 列中重复返回失败
                MySqu = 3 * (i // 3) + j // 3       # 根据行、列计算所在宫格
                if Sudoku[i][j] in CheCan[2][MySqu]:    # 如果辅助列表CheCan宫中存在
                    del CheCan[2][MySqu][Sudoku[i][j]]  # 则从辅助列表CheCan宫中删除他
                else:                               # 如果不存在（之前被删除过一次）
                    return -1                       # 宫格中重复返回失败
    if count == 0:  # 如果数字全满，并且上面没有返回
        return 1    # 则返回成功
    else:           # 如果未满，并且上面没有返回
        return 0    # 则返回未完成


def Sole(Candidate, Sudoku):
    """
    行、列、宫候选数唯一法填放数字
    :param Candidate: 候选数列表
    :param Sudoku: 需要计算的数独
    :return:Candidate:最后生成的候选数列表，Sudoku最后生成的数独状态
    """
    Flag = 1                                                    # 标志位
    while Flag == 1:                                            # 标志位为 1 继续循环
        Flag = 0                                                # 重置标志位
        for i in range(9):                                      # 双重循环遍历数独中每一个位置
            for j in range(9):
                if Sudoku[i][j] == 0:                           # 如果该位置为空
                    if len(Candidate[i][j]) == 1:               # 如果该位置只有一个候选数
                        Sudoku[i][j] = list(Candidate[i][j])[0]   # 写入这个唯一数
                        Candidate[i][j].clear()                   # 清除该位置候选数
                        Candidate = DelCan(Candidate, i, j, Sudoku[i][j])    # 调用DelCan函数，删除所在行、列、宫其它位置候选数
                        continue                                # 处理下一个位置
                    Candi = deepcopy(Candidate[i][j])
                    # 取出该位置候选数放入Candi中（如果不取出，后面修改Candidate[i][j]后会有报错）
                    for key in Candi:                           # 依次取出候选数中的数字
                        RNum = 0                                # 行统计
                        CNum = 0                                # 列统计
                        BNum = 0                                # 宫统计
                        for k in range(9):                      # 遍历所在行、列、宫
                            if key in Candidate[i][k]:          # 如果行中存在 RNum + 1
                                RNum += 1
                            if key in Candidate[k][j]:          # 如果列中存在 CNum + 1
                                CNum += 1
                            MySqu = 3 * (i // 3) + j // 3       # 根据行列计算宫
                            MyRow = 3 * (MySqu // 3) + k // 3   # 根据宫，格计算行
                            MyColumn = 3 * (MySqu % 3) + k % 3  # 根据宫格计算列
                            if key in Candidate[MyRow][MyColumn]:   # 如果宫中存在 BNum + 1
                                BNum += 1
                        if RNum == 1 or CNum == 1 or BNum == 1:  # 行、列、宫任一个唯一
                            Sudoku[i][j] = key                  # 写入这个唯一数
                            Candidate[i][j].clear()             # 清除该位置候选数
                            Candidate = DelCan(Candidate, i, j, key)    # 调用DelCan函数，删除所在行、列、宫其它位置候选数
                            # Flag = 1                            # 如果数据发生变化，给Flag赋值，再次循环
                            break                               # 跳出本次循环，进入下一个单元格
    return Candidate, Sudoku


def Trial(MyRow: int, MyColumn: int, Candidate, Sudoku):
    """
    核心递归函数，对不能用唯一法确定数字的位置，用候选数中的数字依次尝试，直到得出正确结果（很 * 很暴力）。
    :param MyRow: 开始行
    :param MyColumn: 开始列
    :param Candidate: 候选数列表
    :param Sudoku: 数独
    :return: 无（并非真正的无返回值，因为 Python 中列表和字典类型的调用是通过地址引用的方式调用的，
                所以修改后的数据调用后的位置可以直接使用。）
    """
    global AnswerArr                                            # 用来存放计算结果的数组
    CanBak = deepcopy(Candidate)                                # 备份候选数列表
    SudoBak = deepcopy(Sudoku)                                  # 备份数独状态
    for key in CanBak[MyRow][MyColumn]:                         # 利用备份的候选数列表遍历（因为候选数列表后面会发生变化，如果直接用的话会报错）
        Sudoku[MyRow][MyColumn] = key                           # 尝试写入候选数
        Candidate[MyRow][MyColumn].clear()                      # 删除当前位置候选数
        Candidate = DelCan(Candidate, MyRow, MyColumn, key)     # 调用 DelCan 函数删除所在行列宫候选数
        Candidate, Sudoku = Sole(Candidate, Sudoku)             # 调用 Sole 函数，用唯一法尝试完成数独
        MyCheck = Check(Candidate, Sudoku)                      # 检查数独是完成，有三种情况：完成，未完成，失败
        if MyCheck == 1:                                        # 如果完成
            AnswerArr.append(deepcopy(Sudoku))                  # 写入答案列表
            break                                               # 跳出循环（结束本次调用，如果求解非唯一解数独需要去掉这一行）
        else:                                                   # 如果不等于1（合并失败和未完成状态，因为这两种状态都需要写回溯函数）
            if MyCheck == 0:                                    # 如果是未完成状态向下递归
                for i in range(9 * MyRow + MyColumn + 1, 80):   # 从下一个位置遍历数独
                    if Sudoku[i // 9][i % 9] == 0:              # 找到空白位置
                        Trial(i // 9, i % 9, Candidate, Sudoku)  # 递归调用本函数，尝试下一个空白位置试值
                        break                                   # 递归调用完成后不再去找下一个空白位置（因为候选数中上肯定有正确数字）
            if len(AnswerArr) >= 1:                             # 如果有答案（非唯一解数独需要求几个解把 1 改成几）
                break                                           # 跳出循环（结束调用，如果非唯一解数独所有解，删除195行，上面一行和本行）
        Sudoku = deepcopy(SudoBak)                              # 失败回溯数独状态
        Candidate = deepcopy(CanBak)                            # 失败回溯候选数列表
    return


def sudokuGen(text):
    """
    根据输入的数字转换成二维列表
    :param text:输入的一串81位的数字（如果输入超过81位，只取前81位）
    :return:返回生成的二维列表型数独
    """
    Sudoku = []                         # 定义一个列表
    tmp = []                            # 定义 tmp 变量（纯粹为了消除报错）
    for i in range(81):                 # 遍历 text 的前 81 位
        if i % 9 == 0:                  # 够一行初始化 tmp
            tmp = []                    # 过渡变量，够 9 个加入 Sudoku 中
        if "0" <= text[0] <= "9":       # 判断是不是数字，如果是
            tmp.append(eval(text[0]))   # 加入到 tmp 后面
            text = text[1:]             # 删除 text 第一位字符
        else:                           # 如果输入的不是数字
            tmp.append(0)               # 按 0 处理，加入到 tmp 后面
            text = text[1:]             # 删除 text 第一位字符
        if i % 9 == 0:                  # 够 9 位 存入 Sudoku 后面
            Sudoku.append(tmp)
    return Sudoku                       # 返回生成的数独二维列表


def inputSudoku():
    """
    输入数独函数
    :param: 无参数
    :return: 返回生成的数独
    """
    text = input("请输入一个数独（连续81个数字；或者9行数字，每行9个）：")
    while 1:                                # 无限循环，直到输入的数字达到 81 个
        if len(text) < 81:
            text += input("请继续输入（还缺少{}位）:".format(81 - len(text)))      # 新输入的数字写到 text 后面
        else:
            break                           # 够 81 个数字退出
    return sudokuGen(text)                  # 调用 sudokuGen 函数，将生成的数独验证，转换为二维列表，并返回


def CalSudoku(Sudoku=None):
    """
    主函数，根据传入的数独求解并输出，如果没有参数传入，则使用 Tmp3 做为要计算的数独
    :param Sudoku: 传入的数独
    :return: 无返回值
    """
    if Sudoku is None:
        Sudoku = Tmp3
    Candidate = ini_Candidate()                         # 调用ini_Candidate函数，初始化候选数列表
    global AnswerArr                                    # 引入公共变量AnswerArr,用来存放答案数据
    Candidate = CandidateGen(Candidate, Sudoku)         # 根据数独生成候选数列表
    Candidate, Sudoku = Sole(Candidate, Sudoku)         # 调用 Sole 函数，用唯一法先填一次
    MyCheck = Check(Candidate, Sudoku)                  # 调用　Check 函数检查数独状态
    if MyCheck == 0:                                   # 如果未完成
        for i in range(81):                             # 遍历数独
            if Sudoku[i // 9][i % 9] == 0:              # 查找空白位置
                Trial(i // 9, i % 9, Candidate, Sudoku)  # 调用 Trial 函数完成数独
                break                                   # 主函数只调用一次
    elif MyCheck == 1:                                  # 如果一次完成
        AnswerArr.append(deepcopy(Sudoku))              # 把结果写入答案列表
    elif MyCheck < 0:                                   # 如果失败，数独无解
        return -1                                       # 返回 -1
    return AnswerArr[0]
    for i in range(len(AnswerArr)):                     # 遍历答案列表，输出答案
        print()
        for j in range(9):
            print(AnswerArr[i][j])


# Sudoku = inputSudoku()      # 手动输入数独
# t = perf_counter()          # 记录开始时间
# CalSudoku(Sudoku)                # 调用 main 函数计算数独并输出
# print("共用时{:.4f}秒".format(perf_counter() - t))   # 输出总用时
