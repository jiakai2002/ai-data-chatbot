# CSV Chatbot 🗂️🤖

A web application that allows users to upload CSV files and interact with the data using natural language. Built with Streamlit, LangChain, and OpenAI’s GPT-3.5, this tool enables users to ask questions about the data in their CSV files and receive intelligent responses.

<img width="1230" alt="Screenshot 2025-04-15 at 1 11 52 AM" src="https://github.com/user-attachments/assets/9f4d9170-c11c-4584-aab8-7ddd0b59c0b8" />

## Features

- **CSV File Upload**: Upload one or more CSV files to the app.
- **Data Preview**: Preview the first few rows of the selected CSV file.
- **Interactive Querying**: Ask natural language questions about the data and get responses powered by OpenAI’s GPT-3.5.
- **Query History**: Track and view a history of previous queries and their responses.
- **Session Management**: The app stores uploaded files and query history across sessions.

## Technologies Used

- **Streamlit**: For building the web interface.
- **LangChain**: For integrating OpenAI’s GPT-3.5 and creating the CSV agent.
- **OpenAI API**: To generate natural language responses based on the CSV data.
- **Pandas**: For handling and processing CSV data.
- **dotenv**: For securely loading environment variables.
- **Tempfile**: For temporarily saving uploaded CSV files.
