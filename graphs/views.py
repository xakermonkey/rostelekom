from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
# import tensorflow as tf
# from keras.models import load_model
# import neurokit2 as nk
# import numpy as np
# import pandas as pd
# from scipy.signal import find_peaks
# import os
# import json

# def get_data_from_file(df):
#     df.columns = [i.lower() for i in df.columns]
#     X1 = list()
#     X2 = list()
#     X3 = list()
#     ID = list()
#     for user, data_user in df.groupby("filename"):
#         for test, test_data in data_user.groupby(["test_index"]):
#             for repert, repert_data in test_data.groupby(["presentation"]):
#                 X_1 = list()
#                 X_2 = list()
#                 X_3 = list()
#                 for ind, question in enumerate(
#                         list(repert_data.question)):
#                     data = repert_data[repert_data["question"] == question]
#                     data_1 = np.array([int(i) * (-1) for i in list(data.data)[0][1:-1].split(", ")])
#                     data_2 = np.array([int(i) * (-1) for i in list(data.data_2)[0][1:-1].split(", ")])
#                     signals, info = nk.ppg_process(data_1, sampling_rate=20)
#                     X_1.append(data_1)
#                     X_2.append(data_2)
#                     X_3.append(np.array(list(signals.PPG_Rate)))
#                     ID.append([user, str(test), str(repert), str(question)])
#                 if len(X_1) == 0:
#                     continue
#                 X_1 = np.array(X_1).reshape((len(X_1) * 240,))
#                 X_2 = np.array(X_1).reshape((len(X_2) * 240,))
#                 X_3 = np.array(X_2).reshape((len(X_3) * 240,))
#                 X_1 = (X_1 - X_1.min()) / (X_1.max() - X_1.min())
#                 X_3 = (X_3 - X_3.min()) / (X_3.max() - X_3.min())
#                 X_2 = (X_2 - X_2.min()) / (X_2.max() - X_2.min())
#                 X1 += [X_1[i * 240:240 * (i + 1)] for i in range(X_1.shape[0] // 240)]
#                 X3 += [X_3[i * 240:240 * (i + 1)] for i in range(X_3.shape[0] // 240)]
#                 X2 += [X_2[i * 240:240 * (i + 1)] for i in range(X_2.shape[0] // 240)]
#     X1 = np.array(X1)
#     X2 = np.array(X2)
#     X3 = np.array(X3)
#     return X1, X2, X3, ID

def index(request):
    return render(request, 'index.html', )


def api(request):
    return render(request, 'api.html')
