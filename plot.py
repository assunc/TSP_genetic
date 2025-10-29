import subprocess
import time
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Measure start time
start_time = time.time()

# Step 2: Run the optimization program
# Ensure r0123456.py is in the same directory and generates r0123456.csv
subprocess.run(["python3", "r0123456.py"])

# Step 3: Measure end time
end_time = time.time()
execution_time = end_time - start_time
print(f"Total runtime of r0123456.py: {execution_time:.2f} seconds")

# Step 4: Load and clean the resulting CSV file
file_path = 'r0123456.csv'
cols = ['Iteration', 'ElapsedTime', 'MeanObjective', 'BestObjective']
df = pd.read_csv(file_path, usecols=[0, 1, 2, 3], names=cols, header=None)

# Convert columns to numeric and drop invalid rows
df = df[pd.to_numeric(df['MeanObjective'], errors='coerce').notnull()]
df = df[pd.to_numeric(df['BestObjective'], errors='coerce').notnull()]
df['Iteration'] = pd.to_numeric(df['Iteration'])
df['MeanObjective'] = pd.to_numeric(df['MeanObjective'])
df['BestObjective'] = pd.to_numeric(df['BestObjective'])

# Step 5: Plot convergence graph
plt.figure(figsize=(10, 6))
plt.plot(df['Iteration'], df['MeanObjective'], label='Mean Objective', color='blue')
plt.plot(df['Iteration'], df['BestObjective'], label='Best Objective', color='green')

plt.title('Convergence Graph')
plt.xlabel('Iteration')
plt.ylabel('Objective Value')
plt.legend()
plt.grid(True)

# Add runtime text inside the graph
plt.text(0.05, 0.95, f"Runtime: {execution_time:.2f} seconds",
         transform=plt.gca().transAxes,
         fontsize=10, verticalalignment='top',
         bbox=dict(facecolor='white', alpha=0.6))

plt.tight_layout()
plt.savefig('convergence_graph_with_runtime.png')
plt.show()