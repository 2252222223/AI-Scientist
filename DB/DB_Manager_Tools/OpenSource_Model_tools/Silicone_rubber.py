import torch
import torch.nn as nn
from sklearn import preprocessing
import pandas as pd
import numpy as np
from DB.DB_Manager_Tools.MIR_tools.Base.Data_loder import read_excel_data


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class Si_Rubber_LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers):
        super(Si_Rubber_LSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers=num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        predictions = self.linear(lstm_out)
        return predictions


def rubber_data_process(path):
    str_data = np.array(read_excel_data(path))
    expanded_array = np.tile(str_data, (50, 1))
    strain_to_add = np.arange(0, 50).reshape(-1, 1)
    result_array = np.hstack((expanded_array, strain_to_add))
    data = read_excel_data("./3D_printed_rubber.xlsx")
    scaler = preprocessing.StandardScaler().fit(data.iloc[:,:-1])
    data_tra = scaler.transform(result_array)
    x = torch.from_numpy(data_tra.astype(np.float32))
    return x


def rubber_stress_strain_predict(path):
    multi_layer_lstm_net = Si_Rubber_LSTM(input_size=6, hidden_size=50, output_size=1, num_layers=3)
    path = './LSTM_best.pth'
    chickpoint = torch.load(path)
    multi_layer_lstm_net.load_state_dict(chickpoint["state_dict"])
    multi_layer_lstm_net.to(device)

    x = rubber_data_process(path)
    x = x.to(device)
    output = multi_layer_lstm_net(x)
    y_pre = output.cpu()
    y_pre = y_pre.data.numpy()
    pd.DataFrame(y_pre.reshape(-1)).to_csv("./pre_strain_stress.csv",index=False)
    return "./pre_strain_stress.csv"