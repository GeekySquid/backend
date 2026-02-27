# app/services/lstm_service.py

import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from app.core.config import settings

SEQUENCE_LENGTH = settings.SEQUENCE_LENGTH


class LSTMModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=50, batch_first=True)
        self.fc = nn.Linear(50, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out


def load_lstm_model():
    model = LSTMModel()
    model.load_state_dict(torch.load("app/models/lstm_model.pth"))
    model.eval()
    return model


def predict_price(model, df):
    scaler = MinMaxScaler()
    close_prices = df["close"].values.reshape(-1, 1)
    scaled = scaler.fit_transform(close_prices)

    last_sequence = scaled[-SEQUENCE_LENGTH:]
    last_sequence = np.reshape(last_sequence, (1, SEQUENCE_LENGTH, 1))

    input_tensor = torch.FloatTensor(last_sequence)

    with torch.no_grad():
        prediction = model(input_tensor)

    predicted_price = scaler.inverse_transform(
        prediction.numpy()
    )[0][0]

    return float(predicted_price)