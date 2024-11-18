import plotly.graph_objects as go

# Sample data
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# Create an interactive line chart
fig = go.Figure(go.Scatter(x=x, y=y, mode='lines+markers', name='Sample Line'))
fig.update_layout(title='Interactive Line Chart', xaxis_title='X-axis', yaxis_title='Y-axis')
fig.show()
