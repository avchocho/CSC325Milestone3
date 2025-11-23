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

# V2 line chart 
query1 = """
SELECT release_year as 'Release Year', COUNT(*) AS 'Number of Titles' 
FROM `Show` 
GROUP BY release_year 
ORDER BY release_year;
"""
df1 = pd.read_sql(query1, conn)

# V2 bar chart
query2 = """
SELECT gname AS Genre, show_type AS 'Title Type', COUNT(*) AS 'Number of Titles'
FROM `Show` s, ShowGenre sg, Genre g
WHERE s.show_id = sg.showID AND g.id = sg.genre_id
GROUP BY gname, show_type
ORDER BY COUNT(*) DESC
"""
df2 = pd.read_sql(query2, conn)

# V3 pie chart
query3 = """
SELECT show_type AS Type, COUNT(*) AS 'Total'
FROM `Show` 
GROUP BY show_type;
"""
df3 = pd.read_sql(query3, conn)

# V4 horizontal bar chart 

# V5 bar chart

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
