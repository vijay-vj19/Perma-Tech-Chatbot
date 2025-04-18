import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import altair as alt

def predict_and_plot_lists(data_list1, data_list2, data_list3=None, x_labels=None, y_label1="Values1", y_label2="Values2", y_label3="Values3"):
    """Predicts and plots two or three lists using st.altair_chart with dual y-axis and custom y-axis labels, with automatic offset."""

    if not data_list1 or not data_list2:
        st.write("One or both of the first two lists are empty.")
        return

    values1 = np.array(data_list1)
    values2 = np.array(data_list2)

    if np.isnan(values1).any() or not np.issubdtype(values1.dtype, np.number):
        st.write("Invalid data in the first list (NaN or non-numerical).")
        return

    if np.isnan(values2).any() or not np.issubdtype(values2.dtype, np.number):
        st.write("Invalid data in the second list (NaN or non-numerical).")
        return

    X1 = np.array(range(len(values1))).reshape(-1, 1)
    y1 = values1

    model1 = LinearRegression()
    model1.fit(X1, y1)

    next_X1 = np.array([[len(values1)]])
    predicted_value1 = model1.predict(next_X1)[0]

    X2 = np.array(range(len(values2))).reshape(-1, 1)
    y2 = values2

    model2 = LinearRegression()
    model2.fit(X2, y2)

    next_X2 = np.array([[len(values2)]])
    predicted_value2 = model2.predict(next_X2)[0]

    if x_labels is None:
        labels = list(range(len(values1))) + ["Predicted 2023 Q2"]
    else:
        labels = x_labels + ["Predicted 2023 Q2"]

    data1 = np.append(values1, predicted_value1)
    data2 = np.append(values2, predicted_value2)

    # Create a DataFrame for Altair
    df = pd.DataFrame({
        "Data Points": labels,
        y_label1: data1,
        y_label2: data2
    })

    # Automatically calculate offset for y2
    offset_y2 = (max(data1) - min(data1)) * 0.1  # 10% of the range of data1
    df['offset_y2'] = df[y_label2] + offset_y2

    # Create the Altair chart with dual y-axis
    bar_chart = alt.Chart(df).mark_bar().encode(
        x="Data Points:O",
        y=f"{y_label1}:Q",
        color=alt.condition(
            alt.datum["Data Points"] == "Predicted 2023 Q2",
            alt.value("#e74c3c"),
            alt.value("#3498db")
        )
    )

    line_chart1 = alt.Chart(df).mark_line(color="orange").encode(
        x="Data Points:O",
        y=alt.Y('offset_y2:Q', axis=alt.Axis(title=f"{y_label2} (Secondary Axis)", titleColor="orange"))
    )

    layered_chart = alt.layer(bar_chart, line_chart1).resolve_scale(y='independent')

    if data_list3 is not None:
        values3 = np.array(data_list3)
        if np.isnan(values3).any() or not np.issubdtype(values3.dtype, np.number):
            st.write("Invalid data in the third list (NaN or non-numerical).")
            return

        X3 = np.array(range(len(values3))).reshape(-1, 1)
        y3 = values3

        model3 = LinearRegression()
        model3.fit(X3, y3)

        next_X3 = np.array([[len(values3)]])
        predicted_value3 = model3.predict(next_X3)[0]

        data3 = np.append(values3, predicted_value3)

        df[y_label3] = data3

        # Automatically calculate offset for y3
        offset_y3 = (max(data1) - min(data1)) * 0.2  # 20% of the range of data1
        df['offset_y3'] = df[y_label3] + offset_y3

        line_chart2 = alt.Chart(df).mark_line(color="green").encode(
            x="Data Points:O",
            y=alt.Y('offset_y3:Q', axis=alt.Axis(title=f"{y_label3} (Tertiary Axis)", titleColor="green"))
        )

        layered_chart = alt.layer(bar_chart, line_chart1, line_chart2).resolve_scale(y='independent')

    # Display the Altair chart in Streamlit
    st.altair_chart(layered_chart, use_container_width=True)