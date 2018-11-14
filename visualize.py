# libraries and data
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

def visualize(file):
    data = open(file).read()

    lineData = data.split("\n")
    allData = []

    for row in lineData:
        allData.append(row.split("\t"))

    dates = []
    totalRecommend = 0

    for row in allData:
        totalRecommend += int(row[2]) + int(row[3])

        if(len(dates) > 0 and row[1] not in dates):
            dates = dates.append(str(row[1]))

    print(totalRecommend)

# visualize("data/양진호_2018-10-30_2018-11-08.tsv")

