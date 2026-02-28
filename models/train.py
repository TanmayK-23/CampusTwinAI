import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pickle

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.ml.torch_models import CrowdMLP, EquipmentMLP

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(MODEL_DIR), "data")

zone_mapping = {"Library": 0, "Gate3": 1, "Cafeteria": 2, "HostelArea": 3, "MainBlock": 4}

def train_crowd():
    print("Training Crowd Model...")
    df = pd.read_csv(os.path.join(DATA_DIR, "crowd_data.csv"))
    
    # Feature engineering
    df['zone_idx'] = df['zone_id'].map(zone_mapping)
    features = ['zone_idx', 'hour_of_day', 'day_of_week', 'event_flag', 'weather_flag']
    target = 'density'
    
    X = torch.tensor(df[features].values, dtype=torch.float32)
    y = torch.tensor(df[target].values, dtype=torch.float32).view(-1, 1)
    
    dataset = TensorDataset(X, y)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    model = CrowdMLP(input_size=len(features))
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    
    epochs = 50
    for epoch in range(epochs):
        for bx, by in loader:
            optimizer.zero_grad()
            pred = model(bx)
            loss = criterion(pred, by)
            loss.backward()
            optimizer.step()
            
    torch.save(model.state_dict(), os.path.join(MODEL_DIR, "crowd_mlp.pt"))
    print("Saved crowd_mlp.pt")

def train_equipment():
    print("Training Equipment Model...")
    df = pd.read_csv(os.path.join(DATA_DIR, "equipment_data.csv"))
    
    features = ['usage_hours', 'avg_temperature', 'maintenance_history', 'age_days']
    target = 'failure_probability'
    
    # Normalize inputs for stable training (save scalers for inference)
    means = df[features].mean()
    stds = df[features].std()
    
    df[features] = (df[features] - means) / stds
    
    with open(os.path.join(MODEL_DIR, "equipment_scaler.pkl"), "wb") as f:
        pickle.dump({"means": means, "stds": stds}, f)
        
    X = torch.tensor(df[features].values, dtype=torch.float32)
    y = torch.tensor(df[target].values, dtype=torch.float32).view(-1, 1)
    
    dataset = TensorDataset(X, y)
    loader = DataLoader(dataset, batch_size=16, shuffle=True)
    
    model = EquipmentMLP(input_size=len(features))
    criterion = nn.BCELoss() # Binary Cross Entropy since target is probability
    optimizer = optim.Adam(model.parameters(), lr=0.005)
    
    epochs = 100
    for epoch in range(epochs):
        for bx, by in loader:
            optimizer.zero_grad()
            pred = model(bx)
            loss = criterion(pred, by)
            loss.backward()
            optimizer.step()
            
    torch.save(model.state_dict(), os.path.join(MODEL_DIR, "equipment_mlp.pt"))
    print("Saved equipment_mlp.pt")

if __name__ == "__main__":
    train_crowd()
    train_equipment()
