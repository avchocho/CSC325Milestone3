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

# 1. Line Chart: Growth of Disney Content Over Time 
fig1 = px.line(
    df1,
    x='Release Year',
    y='Number of Titles',
    title='Growth of Disney Content Over Time',
    markers=True
)
fig1.update_layout(
    height=700,     
    width=1000,
    title_x=0.5      
)
fig1.show()


# 2. Bar Chart: Top 10 Popular Genres 
# get the total titles per genre
genre_totals = df2.groupby('Genre')['Number of Titles'].sum().sort_values(ascending=False)

# filter to only the top 10 genres
top10_genres = genre_totals.head(10).index

# filter the df to only the top 10
df2_top10 = df2[df2['Genre'].isin(top10_genres)]

fig2 = px.bar(
    df2_top10,
    x='Genre',
    y='Number of Titles',
    color='Title Type',
    barmode='group',
    title='Top 10 Most Popular Genres on Disney+'
)
fig2.update_layout(
    xaxis_title='Genre',
    yaxis_title='Number of Titles',
    title_x=0.5,
    height=700,
    width=1000
)
fig2.show()

# 3. Pie Chart: Movies vs TV Shows 
fig3 = px.pie(
    df3,
    names='Type',
    values='Total',
    title='Movies vs TV Shows on Disney+'
)
fig3.update_layout(
    title_x=0.5,
    height=600
)
fig3.show()

# 4. Horizontal Bar Chart: Title Content From Each Country

# 5. Bar Chart: Top 10 Directors 