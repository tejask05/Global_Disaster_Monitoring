import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import exceptions

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


cred = credentials.Certificate("YOUR JSON FILE PATH HERE")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

def main():
    st.title(':green[Welcome to Geospatial Visualization for Disaster Monitoring]')  # Use st.title for large font title
    

    def send_email(email):
        email_sender  = 'YOUR EMAIL HERE'
        email_password = 'YOUR PASSWORD HERE'
        email_receiver = email
        subject = "Welcome to Geo-Spatial Visualization for Disaster Monitoring"

        # Create a message with HTML content
        msg = MIMEMultipart('alternative')
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = subject

        # Plain text version (optional)
        text_part = MIMEText("Plain text version of the email", 'plain')  # Corrected constructor call
        msg.attach(text_part)
        

        # HTML version with bold formatting and larger headings
        html_part = MIMEText(f"""
        <html>
        <head>
          <style>
            h2 {{
              font-size: 20px;  /* Adjust as desired for headings */
              font-weight: bold;
            }}
          </style>
        </head>
        <body>
          <p>Dear User,</p>
          <p>Thank you for signing up for Geo-Spatial Visualization for Disaster Monitoring! We're thrilled to welcome you to our platform.</p>
          <p><b>Geo-Spatial Visualization for Disaster Monitoring</b> is a cutting-edge web application designed to monitor and visualize disasters in real-time by analyzing news articles. Our mission is to provide a comprehensive overview of ongoing and past disaster events, empowering users with valuable insights and actionable information.</p>

          <h2><b>Key Features:</b></h2>
          <ol>
            <li><b>Interactive Map Visualization:</b> Explore the geographical distribution of disaster events on our interactive map powered by Folium.</li>
            <li><b>Advanced Filtering Options:</b> Customize your experience by filtering disaster events based on type and date range using intuitive sidebar widgets.</li>
            <li><b>Insights and Analytics:</b> Gain valuable insights into disaster events through interactive visualizations, including charts, word clouds, and event counts over time.</li>
            <li><b>Key Events Marquee:</b> Stay informed about recent key events with our scrolling marquee in the sidebar, complete with clickable links for more information.</li>
            <li><b>Dynamic Updates:</b> Our application dynamically updates visualizations and data in real-time based on user-selected filters, ensuring you always have access to the latest information.</li>
          </ol>
          Explore our GitHub Repository for more details: <a href="https://github.com/ARYANRVIMPADAPU/GeoNews">Link to GitHub</a>

          <p>If you have any questions, feedback, or suggestions, please don't hesitate to reach out to us. We're here to support you every step of the way.</p>

          <p>Best regards,</p>
          <p>The Geo-Spatial Visualization for Disaster Monitoring Team</p>
        </body>
        </html>
        """, 'html')
        msg.attach(html_part)

        # Set Content-Type header for HTML rendering
        msg['Content-Type'] = "text/html"

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, msg.as_string())


    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def f():
        try:
            user = auth.get_user_by_email(email)
            st.success("Login Successful")

            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.signedout = True
            st.session_state.signout = True

        except exceptions.InvalidArgumentError as e:
            st.error("Invalid email address. Please enter a valid email address.")

        except:
            st.error("Login Failed")

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False 
        st.session_state.username = ''
        st.session_state.useremail = ''
    
    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False

    if not st.session_state['signedout']:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign Up'])

        if choice == 'Login':
            email = st.text_input('Email Address')
            password = st.text_input('Password', type='password')
            st.button('Login', on_click=f)
        else:
            email = st.text_input('Email Address')
            password = st.text_input('Password', type='password')
            username = st.text_input('Username')
            
            if st.button('Create my account'):
                if len(password) < 6:
                    st.error("Password must be at least 6 characters long.")
                    return  # Exit the function to prevent user creation with an invalid password
    
                try:
                    # Fetch all users
                    all_users = auth.list_users()

                    # Check if the UID already exists
                    for user in all_users.users:
                        if user.uid == username:
                            st.error("Username already exists. Please choose a different username.")
                            return

                    # If the username is unique, proceed with user creation
                    user = auth.create_user(email=email, password=password, uid=username)
                    st.success('Account created successfully! Login now to Explore...')
                    st.balloons()
                    send_email(email)
                except exceptions.InvalidArgumentError as e:
                    st.error("Invalid email address. Please enter a valid email address.")
    if st.session_state.signout:
        st.text('Name: ' + st.session_state.username)
        st.text('Email id: ' + st.session_state.useremail)
        st.button('Sign out', on_click=t)

