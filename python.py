import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the CSV file
df = pd.read_csv("data.csv")

# Step 2: Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Step 3: Plot the data
plt.figure(figsize=(10, 6))  # Set figure size
plt.plot(df['Date'], df['Sales'], marker='o', linestyle='-', color='green')  # Line plot

# Step 4: Add titles and labels
plt.title('Monthly Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.grid(True)  # Add grid lines for readability

# Step 5: Display the plot
plt.tight_layout()  # Adjust layout
plt.show()
