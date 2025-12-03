# CS_461_program_2_Genetic_Algorithms
**Author:** Victor Olatunji  
**Semester:** Fall 2025  

📌 Project Overview

This project implements a complete Genetic Algorithm (GA) to generate an improved university course schedule.
Each "chromosome" in the population represents a full schedule assigning:

Rooms

Time slots

Facilitators

for 11 SLA activities.

The GA follows all required steps:

Representation of schedules

Custom fitness function with all rules implemented

Softmax selection

Single-point crossover

Mutation operator

Full evolutionary loop (500 generations)

Fitness metrics tracking (best, average, worst, improvement %)

Graph plotting (matplotlib)

Clean final output and best schedule reporting

The final GA produces a schedule with best fitness:
🎯 9.20

🧠 Key Features Implemented
✔ Complete Fitness Function

Includes:

Room size constraints

Facilitator preference scores

Room conflict penalties

Facilitator overload/underload logic

Facilitator double-booking penalties

Special SLA101/SLA191 sequencing rules

Cross-rules for building location penalties and spacing rewards

✔ Softmax Selection

The algorithm uses SciPy’s softmax to assign probabilistic selection weights:

Higher fitness → Higher probability of being selected as a parent.

✔ Crossover and Mutation

Single-point crossover using consistent ordering of activity keys

Mutation randomly reassigns room, time, facilitator

Adjustable mutation rate (default: 0.1)

✔ Evolution Loop (500 generations)

Each generation computes:

Best fitness

Average fitness

Worst fitness

Generation-to-generation improvement %

All metrics stored in arrays for plotting and reporting.

✔ Fitness Plot

A graph shows progression of:

Best fitness

Average fitness

Worst fitness

Saved as:

final_fitness_plot.png

📊 Final Performance Summary

Best Fitness: 9.20

Average Fitness: 9.04

Worst Fitness: 6.30

Improvement % across evolution: Flattened near the final generations, indicating convergence.

📁 Repository Structure
/
│ README.md
│ final_fitness_plot.png
│ schedule_ga.py        # main source code
│ /screenshots          # optional screen captures
│ /example_outputs      # best schedule, graph, logs

▶️ How to Run
Requirements
Python 3.9+
numpy
scipy
matplotlib


Install dependencies:

pip install numpy scipy matplotlib


Run the GA:

python schedule_ga.py


Output includes:

Full final report

Best schedule

Metrics summary

Saved plot

✨ Citations

This project was completed with conceptual assistance from:

ChatGPT (OpenAI, 2025)
Used to help structure code, debug logic, and improve documentation clarity.

The genetic algorithm principles adapted from standard GA references:

Holland, J. (1992). Adaptation in Natural and Artificial Systems.

Goldberg, D. (1989). Genetic Algorithms in Search, Optimization & Machine Learning.
