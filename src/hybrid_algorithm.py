import torch
import itertools
from ml_model import SchedulePredictor
from ppc_solver import solve_scheduling

def hybrid_schedule(tasks):
    model = SchedulePredictor()
    model.load_state_dict(torch.load("../data/model.pth"))
    model.eval()

    best_duration = float("inf")
    best_order = None

    # Tester plusieurs ordres et choisir celui avec la plus petite prédiction ML
    for perm in itertools.permutations(tasks):
        durations = [d for _, d in perm]
        input_tensor = torch.tensor([durations], dtype=torch.float32)
        predicted_time = model(input_tensor).item()

        if predicted_time < best_duration:
            best_duration = predicted_time
            best_order = perm

    # Une fois le meilleur ordre choisi, on lance le PPC
    optimal = solve_scheduling(best_order)
    return best_order, optimal

if __name__ == "__main__":
    tasks = [("A", 3), ("B", 5), ("C", 2)]
    order, total = hybrid_schedule(tasks)
    print("Ordre optimal prédit :", [t[0] for t in order])
    print("Durée totale réelle :", total)
