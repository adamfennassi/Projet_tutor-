from ortools.sat.python import cp_model

def solve_scheduling(tasks):
    """
    Résout un petit problème d'ordonnancement.
    :param tasks: liste de tuples (nom, durée)
    :return: durée totale optimale
    """
    model = cp_model.CpModel()

    # Variables : chaque tâche commence à un temps donné
    start_times = {}
    for i, (name, duration) in enumerate(tasks):
        start_times[name] = model.NewIntVar(0, 100, f'start_{name}')

    # Contrainte : pas de chevauchement (les tâches sont en série)
    for i in range(len(tasks) - 1):
        current, next_task = tasks[i], tasks[i + 1]
        model.Add(start_times[next_task[0]] >= start_times[current[0]] + current[1])

    # Objectif : minimiser le temps total
    last_task = tasks[-1]
    end_time = model.NewIntVar(0, 100, 'end_time')
    model.Add(end_time == start_times[last_task[0]] + last_task[1])
    model.Minimize(end_time)

    # Solveur
    solver = cp_model.CpSolver()
    solver.Solve(model)

    return solver.Value(end_time)
if __name__ == "__main__":
    tasks = [("A", 3), ("B", 5), ("C", 2)]
    result = solve_scheduling(tasks)
    print("Durée totale optimale :", result)
