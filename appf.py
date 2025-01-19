import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


st.set_page_config(page_title="STUDENT MENTAL HEALTH DASHBOARD",layout="wide")
# Title of the app
st.title("Student Mental Health Dashboard")

# Load the dataset
data = pd.read_csv("Student Mental health.csv")

# Section 1:Overview
st.subheader("Overview")
col1, col2 = st.columns(2)

with col1:
    total_participants = len(data)  
    st.metric(label="Total Participants", value=total_participants)

with col2:
    age_range = f"{data['age'].min()} - {data['age'].max()}"  
    st.metric(label="Age Range", value=age_range)

# Section 2: (Demographics
st.subheader("Demographics")
col3, col4 = st.columns(2)

# Pie Chart for Gender Distribution
with col3:
    gender_distribution = data["gender"].value_counts(normalize=True) * 100  # Calculate percentage distribution
    fig1, ax1 = plt.subplots()
    ax1.pie(
        gender_distribution,
        labels=gender_distribution.index,
        autopct="%1.1f%%",
        colors=plt.cm.Pastel1.colors
    )
    ax1.set_title("Gender Distribution")
    st.pyplot(fig1)

# Bar Chart for Marital Status
with col4:
    marital_status_counts = data["marital_status"].value_counts()  # Count the occurrences
    fig2, ax2 = plt.subplots()
    ax2.bar(
        marital_status_counts.index,
        marital_status_counts.values,
        color=plt.cm.Paired.colors
    )
    ax2.set_title("Marital Status")
    ax2.set_ylabel("Count")
    ax2.set_xlabel("Marital Status")
    st.pyplot(fig2)

# Sidebar Filters
st.sidebar.header("Please filter here")

# Gender filter
selected_genders = st.sidebar.multiselect(
    "Select Gender:",
    options=data["gender"].unique(),
    default=data["gender"].unique()  
)

# Year of study filter
selected_years = st.sidebar.multiselect(
    "Select Year of Study:",
    options=data["year_of_study"].unique(),
    default=data["year_of_study"].unique()  
)

# Apply the selected filters to the data
filtered_data = data[
    (data["gender"].isin(selected_genders)) & 
    (data["year_of_study"].isin(selected_years))
]

# Section 3: Effect of CGPA on Mental Health (filtered data only)
st.subheader("Effect of CGPA on Mental Health")

# Function to plot bar chart for each condition (for filtered data)
def plot_cgpa_condition(cgpa_column, condition_column, title):
    
    condition_counts = filtered_data.groupby([cgpa_column, condition_column]).size().unstack(fill_value=0)
    
    # Plot the bar chart
    fig, ax = plt.subplots()
    condition_counts.plot(kind='bar', ax=ax, color=['lightblue', 'orange'])
    ax.set_title(title)
    ax.set_xlabel("CGPA")
    ax.set_ylabel("Count of Participants")
    st.pyplot(fig)

# Bar Chart for CGPA vs Depression (filtered data)
col7, col8 = st.columns(2)

with col7:
    plot_cgpa_condition("CGPA", "depression", "CGPA vs Depression")

# Bar Chart for CGPA vs Anxiety 
with col8:
    plot_cgpa_condition("CGPA", "anxiety", "CGPA vs Anxiety")

# Bar Chart for CGPA vs Panic Attack (filtered data)
with st.container():
    plot_cgpa_condition("CGPA", "panic_attack", "CGPA vs Panic Attack")

# Section 5: Bar chart for Seeking Professional Help (filtered data only)
st.subheader("Number of People Who Sought Professional Help")

# Did you seek any specialist for a treatment?
help_counts_filtered = filtered_data["Did you seek any specialist for a treatment?"].value_counts()

# Plot the bar chart for filtered data
fig6, ax6 = plt.subplots()
help_counts_filtered.plot(kind='bar', color=['lightgreen', 'salmon'])
ax6.set_title("People Who Sought Professional Help")
ax6.set_xlabel("Response (Yes/No)")
ax6.set_ylabel("Count of Participants")
ax6.set_xticklabels(["No", "Yes"], rotation=0)
st.pyplot(fig6)



