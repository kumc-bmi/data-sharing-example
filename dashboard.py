from q_db import *
from q_one import product
from q_four import smod, smod_count
from q_five import employees_count

pts = alt.selection(type="single", encodings=['x'])

rect = alt.Chart(product).mark_rect().encode(
    alt.X('product_count:Q', bin=True),
    alt.Y('product_sum:Q', bin=True),
    alt.Color('count()',
        scale=alt.Scale(scheme='yellowgreen'),
        legend=alt.Legend(title='Total Products')
    )
).properties(
    width=600,
    height=200
)

circ = rect.mark_point().encode(
    alt.ColorValue('grey'),
    alt.Size('count()',
        legend=alt.Legend(title='Product in Selection')
    )
).transform_filter(
    pts
)

bar_one = alt.Chart(product).mark_bar().encode(
    x='most_popular:N',
    y='max(product_count)',
    color=alt.condition(pts, alt.ColorValue("lightskyblue"), alt.ColorValue("lightgrey"))
).properties(
    width=600,
    height=300
).add_selection(pts)

bar_two = alt.Chart(product).mark_bar().encode(
    x='country:N',
    y='max(product_count)',
    color=alt.condition(pts, alt.ColorValue("lightskyblue"), alt.ColorValue("lightgrey"))
).properties(
    width=600,
    height=300
).add_selection(pts)

one = alt.vconcat(
    rect + circ,
    bar_one,
    bar_two
).resolve_legend(
    color="independent",
    size="independent"
)

smo = smod
smo.index = pd.RangeIndex(smod_count.iloc[0]['count'], name = 'x')
smo = pd.DataFrame({'ship_id' : smo.ship_id, 'company_name' : smo.company_name, 'shipping_time' : smo.shipping_time})
smo = smo.reset_index().melt('x', var_name='shipper', value_name='y')

# Create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['x'], empty='none')

# The basic line
line = alt.Chart(smo).mark_line(interpolate='basis').encode(
    x='x:Q',
    y='y:Q',
    color='shipper:N'
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = alt.Chart(smo).mark_point().encode(
    x='x:Q',
    opacity=alt.value(0),
).add_selection(
    nearest
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'y:Q', alt.value(' '))
)

# Draw a rule at the location of the selection
rules = alt.Chart(smo).mark_rule(color='gray').encode(
    x='x:Q',
).transform_filter(
    nearest
)

# Put the five layers into a chart and bind the data
four = alt.layer(
    line, selectors, points, rules, text
).properties(
    width=600, height=300
)

brush = alt.selection(type='interval')

points = alt.Chart(employees_count).mark_point().encode(
    x='employee_id:Q',
    y='total_dollar_sales:Q',
    color=alt.condition(brush, 'last_name:N', alt.value('lightgray'))
).add_selection(
    brush
).properties(
    width=300,
    height=300
)

bars = alt.Chart(employees_count).mark_bar().encode(
    y='last_name:N',
    color='last_name:N',
    x='max(total_dollar_sales):Q'
).transform_filter(
    brush
).properties(
    width=300,
    height=300
)

five = points | bars

all_chart = alt.vconcat(one, four, five)

all_chart_html = all_chart.to_json()