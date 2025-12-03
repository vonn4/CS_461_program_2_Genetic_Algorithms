# CS_461_program_2_Genetic_Algorithms
**Author:** Victor Olatunji  
**Semester:** Fall 2025  

---

## 📌 Project Overview

This project implements a **Genetic Algorithm (GA)** to automatically generate an optimized schedule for SLA-based course sections.  
The GA evaluates each candidate schedule using several real-world constraints — including room sizes, facilitator preferences, time conflicts, building proximity, and workload balancing.

Across hundreds of generations, the algorithm evolves increasingly optimal schedules through the application of:

- **Softmax-based selection**  
- **Single-point crossover**  
- **Random mutation**  
- **Comprehensive fitness scoring**  
- **Evolution tracking and graphing**

The final result includes:

1. The **best schedule found after 500 generations**  
2. The **best fitness score achieved**  
3. A generated **fitness plot** showing best/average/worst scores across generations  

---

## 🧠 How the Algorithm Works

### **1. Phase 1 — Schedule Representation**
Each schedule (chromosome) consists of assignments for all SLA classes:

- `room`
- `time`
- `facilitator`

Schedules are stored as Python dictionaries.  
The initial population contains **250 randomly generated schedules**, as required.

---

### **2. Phase 2 — Fitness Function**

The fitness function evaluates each schedule using several rules:

#### **Room Size Rules**
- Penalizes under-capacity rooms  
- Penalizes significantly oversized rooms  
- Rewards rooms that closely match course enrollment  

#### **Facilitator Preference Rules**
- Rewards preferred facilitators  
- Slight reward for acceptable facilitators  
- Penalizes unsuitable facilitators  

#### **Room Conflict Rules**
- Penalizes any two classes scheduled in the same room at the same time  

#### **Facilitator Load Rules**
- Penalizes double-booked facilitators  
- Penalizes facilitators teaching too many or too few courses  
- Special exception: *Tyler* has a slightly modified underload rule  

#### **SLA101 / SLA191 Special Rules**
- SLA101A & SLA101B must not be at the same time  
- SLA191A & SLA191B must not be at the same time  
- Rewards appropriate spacing  
- Rewards adjacency between SLA101 and SLA191 if buildings align  
- Penalizes adjacency across far-apart buildings  

Each of these rules contributes to the final fitness score.

---

## 🎯 Phase 3 — Selection (Softmax)

Fitness values are converted to probabilities using SciPy’s **softmax** function.  
This allows:

- Higher-fitness schedules → more likely to be chosen  
- Lower-fitness schedules → still possible to select (prevents premature convergence)

---

## 🔗 Phase 4 — Crossover

The algorithm performs **single-point crossover**, combining two parent schedules into two children:

- First part from Parent A  
- Second part from Parent B  

This encourages the mixing of strong traits between schedules.

---

## 🔄 Phase 5 — Mutation

A small percentage of schedules (10%) undergo mutation.  
One activity is randomly reassigned:

- a new room  
- a new time  
- and/or a new facilitator  

Mutation ensures diversity and prevents stagnation.

---

## 🚀 Phase 6 — Evolution Loop

The algorithm runs for **500 generations**, each time:

1. Evaluating population fitness  
2. Selecting parents  
3. Producing new children  
4. Applying crossover & mutation  
5. Replacing the population  
6. Tracking best/average/worst fitness  

At the end, the best chromosome and fitness history are returned.

---

## 📊 Phase 6.3 — Fitness Plot

Using Matplotlib, the algorithm generates:


The plot displays:

- **Green** — Best fitness  
- **Blue** — Average fitness  
- **Red** — Worst fitness  

The graph visually demonstrates convergence toward an optimal schedule.


📊 Performance Metrics Collected Each Generation

This genetic algorithm tracks the following metrics, as required by the project specification:

1. Best Fitness

The maximum fitness value within a generation — represents the strongest schedule found so far.

2. Average Fitness

The mean fitness across the entire population — indicates population health and diversity.

3. Worst Fitness

The lowest-performing schedule in the generation — useful for understanding algorithm spread.

4. Generation-to-Generation Improvement (%)

Measures how much better the best schedule becomes from one generation to the next:

Improvement
=
Best
(
𝑔
)
−
Best
(
𝑔
−
1
)
∣
Best
(
𝑔
−
1
)
∣
+
𝜖
×
100
Improvement=
∣Best(g−1)∣+ϵ
Best(g)−Best(g−1)
	​

×100

This metric shows:

Convergence rate

Whether evolution is stagnating

Whether mutation/crossover is still producing new improvements

All four metrics appear:

In the terminal output

Stored in history 

Visualized in the fitness plot

---

## ▶ How to Run the Program

### **Dependencies**

Install required packages:

### **Run the Full Program**


This will:

- Run the complete GA for 500 generations  
- Print the final optimized schedule  
- Save `final_fitness_plot.png`  

---

## 📘 Citations & References

This project draws concepts from:

- **Whitley, Darrell (1994).** *A Genetic Algorithm Tutorial.*  
- **Goldberg, David E. (1989).** *Genetic Algorithms in Search, Optimization, and Machine Learning.*  
- **SciPy Documentation:** https://docs.scipy.org  
- **NumPy Documentation:** https://numpy.org  
- **Matplotlib Documentation:** https://matplotlib.org  

### **AI Assistance Acknowledgment**
Portions of this project’s debugging, structural organization, and explanation text were developed with assistance from **ChatGPT (OpenAI, GPT-5.1)**.  
All algorithm logic, code design decisions, and final implementation were completed and reviewed by the author.

---

## 🏁 End of README
