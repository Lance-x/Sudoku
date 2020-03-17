# -*- coding: utf-8 -*-
"""
fileSudo.py
Created on Mon Mar 16 23:30:13 2020.

@author: Lance.Xu
"""
import CalSudokuV1                                          # 导入数独计算器
from time import perf_counter                               # 导入时间模块

count = 0                                                   # 统计题目个娄
t = perf_counter()                                          # 开始计时
file = open("Sudo.txt", "r", encoding="utf-8")              # 打开数独题目文件
txt = file.read()                                           # 读入题目
file.close()                                                # 关闭题目文件
fileAnswer = open("SudoAnswer.txt", "w", encoding="utf-8")  # 打开答案文件
txt = txt.replace("\n", "")                                 # 删除题目中的回车
txt = txt.replace(" ", "")                                  # 删除题目中的空格
for i in range(len(txt) // 81):                             # 遍历每一个题目
    sudo = txt[81 * i:81 * (i + 1)]                         # 取出一个题目
    sudo = CalSudokuV1.sudokuGen(sudo)                      # 调用数独生成函数，把字符串转换成二维列表型数独
    answer = CalSudokuV1.CalSudoku(sudo)                    # 调用计算函数，生成的解存入 answer 变量
    for j in range(len(answer)):                            # 把答案中的每一行写入到答案文件
        fileAnswer.writelines(str(answer[j]) + "\n")
    fileAnswer.writelines("\n")                             # 每个答案之间空一行
    count += 1                                              # 统计题目个数
fileAnswer.close()                                          # 关闭答案文件
print("Number of question:{}, Total time:{:.4f}s`".format(count, perf_counter() - t))  # 输出总用时
