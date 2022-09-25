from django.shortcuts import render
import pandas as pd
import numpy as np
import re


def find_table(x):
    x = re.split(",| ", x)
    arr = list()
    for i in x:
        if i.startswith("tbl"):
            arr.append(i)
    return arr


def type_query(x):
    x = x.split(",")
    arr = list()
    for i in x:
        ret = i.split(" ")[0]
        if ret.lower() == "into":
            arr.append(0)
        else:
            arr.append(1)
    return arr


def find_relevant(name):
    df = pd.read_csv("templates/static/" + name)
    df["type_user"] = df.loguser.apply(lambda x: 1 if x.startswith("etl") else 0)
    """
    Создание столбца table с массивом всех таблиц в запросе
    """
    df["table"] = df["query"].apply(find_table)
    """
    Создания столбца type_query с массивом типов запросов * 1- from, join ; 0 - into*
    """
    df["type_query"] = df["query"].apply(type_query)
    df.drop(columns=["rn", "query"], inplace=True)
    """
    Создане словаря с ключом - название таблицы;
                      заначение - масив 1 элемент - количестово выгрузок пользователями
                                        2 элемент - количество выгрузок программистами
                                        3 элемент - количество загрузок пользователем
                                        4 элемент - количество загрузок программистом
                                        5 элемент - количество выгрузок
                                        6 элемент - количество загрузок
    """
    dt = dict()
    for row in range(len(df)):
        for ind_table in range(len(df.iloc[row, 2])):
            table = df.iloc[row, 2][ind_table]
            if not table in dt:
                dt[table] = [0] * 6
            if df.iloc[row, 3][ind_table] == 0:
                dt[table][4] += 1
                if df.iloc[row, 1] == 1:
                    dt[table][0] += 1
                else:
                    dt[table][1] += 1
            elif df.iloc[row, 3][ind_table] == 1:
                dt[table][5] += 1
                if df.iloc[row, 1] == 1:
                    dt[table][2] += 1
                else:
                    dt[table][3] += 1
    table = list(dt.keys())
    count_down = list()
    count_select = list()
    count_down_etl = list()
    count_select_etl = list()
    count_down_dev = list()
    count_select_dev = list()
    for tb in dt:
        count_down.append(dt[tb][4])
        count_select.append(dt[tb][5])
        count_down_etl.append(dt[tb][0])
        count_select_etl.append(dt[tb][2])
        count_down_dev.append(dt[tb][1])
        count_select_dev.append(dt[tb][3])
    new_data = pd.DataFrame({"table": table,
                             "count_all_into": count_down,
                             "count_all_select": count_select,
                             "count_etl_into": count_down_etl,
                             "count_etl_select": count_select_etl,
                             "count_dev_into": count_down_dev,
                             "count_dev_select": count_select_dev})
    new_data[["count_all_into", "count_etl_into"]] = new_data[["count_all_into", "count_etl_into"]].apply(
        lambda x: x + 1 if x.count_etl_into == 0 else x, axis=1)
    q = new_data.count_dev_select.sum()
    qq = new_data.count_etl_into.sum()
    new_data["conv_etl"] = new_data.count_etl_into / qq
    new_data["conv_dev"] = new_data.count_dev_select / q
    new_data["relevant"] = new_data.conv_dev / new_data.conv_etl
    new_data = new_data.fillna(0)
    data = new_data.sort_values(by='relevant', ascending=False)
    new_csv = data[data["relevant"] != 0]
    new_csv["table"].to_csv("templates/static/" + name.split(".")[:-1] + "_new.csv")
    return data[["table", "count_etl_into", "count_dev_select", "conv_etl", "conv_dev", "relevant"]].iloc[
           :100].tolist(), data[["table", "count_etl_into", "count_dev_select", "conv_etl", "conv_dev",
                                 "relevant"]].iloc[-100:].tolist(), "templates/static/" + name.split(".")[
                                                                                          :-1] + "_new.csv", name.split(
        ".")[:-1] + "_new.csv"


def save_file(f):
    with open(f'templates/static/{f.name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def index(request):
    if request.POST:
        save_file(request.FILES.get("file"))
        table1, table2, new_csv, name = find_relevant(request.FILES.get("file").name)
        return render(request, 'index.html', {"table1": table1, "table2": table2, "new_file": new_csv, "name": name})
    else:
        return render(request, 'index.html')


def api(request):
    return render(request, 'api.html')
