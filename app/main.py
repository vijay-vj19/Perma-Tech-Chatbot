import streamlit as st
import pandas as pd
from app.plots.barchart_utils import predict_and_plot_lists, plot_prophet_forecast
from RAG.chatbot import get_answer


def main():
    """
    Main function to structure the Streamlit app with a sidebar chatbot and main page dashboard.
    """

    # Sidebar for Chatbot
    st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
    )
    # Sidebar for Chatbot
    with st.sidebar:
        st.header("Chatbot")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun (at the top)
        chat_container = st.container()

        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Create an empty container for the input field
        input_container = st.empty()

        # Place the input field in the container
        if prompt := input_container.chat_input("Ask me about the dashboard?"):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            response = get_answer(prompt)
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Force a re-render to ensure correct placement
            st.rerun()

    # Main page for Dashboard
    st.header("Dashboard")

    st.subheader("PCCP")

    #preprocessing data
    file_path = r"resources\Preprocessed.xlsx"
    sheet_name = "Portfolio Trend"

    df = pd.read_excel(file_path, sheet_name=sheet_name,header=None)

    #Dashboard starts here\

    st.markdown("<h3>Portfolio Trend</h3>", unsafe_allow_html=True)

    Loan = df.iloc[1][1:].tolist()
    UPB = df.iloc[2][1:].tolist()
    pccp_lable = df.iloc[0][1:].tolist()

    predict_and_plot_lists(UPB,Loan,None,pccp_lable,"UPB","Loan",None)

    st.markdown("<h3>Revenue Trend</h3>", unsafe_allow_html=True)
    Total_revenue = df.iloc[3][1:].tolist()
    Rev_Loan = df.iloc[4][1:].tolist()
    
    predict_and_plot_lists(Total_revenue,Rev_Loan,None,pccp_lable,"Total Revenue","Rev/Loan",None)

    st.markdown("<h3>Staffing Trend</h3>", unsafe_allow_html=True)
    Asset_Mgmt = df.iloc[5][1:].tolist()
    Portfolio_Mgmt = df.iloc[6][1:].tolist()

    predict_and_plot_lists(Loan,Asset_Mgmt,Portfolio_Mgmt,pccp_lable,"Loan","Asset Management","Portfolio Management")

    try:
        # Load Portfolio Trend sheet
        file_path = "resources/Preprocessed.xlsx"
        sheet_name = "Portfolio Trend"
        portfolio_data = pd.read_excel(file_path, sheet_name=sheet_name)

        # === Call the new Prophet function at the end ===
        plot_prophet_predictions(portfolio_data, pccp_lable)

    except Exception as e:
        st.error(f"An error occurred: {e}")


# Call Prophet Model
def plot_prophet_predictions(portfolio_data, pccp_lable):
    
    # Extract data for Prophet predictions
    loan_data = portfolio_data.loc[portfolio_data["Period"] == "Loan"].values.flatten()[1:]
    upb_data = portfolio_data.loc[portfolio_data["Period"] == "UPB"].values.flatten()[1:]
    total_revenue_data = portfolio_data.loc[portfolio_data["Period"] == "Total Revenue (excl. IOD)"].values.flatten()[1:]
    rev_loan_data = portfolio_data.loc[portfolio_data["Period"] == "Rev/Loan"].values.flatten()[1:]
    asset_mgmt_data = portfolio_data.loc[portfolio_data["Period"] == "Asset Mgmt"].values.flatten()[1:]
    portfolio_mgmt_data = portfolio_data.loc[portfolio_data["Period"] == "Portfolio Mgmt"].values.flatten()[1:]
    
    # Plot Prophet predictions
    st.subheader(" Prophet Forecast for Loan Count")
    plot_prophet_forecast(
    loan_data, upb_data, None, x_labels=pccp_lable,
    y_label1="Loan Count", y_label2="UPB Value", y_label3=None
)
    st.subheader(" Prophet Forecast for Total Revenue")
    plot_prophet_forecast(
    total_revenue_data, rev_loan_data, None, x_labels=pccp_lable,
    y_label1="Total Revenue", y_label2="Rev/Loan", y_label3=None
)    
    st.subheader(" Prophet Forecast for UPB")
    plot_prophet_forecast(
    upb_data, loan_data, None, x_labels=pccp_lable,
    y_label1="UPB Value", y_label2="Loan", y_label3=None
)


if __name__ == "__main__":
   main()
