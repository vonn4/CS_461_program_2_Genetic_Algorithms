# ==============================================================
# CS 461 — Program 2
# Genetic Algorithm for Scheduling
# ==============================================================


# ==============================================================
# PHASE 1 — PROBLEM SETUP
# --------------------------------------------------------------
# 1.1 Facilitators, Rooms, Times, Activities
# 1.2 Schedule Representation
# 1.3 Initial Population Generation
# ==============================================================

from scipy.special import softmax
import numpy as np
import random
import matplotlib.pyplot as plt

# ---------- Facilitators ----------
FACILITATORS = [
    "Lock", "Glen", "Banks", "Richards", "Shaw",
    "Singer", "Uther", "Tyler", "Numen", "Zeldin"
]

# ---------- Rooms + Capacity ----------
ROOMS = {
    "Beach 201": 18,
    "Beach 301": 25,
    "Frank 119": 95,
    "Loft 206": 55,
    "Loft 310": 48,
    "James 325": 110,
    "Roman 201": 40,
    "Roman 216": 80,
    "Slater 003": 32
}

# ---------- Time Slots ----------
TIMES = ["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]

# ---------- Activities ----------
ACTIVITIES = {
    "SLA101A": {
        "enrollment": 40,
        "preferred": ["Glen", "Lock", "Banks"],
        "other": ["Numen", "Richards", "Shaw", "Singer"]
    },
    "SLA101B": {
        "enrollment": 35,
        "preferred": ["Glen", "Lock", "Banks"],
        "other": ["Numen", "Richards", "Shaw", "Singer"]
    },
    "SLA191A": {
        "enrollment": 45,
        "preferred": ["Glen", "Lock", "Banks"],
        "other": ["Numen", "Richards", "Shaw", "Singer"]
    },
    "SLA191B": {
        "enrollment": 40,
        "preferred": ["Glen", "Lock", "Banks"],
        "other": ["Numen", "Richards", "Shaw", "Singer"]
    },
    "SLA201": {
        "enrollment": 60,
        "preferred": ["Glen", "Banks", "Zeldin", "Lock", "Singer"],
        "other": ["Richards", "Uther", "Shaw"]
    },
    "SLA291": {
        "enrollment": 50,
        "preferred": ["Glen", "Banks", "Zeldin", "Lock", "Singer"],
        "other": ["Richards", "Uther", "Shaw"]
    },
    "SLA303": {
        "enrollment": 25,
        "preferred": ["Glen", "Zeldin"],
        "other": ["Banks"]
    },
    "SLA304": {
        "enrollment": 20,
        "preferred": ["Singer", "Uther"],
        "other": ["Richards"]
    },
    "SLA394": {
        "enrollment": 15,
        "preferred": ["Tyler", "Singer"],
        "other": ["Richards", "Zeldin"]
    },
    "SLA449": {
        "enrollment": 30,
        "preferred": ["Tyler", "Zeldin", "Uther"],
        "other": ["Zeldin", "Shaw"]
    },
    "SLA451": {
        "enrollment": 90,
        "preferred": ["Lock", "Banks", "Zeldin"],
        "other": ["Tyler", "Singer", "Shaw", "Glen"]
    }
}

# Ordered list for consistent crossover
ACTIVITY_KEYS = list(ACTIVITIES.keys())



# ==============================================================
# PHASE 1.2 — Schedule Representation
# ==============================================================

def generate_random_schedule():
    """Creates a random schedule mapping each activity to a room, time, and facilitator."""
    schedule = {}
    for activity in ACTIVITIES.keys():
        schedule[activity] = {
            "room": random.choice(list(ROOMS.keys())),
            "time": random.choice(TIMES),
            "facilitator": random.choice(FACILITATORS)
        }
    return schedule


def print_schedule(schedule):
    """Prints a schedule in a clean, readable format."""
    print("\nRandomly Generated Schedule:")
    print("-" * 40)
    for activity, assignment in schedule.items():
        print(f"{activity}: Room={assignment['room']}, "
              f"Time={assignment['time']}, "
              f"Facilitator={assignment['facilitator']}")
    print("-" * 40)



# ==============================================================
# PHASE 1.3 — Initial Population Generation
# ==============================================================

def generate_initial_population(size=250):
    """Generates the initial population of schedules."""
    return [generate_random_schedule() for _ in range(size)]



# ==============================================================
# PHASE 2 — FITNESS FUNCTION
# ==============================================================

def compute_fitness(schedule):
    """
    Computes the fitness for a schedule using:
    - Room size matching
    - Facilitator preferences
    - Room conflicts
    - Facilitator conflicts + workload fairness
    - SLA101 / SLA191 special spacing rules
    """
    fitness = 0.0

    # ------------------------------------
    # Room size + facilitator preference scoring
    # ------------------------------------
    for activity, assign in schedule.items():
        room = assign["room"]
        cap = ROOMS[room]
        need = ACTIVITIES[activity]["enrollment"]

        # Room size scoring
        if cap < need:
            fitness -= 0.5
        elif cap > 3 * need:
            fitness -= 0.4
        elif cap > 1.5 * need:
            fitness -= 0.2
        else:
            fitness += 0.3

        # Facilitator preference
        fac = assign["facilitator"]
        pref = ACTIVITIES[activity]["preferred"]
        other = ACTIVITIES[activity]["other"]

        if fac in pref:
            fitness += 0.5
        elif fac in other:
            fitness += 0.2
        else:
            fitness -= 0.1

    # ------------------------------------
    # Room conflicts
    # ------------------------------------
    room_time_counts = {}
    for act, assign in schedule.items():
        key = (assign["room"], assign["time"])
        room_time_counts[key] = room_time_counts.get(key, 0) + 1

    for act, assign in schedule.items():
        if room_time_counts[(assign["room"], assign["time"])] > 1:
            fitness -= 0.5

    # ------------------------------------
    # Facilitator conflicts + loads
    # ------------------------------------
    fac_total = {}
    fac_time = {}

    for act, assign in schedule.items():
        f = assign["facilitator"]
        t = assign["time"]

        fac_total[f] = fac_total.get(f, 0) + 1
        fac_time[(f, t)] = fac_time.get((f, t), 0) + 1

    # Time overlap penalty
    for (f, t), count in fac_time.items():
        if count > 1:
            fitness -= 0.2 * count

    # Workload fairness
    for f, total in fac_total.items():
        if total > 4:
            fitness -= 0.5
        elif total < 3:
            if f == "Tyler":
                if total < 2:
                    fitness -= 0.4
            else:
                fitness -= 0.4

    # ------------------------------------
    # SLA101 / SLA191 Special Rules
    # ------------------------------------
    time_map = {"10 AM": 10, "11 AM": 11, "12 PM": 12, "1 PM": 13, "2 PM": 14, "3 PM": 15}

    def t(a): return time_map[schedule[a]["time"]]
    def b(a): return schedule[a]["room"].split()[0]

    # Block 1 — 101A vs 101B
    if t("SLA101A") == t("SLA101B"):
        fitness -= 0.5
    if abs(t("SLA101A") - t("SLA101B")) > 4:
        fitness += 0.5

    # Block 2 — 191A vs 191B
    if t("SLA191A") == t("SLA191B"):
        fitness -= 0.5
    if abs(t("SLA191A") - t("SLA191B")) > 4:
        fitness += 0.5

    # Cross rules
    for x, y in [
        ("SLA101A", "SLA191A"),
        ("SLA101A", "SLA191B"),
        ("SLA101B", "SLA191A"),
        ("SLA101B", "SLA191B"),
    ]:
        diff = abs(t(x) - t(y))
        if diff == 0:
            fitness -= 0.25
        elif diff == 1:
            fitness += 0.5
            if (b(x) in {"Roman", "Beach"}) ^ (b(y) in {"Roman", "Beach"}):
                fitness -= 0.4
        elif diff == 2:
            fitness += 0.25

    return fitness



# ==============================================================
# PHASE 3 — SOFTMAX SELECTION
# ==============================================================

def compute_population_fitness(population):
    return [compute_fitness(ch) for ch in population]


def softmax_selection(population, fitness_values):
    return softmax(fitness_values)


def pick_two_parents(population, probs):
    i, j = np.random.choice(len(population), size=2, replace=False, p=probs)
    return population[i], population[j]



# ==============================================================
# PHASE 4 — CROSSOVER
# ==============================================================

def crossover(p1, p2):
    point = random.randint(1, len(ACTIVITY_KEYS) - 2)
    c1, c2 = {}, {}
    for i, act in enumerate(ACTIVITY_KEYS):
        if i < point:
            c1[act] = p1[act]
            c2[act] = p2[act]
        else:
            c1[act] = p2[act]
            c2[act] = p1[act]
    return c1, c2



# ==============================================================
# PHASE 5 — MUTATION
# ==============================================================

def mutate(ch, rate=0.1):
    if random.random() < rate:
        act = random.choice(ACTIVITY_KEYS)
        ch[act] = {
            "room": random.choice(list(ROOMS.keys())),
            "time": random.choice(TIMES),
            "facilitator": random.choice(FACILITATORS)
        }
    return ch



# ==============================================================
# PHASE 6 — EVOLUTION ENGINE
# --------------------------------------------------------------
# 6.1 Create Next Generation
# 6.2 Run Full Evolution Loop
# ==============================================================

def create_next_generation(pop, mutation_rate=0.1):
    new_pop = []
    fits = compute_population_fitness(pop)
    probs = softmax_selection(pop, fits)

    while len(new_pop) < len(pop):
        p1, p2 = pick_two_parents(pop, probs)
        c1, c2 = crossover(p1, p2)
        new_pop.append(mutate(c1, mutation_rate))
        if len(new_pop) < len(pop):
            new_pop.append(mutate(c2, mutation_rate))

    return new_pop


def run_evolution(generations=500, population_size=250, mutation_rate=0.1):
    population = generate_initial_population(population_size)

    best_hist, avg_hist, worst_hist = [], [], []
    best_ch, best_fit = None, float("-inf")

    for g in range(generations):
        fits = compute_population_fitness(population)
        best_hist.append(max(fits))
        avg_hist.append(sum(fits) / len(fits))
        worst_hist.append(min(fits))

        if max(fits) > best_fit:
            best_fit = max(fits)
            best_ch = population[fits.index(best_fit)]

        population = create_next_generation(population, mutation_rate)

    return best_ch, best_fit, {
        "best": best_hist,
        "avg": avg_hist,
        "worst": worst_hist
    }



# ==============================================================
# PHASE 6.3 — FITNESS PLOTTING
# ==============================================================

def plot_fitness(history, filename="fitness_plot.png"):
    gens = range(len(history["best"]))

    plt.figure(figsize=(10, 6))
    plt.plot(gens, history["best"], label="Best Fitness", color="green")
    plt.plot(gens, history["avg"], label="Average Fitness", color="blue")
    plt.plot(gens, history["worst"], label="Worst Fitness", color="red")

    plt.title("Genetic Algorithm Fitness Over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Fitness Score")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Fitness plot saved as: {filename}")



# ==============================================================
# PHASE 7 — FINAL EXECUTION BLOCK
# ==============================================================

if __name__ == "__main__":
    print("Running full genetic algorithm...")
    print("This may take a moment...\n")

    best_schedule, best_score, history = run_evolution(
        generations=500,
        population_size=250,
        mutation_rate=0.1
    )

    plot_filename = "final_fitness_plot.png"
    plot_fitness(history, filename=plot_filename)

    print("\n====================================")
    print("       FINAL GENETIC ALGORITHM RESULTS")
    print("====================================")
    print(f"Best Fitness After 500 Generations: {best_score}\n")

    print("Best Schedule Produced:\n")
    print_schedule(best_schedule)

    print(f"\nFitness plot saved as: {plot_filename}")
    print("Execution complete.")
