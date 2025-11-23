#https://plotly.com/python/v3/graph-data-from-mysql-database-in-python/

import pandas as pd
import plotly.express as px
import os
import pymysql

# -----------------------------
# 1. Connect to AWS
# -----------------------------
def make_connection():
    return pymysql.connect(
        host="csc325termproject-db.cjww46guy0g5.us-east-2.rds.amazonaws.com",
        port=3306,                                       # MySQL default port
        user="admin",
        password="Milestone2",
        database="disneyplus_db" 
    )


# -----------------------------
# 2. Fetch data from MySQL
# -----------------------------
conn = make_connection()
query = "SELECT Name, Continent, Population, LifeExpectancy, GNP FROM country"
df = pd.read_sql(query, conn)
conn.close()

# -----------------------------
# 3. Plotly Express Charts
# -----------------------------

# 1. Scatter Plot: GNP vs Life Expectancy
fig1 = px.scatter(
    df,
    x='GNP',
    y='LifeExpectancy',
    hover_data=['Name', 'Continent'],
    title='GNP vs Life Expectancy',
    color='Continent'
)
fig1.show()

# 2. Bar Chart: Population by Continent
continent_pop = df.groupby('Continent')['Population'].sum().reset_index()
fig2 = px.bar(
    continent_pop,
    x='Continent',
    y='Population',
    title='Population by Continent',
    color='Continent'
)
fig2.show()

# 3. Histogram: Life Expectancy Distribution
fig3 = px.histogram(
    df,
    x='LifeExpectancy',
    nbins=20,
    title='Life Expectancy Distribution',
    color='Continent'
)
fig3.show()
