import streamlit as st
import pandas as pd
from plots.barchart_utils import predict_and_plot_lists
from RAG.chatbot import get_answer 
from auth import login_form, logout_button





def main():
    """
    Main function to structure the Streamlit app with a sidebar chatbot and main page dashboard.
    """


    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login_form()
        return  # Skip rest of app if not logged in

    
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
        # input_container = st.empty()

        # Place the input field in the container
        if prompt := st.chat_input("Ask me about the dashboard?"):
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

    predict_and_plot_lists(Loan,Asset_Mgmt,None,pccp_lable,"Loan","Asset Management",None)





if __name__ == "__main__":
    main()
    