# Rakshika-Ai Project Documentation

## Table of Contents
1. Abstract ........................................... Page 1
2. Acknowledgement ................................... Page 2
3. Introduction ...................................... Page 2
4. Scope and Objectives .............................. Page 4
5. Project Description ................................ Page 6
   - Existing System .................................. Page 6
   - Proposed System ................................. Page 7
6. Technology Used ................................... Page 9
7. Design Phase ...................................... Page 10
   - ER Diagram ...................................... Page 11
   - Activity Diagram ............................... Page 12
   - Use Case Diagram ............................... Page 12
   - Class Diagram ................................... Page 13
8. Data Dictionary .................................... Page 14
9. Implementation of Project ........................ Page 15
10. Test Cases ........................................ Page 19
11. Conclusion ........................................ Page 21
12. Future Enhancement ............................... Page 22
13. References ........................................ Page 23
14. Group Log Sheet ................................... Page 24

---

## 1. Abstract

Rakshika-Ai is a web-based women safety analytics platform designed to transform complex crime records into actionable insights. Built with Streamlit for the frontend and Flask for the backend, the system processes district-level crime datasets and converts them into interactive dashboards, maps, and risk indicators.

This application helps users visualize trends across states, compare districts, and calculate safety scores for selected regions. It also includes a global chat feature that allows users to communicate and optionally share their current location in emergency situations. User authentication ensures that analytics and chat features are accessible only to authorized users.

By combining data analysis, visual storytelling, and community communication, Rakshika-Ai offers a practical tool to improve awareness of women’s safety issues and support better decision-making.

## 2. Acknowledgement

We would like to express our heartfelt gratitude to our project guide and mentors for their continuous guidance, constructive feedback, and encouragement throughout the project development journey. Their direction helped us refine our approach and keep the system focused on real-world user needs.

We are also grateful to our institution for providing the infrastructure, software tools, and learning environment needed to develop Rakshika-Ai. The support of our colleagues and peers has been invaluable during the design, implementation, and testing phases.

Finally, we acknowledge the contributions of the open-source community. Libraries such as Streamlit, Flask, Pandas, and Plotly made rapid development possible and provided a strong foundation for the application.

## 3. Introduction

Women’s safety data is often available through government publications, but raw crime statistics are not easy to interpret for most users. Rakshika-Ai addresses this problem by converting district-level crime data into meaningful visualizations and safety guidance.

The platform is built to help users understand safety patterns across Indian states and districts. It offers tools to analyze crime categories, compare locations, and evaluate safety risk based on historical data.

The application is especially useful for:
- Individuals seeking clarity on regional safety trends.
- Researchers analyzing women’s safety statistics.
- Authorities and NGOs looking for data-driven insights.

### 3.1 Background

National crime data is valuable for understanding long-term trends, but the information is usually published as CSV tables with many columns and values. This format makes it difficult for non-technical users to extract insights or compare regions.

### 3.2 Problem Statement

Existing crime reporting systems present several challenges:
- Users must manually download datasets and build their own charts.
- There are no easy filters to compare state and district results.
- Risk scoring is not available in a user-friendly format.
- Emergency contact information is not integrated with crime analytics.
- Communication channels are absent from existing analytics solutions.

### 3.3 Solution Overview

Rakshika-Ai provides a single platform that combines data analytics, interactive mapping, and community communication. The application reads district-level crime datasets, summarizes key metrics, and visualizes trends through charts and maps.

The solution also includes a global chat interface for conversation and support. When users choose to share their location, the system captures geolocation data and attaches it to chat messages securely.

## 4. Scope and Objectives

### 4.1 Scope

Rakshika-Ai is designed as a modular web application with the following scope:
- Authentication: A secure login/register system for users.
- Dashboard: Analytical pages that display crime summaries and charts.
- Risk Prediction: Visual risk scoring based on crime statistics.
- Safety Map: Geographic visualization of crime intensity.
- Chat: Global chat feature with optional location sharing.
- Helpline Directory: Emergency contact information by state.
- Data Persistence: SQLite database to store users and chat messages.
- Theming and UI: Consistent Streamlit-based interface across pages.

### 4.2 Objectives

Primary objectives:
- Make district-level crime data easy to understand for end users.
- Provide insights on high-risk areas and trends in women’s safety.
- Offer a chat feature for community discussion and emergency communication.
- Present safety metrics in an accessible, visual format.

Secondary objectives:
- Implement secure user authentication and password hashing.
- Use a lightweight Flask backend for API support.
- Allow optional encryption of sensitive chat data.
- Keep the architecture flexible so new features can be added later.

## 5. Project Description

### 5.1 Existing System

In the existing state, crime datasets are typically shared as raw CSV files or spreadsheets. Users who want to analyze these files must:
- Download multiple datasets from government portals.
- Use spreadsheet software or custom scripts to filter data.
- Build charts manually to compare crime categories.
- Manually search for emergency contact details.

This process is time-consuming and inaccessible to many users. It also makes it difficult to derive quick insights about safety levels or to correlate crime data with geographic regions.

### 5.2 Proposed System

Rakshika-Ai replaces the manual workflow with an integrated analytics application. The proposed system:
- Loads district-level crime data from CSV files.
- Automatically computes total crimes and category-specific summaries.
- Displays dashboards with interactive charts for crime categories and trends.
- Calculates risk scores based on total crimes and national averages.
- Visualizes state-level crime intensity using maps and top district cards.
- Provides a chat interface for sharing concerns and emergency information.
- Stores user data and chat history securely in a local database.

### 5.3 Advantages Over Existing Systems

The new system offers several advantages:
- Automation: Crime analytics are computed automatically after dataset selection.
- Visual clarity: Charts, maps, and cards make insights easier to understand.
- User engagement: The chat feature encourages community interaction.
- Security: Protected login and optional message encryption.
- Accessibility: The Streamlit frontend creates a simple web app experience.
- Reusability: The system can be extended to additional datasets and features.

## 6. Technology Used

### 6.1 Frontend Technologies
- Streamlit: Used for building the application pages and rendering data visualizations quickly.
- Plotly: Provides interactive graphs, maps, and gauge visuals for the dashboard.
- HTML/CSS: Adds custom styling for metric cards, chat bubbles, and page layouts.

### 6.2 Backend Technologies
- Flask: Serves APIs for authentication, chat messaging, and location capture.
- Flask-CORS: Enables communication between the Streamlit frontend and Flask backend.
- SQLite: Stores user profiles, message history, and optional encrypted data.
- Python: Handles data loading, processing, and business logic.

### 6.3 Data Handling
- Pandas: Loads CSV files, filters data, and computes summary statistics.
- NumPy: Supports numerical aggregation and statistical calculations.

### 6.4 Security
- Werkzeug: Securely hashes passwords before storing them in the database.
- Cryptography Fernet: Provides optional encryption for chat content and location data.

### 6.5 Development Tools
- Python 3.x: The primary programming language for both frontend and backend.
- Git: Used for version control and project collaboration.
- Streamlit: Tested locally for frontend development and deployment.

## 7. Design Phase

### 7.1 ER Diagram

The database design includes two primary tables:
- `users`: Stores registered user credentials and display names.
- `messages`: Captures global chat entries, geolocation data, emergency status, and timestamps.

This design enables a one-to-many relationship: each user can send multiple messages, while message records remain linked to the sender.

### 7.2 Activity Diagram

The application workflow is organized around the following steps:
1. The user opens the app and either logs in or registers.
2. Once authenticated, the user navigates to a page: Dashboard, Dataset, Risk Prediction, Safety Map, Chat, or About.
3. The frontend loads crime data from CSV files and renders the selected view.
4. The user interacts with filters, selects regions, and views charts.
5. In the chat page, the user can send messages and choose to share location.
6. The backend records messages and returns chat history to the client.

### 7.3 Use Case Diagram

Major use cases supported by the system include:
- Register new users and authenticate existing users.
- Load district-level crime datasets from the `data` folder.
- Filter crime data by year, state, and district.
- Display analytical dashboards and map visualizations.
- Compute safety risk levels for selected regions.
- Enable users to send messages and emergency information.
- Capture and optionally store geolocation details when permitted.

### 7.4 Class Diagram

The project architecture includes the following components:
- `Backend.app.create_app()`: Creates a Flask application, enables CORS, and registers blueprints.
- `Backend.routes.auth`: Implements API endpoints for registering, logging in, and logging out users.
- `Backend.routes.chat_routes`: Implements endpoints for retrieving messages, sending messages, cleaning up old messages, and capturing location.
- `Backend.db`: Manages SQLite connection details, table initialization, and query execution.
- `Backend.models.message_model.Message`: Handles reading, writing, encrypting, decrypting, and deleting chat messages.
- `Frontend.pages`: Represents individual Streamlit pages that render the UI and call backend APIs.

## 8. Data Dictionary

### 8.1 Crime Dataset Columns
- `STATE/UT`: The state or union territory associated with the crime records.
- `DISTRICT`: The district name.
- `Year`: The year of the crime data.
- `Rape`: Total rape cases reported in the district/year.
- `Kidnapping and Abduction`: Total kidnapping and abduction cases.
- `Dowry Deaths`: Number of dowry-related deaths.
- `Assault on women with intent to outrage her modesty`: Number of assault cases.
- `Insult to modesty of Women`: Cases involving insult to modesty.
- `Cruelty by Husband or his Relatives`: Number of cruelty cases.
- `Importation of Girls`: Number of importation cases.
- `Total Crimes`: Calculated sum of the major crime categories used for risk scoring.

### 8.2 Backend Database Tables

#### `users`
- `id` (INTEGER): Auto-incremented primary key.
- `username` (TEXT): Unique login name for each user.
- `name` (TEXT): Full name provided during registration.
- `password_hash` (TEXT): Hashed password value stored securely.

#### `messages`
- `id` (INTEGER): Auto-incremented primary key.
- `username` (TEXT): Name of the message sender.
- `message` (TEXT): Stored chat text, optionally encrypted.
- `location` (TEXT): Optional geolocation string saved when users share location.
- `emergency` (INTEGER): Boolean indicator for emergency messages (0 or 1).
- `timestamp` (DATETIME): Message creation datetime.

## 9. Implementation of Project

### 9.1 Development Environment Setup

The development environment is simple and easy to configure. Required components include Python 3.x, Streamlit, Flask, and SQLite. All backend dependencies are listed in `Backend/requirements.txt`.

Steps to set up the project:
1. Clone the repository to the local machine.
2. Create a Python virtual environment and activate it.
3. Install the backend requirements with `pip install -r Backend/requirements.txt`.
4. Start the backend by running `python Backend/app.py`.
5. Launch the frontend with `streamlit run Frontend/app.py`.

### 9.2 Backend Implementation

The backend is implemented using Flask and focuses on authentication and chat support.

Detailed backend components:
- `Backend/app.py`: Initializes the Flask app, enables CORS for `/api/*`, registers blueprints, and provides a health check endpoint at `/api/health`.
- `Backend/routes/auth.py`: Implements `/api/register`, `/api/login`, and `/api/logout` endpoints. This module uses Werkzeug to hash passwords and validate login credentials.
- `Backend/routes/chat_routes.py`: Implements chat-related endpoints:
  - `/api/global-chat/messages` to retrieve stored messages.
  - `/api/global-chat/send` to save new messages.
  - `/api/global-chat/cleanup` to delete messages older than a specified number of days.
  - `/api/location` to capture browser geolocation and redirect the user back to the frontend.
- `Backend/db.py`: Contains helper functions for connecting to SQLite, creating tables, and executing queries.
- `Backend/models/message_model.py`: Manages message storage and retrieval, including optional encryption and decryption of chat text and locations.

### 9.3 Frontend Implementation

The frontend is built as a Streamlit app with multiple pages, each focused on a specific feature.

Detailed frontend pages:
- `Frontend/app.py`: Configures the Streamlit page, applies the global theme, and initializes session state variables such as `logged_in`.
- `Frontend/pages/1_login.py`: Displays a login form and sends credentials to `/api/login`. Upon success, it updates the session state.
- `Frontend/pages/8_Register.py`: Displays a registration form and sends the new user data to `/api/register`.
- `Frontend/pages/2_dashboard.py`: Loads CSV files from `Frontend/data`, offers dataset selection, and renders key metrics and charts.
- `Frontend/pages/3_Dataset.py`: Allows users to explore dataset contents and preview the selected crime data.
- `Frontend/pages/4_Risk_Prediction.py`: Calculates a safety risk score based on selected filters, total crimes, and national averages, and displays the result with a gauge chart.
- `Frontend/pages/5_Safety_Map.py`: Shows state-level crime intensity, district summaries, and helpline contacts.
- `Frontend/pages/6_GlobalChat.py`: Provides a chat interface with styled message bubbles, emergency tagging, location sharing, and message history.
- `Frontend/pages/7_About.py`: Describes the project objectives, features, and usage instructions.

### 9.4 Feature Implementation

Key features implemented in Rakshika-Ai include:
- Secure user registration and login to protect analytics and chat access.
- Crime dataset exploration and dashboard analytics.
- Interactive filtering by year, state, and district.
- Risk prediction based on historical crime totals and averages.
- State-level crime intensity maps and district ranking cards.
- Global chat with optional emergency location sharing.
- Emergency helpline details for selected states.

### 9.5 Security Implementation

Security is built into the system through the following mechanisms:
- Passwords are hashed before storage using Werkzeug.
- API endpoints validate request data and return meaningful error responses.
- Streamlit pages are protected by session state checks to ensure users must log in first.
- Optional message encryption is available using Cryptography Fernet, ensuring stored chat text and location data can remain confidential.

## 10. Test Cases

### 10.1 Functional Test Cases
1. Register a new user with valid name, username, and password.
2. Prevent user registration when required fields are missing.
3. Reject duplicate usernames during registration.
4. Authenticate users using valid credentials.
5. Reject invalid usernames or passwords during login.
6. Restrict access to analytics pages for unauthenticated users.
7. Load and display dataset summaries for valid CSV files.
8. Filter datasets by year, state, and district correctly.
9. Calculate risk scores for selected regions and display appropriate risk levels.
10. Render safety map visualizations and top district summaries.
11. Display emergency helpline contacts for the selected state.
12. Send and retrieve chat messages through the backend API.
13. Persist location information when users choose to share it.
14. Delete old chat messages using the cleanup endpoint.
15. Display warnings and fallback messages when the dataset is missing or incomplete.

### 10.2 Non-functional Test Cases
1. Verify that the backend health endpoint returns a successful status.
2. Ensure the app launches successfully when required datasets exist.
3. Confirm that login and registration requests complete quickly.
4. Check that the Streamlit UI clearly warns users who are not logged in.
5. Verify the chat interface remains responsive with many messages.

### 10.3 Security Test Cases
1. Confirm that passwords are stored as hashed strings, not plain text.
2. Verify that protected pages are inaccessible without login.
3. Ensure that location sharing only happens after explicit user consent.
4. Test message encryption and decryption when the encryption key is configured.

## 11. Conclusion

Rakshika-Ai successfully combines crime data analytics, visual risk assessment, and community communication into a single platform. It simplifies the process of understanding district-level women’s safety information and provides tools for users to make better decisions.

This project demonstrates how modern web tools can convert raw data into visual insights, while also offering secure user access and support for emergency communication.

## 12. Future Enhancement

Future enhancements may include:
- Real-time crime data integration from official sources.
- Token-based authentication and role-based access control.
- A mobile-friendly layout or dedicated mobile app.
- Support for multiple languages to improve accessibility.
- Incident reporting and alert notification features.
- Machine learning models for advanced predictive safety scoring.

## 13. References

- National Crime Records Bureau datasets.
- Streamlit documentation and tutorials.
- Flask and Flask-CORS documentation.
- Pandas and Plotly documentation.
- SQLite documentation.
- Python documentation.

## 14. Group Log Sheet

| Sr. No | Name | Role | Hours Spent | Remarks |
|--------|------|------|-------------|---------|
| 1 | [Member 1] | Frontend / UI | [--] | UI design, Streamlit page development |
| 2 | [Member 2] | Backend / API | [--] | Flask API, database design, chat backend |
| 3 | [Member 3] | Data Analysis | [--] | Dataset processing, charts, risk scoring |
| 4 | [Member 4] | Testing & Documentation | [--] | Test planning, documentation, deployment support |

> Note: Replace placeholders with actual group member details and hours.
