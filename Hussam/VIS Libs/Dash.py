import panel as pn
import pandas as pd
import plotly.express as px

pn.extension('plotly')

# Sample Data
df = pd.DataFrame({
    "Category": ["A", "B", "C", "A", "B", "C"],
    "Values": [10, 15, 20, 25, 30, 35]
})

# Widget for filtering
category_filter = pn.widgets.Select(name="Category", options=list(df['Category'].unique()), value="A")

@pn.depends(category_filter)
def update_chart(selected_category):
    filtered_df = df[df['Category'] == selected_category]
    fig = px.bar(filtered_df, x='Category', y='Values', title=f'Category: {selected_category}')
    return pn.pane.Plotly(fig)

# Layout
dashboard = pn.Column(category_filter, update_chart)
dashboard.show()
