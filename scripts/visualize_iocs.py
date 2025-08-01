import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Load timeline
df = pd.read_csv('reports/timeline.csv')

# Clean and parse timestamps
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
df.dropna(subset=['Timestamp'], inplace=True)

# Define event types
def get_event_type(desc):
    if "Accepted password" in desc:
        return "LOGIN_SUCCESS"
    elif "Failed password" in desc:
        return "LOGIN_FAIL"
    elif "invalid user" in desc:
        return "INVALID_USER"
    else:
        return "OTHER"

df['Event'] = df['Description'].apply(get_event_type)

# Set timestamp as index for resampling
df.set_index('Timestamp', inplace=True)

# Resample every 5 minutes (use '5min' instead of deprecated '5T')
resampled = df.groupby('Event').resample('5min')['Event'].count().unstack(fill_value=0).stack().reset_index(name='Count')

# Plot
plt.figure(figsize=(12, 6))
sns.lineplot(data=resampled, x='Timestamp', y='Count', hue='Event', marker='o')
plt.title("SSH Events Over Time")
plt.xlabel("Time")
plt.ylabel("Count")
plt.grid(True)
plt.tight_layout()
plt.show()

