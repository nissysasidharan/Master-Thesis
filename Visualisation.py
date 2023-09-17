import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("data/Assessment/Assessment_Demography")

# Create a bar chart for age distribution
plt.figure(figsize=(10, 6))
plt.bar(df['USERNAME'], df['AGE'], color='skyblue')
plt.xlabel('Username')
plt.ylabel('Age')
plt.title('Age Distribution of Participants')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Create a pie chart for gender distribution
gender_counts = df['GENDER'].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=['lightcoral', 'lightblue'])
plt.title('Gender Distribution of Participants')
plt.tight_layout()
plt.show()

# Create a bar chart for education levels
education_counts = df['EDUCATION'].value_counts()
plt.figure(figsize=(8, 6))
plt.bar(education_counts.index, education_counts.values, color='lightgreen')
plt.xlabel('Education Level')
plt.ylabel('Count')
plt.title('Education Level Distribution of Participants')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Create a bar chart for familiarity with mental health chatbots
familiarity_counts = df['MENTAL HEALTH CHATBOTS'].value_counts()
plt.figure(figsize=(8, 6))
plt.bar(familiarity_counts.index, familiarity_counts.values, color='lightcoral')
plt.xlabel('Familiarity with Mental Health Chatbots')
plt.ylabel('Count')
plt.title('Familiarity with Mental Health Chatbots Among Participants')
plt.tight_layout()
plt.show()

# Create a bar chart for grouping
group_counts = df['GROUP'].value_counts()
plt.figure(figsize=(6, 6))
plt.bar(group_counts.index, group_counts.values, color='lightblue')
plt.xlabel('Group')
plt.ylabel('Count')
plt.title('Distribution of Participants in Different Groups')
plt.tight_layout()
plt.show()
