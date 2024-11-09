import altair as alt
import pandas as pd

# Sample data
data = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [2, 3, 5, 7, 11]})

# Create an interactive line chart
chart = alt.Chart(data).mark_line(point=True).encode(
    x='x',
    y='y'
).properties(title="Interactive Line Chart")

chart.show()
