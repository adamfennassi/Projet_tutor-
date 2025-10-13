import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from ppc_solver import solve_scheduling

# --- Modèle simple ---
class SchedulePredictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(3, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )

    def forward(self, x):
        return self.fc(x)

# --- Génération de données ---
def generate_data(n_samples=200):
    X, y = [], []
    for _ in range(n_samples):
        durations = np.random.randint(1, 10, 3)
        tasks = [("A", int(durations[0])), ("B", int(durations[1])), ("C", int(durations[2]))]
        total = solve_scheduling(tasks)
        X.append(durations)
        y.append(total)
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32).reshape(-1, 1)

# --- Entraînement ---
def train_model():
    X, y = generate_data(100)
    model = SchedulePredictor()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    for epoch in range(100):
        inputs = torch.tensor(X)
        targets = torch.tensor(y)
        outputs = model(inputs)
        loss = criterion(outputs, targets)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    torch.save(model.state_dict(), "../data/model.pth")
    print("✅ Modèle entraîné et sauvegardé.")
    return model
if __name__ == "__main__":
    train_model()
