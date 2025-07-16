import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("🛒 Supermarket Sales Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("SuperMarket Analysis dataset.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Hour'] = pd.to_datetime(df['Time'], format='%I:%M:%S %p').dt.hour
    df['Day'] = df['Date'].dt.day_name()
    return df

df = load_data()
st.dataframe(df.head(10))

# Sidebar Filters
st.sidebar.header("Filter the Data:")

city = st.sidebar.multiselect(
    "Select City",
    options=df["City"].unique(),
    default=df["City"].unique()
)

gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

product_line = st.sidebar.multiselect(
    "Select Product Line",
    options=df["Product line"].unique(),
    default=df["Product line"].unique()
)

df_selection = df.query(
    "City == @city & Gender == @gender & `Product line` == @product_line"
)

# TOP KPI Cards
total_sales = int(df_selection["Sales"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
total_invoices = df_selection.shape[0]

left_col, middle_col, right_col = st.columns(3)

with left_col:
    st.subheader("Total Sales:")
    st.subheader(f"₹ {total_sales:,}")

with middle_col:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} ⭐")

with right_col:
    st.subheader("Total Invoices:")
    st.subheader(f"{total_invoices}")


st.markdown("---")  # Adds a line separator

st.subheader("Sales by Product Line")
product_sales = (
    df_selection.groupby("Product line")["Sales"]
    .sum()
    .sort_values(ascending=True)
)

fig, ax = plt.subplots()
ax.barh(product_sales.index, product_sales.values, color="skyblue")
ax.set_xlabel("Total Sales")
ax.set_ylabel("Product Line")
ax.set_title("Total Sales by Product Line")
st.pyplot(fig)


st.markdown("---")
st.subheader("Sales by Hour")

sales_by_hour = (
    df_selection.groupby("Hour")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Hour")
)

fig, ax = plt.subplots()
ax.plot(sales_by_hour["Hour"], sales_by_hour["Sales"], marker="o", color="orange")
ax.set_xticks(range(0, 24))
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("Total Sales")
ax.set_title("Total Sales by Hour")
plt.grid(True)

st.pyplot(fig)


st.subheader("Payment Method Distribution")
payment_counts = df_selection["Payment"].value_counts()

fig, ax = plt.subplots()
sns.barplot(x=payment_counts.index, y=payment_counts.values, ax=ax)
ax.set_ylabel("Count")
ax.set_xlabel("Payment Method")
ax.set_title("Payment Method Usage")
st.pyplot(fig)
