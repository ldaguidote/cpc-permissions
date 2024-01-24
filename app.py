import streamlit as st
import pandas as pd
import os
import time

# Import datasets
df = pd.read_csv('Permissions.csv')
valid_users = pd.read_csv('Users.csv').users.to_list()
valid_table = pd.read_csv('ValidTables.csv').valid_tables.to_list()

# Create folder for requesters
if not os.path.exists('requests'):
    os.mkdir('requests')

# Read the folder `requests` and get all requesters
requesters = [i[::-1][4:][::-1] for i in os.listdir('requests')]

st.title(':lock: Qlik QVD Permission Request')

st.markdown('Input your username below to search your existing QlikFile folder permissions')
name = st.text_input('To get your username, remove the domain from your email address. '
                     'For example, input `sngranado` if your email is `sngranado@semirarampc.com`.')

if name not in valid_users and name == '':
    pass

elif name not in valid_users and name != '':
    st.error('You are not a valid requester at this moment. '
             'Please contact DSAI for further instructions [laguidote@semirarampc.com]',
             icon="🚨")

else:
    if name != '':
        st.subheader('')
        st.subheader(':unlock: Access List')
        st.markdown('After February 9, you will only be able to create and modify files in the following folders:')

        df_allowed = df.query(f'User == "{name}"').drop_duplicates()
        allowed_folders = df_allowed['Folder Name'].unique()
        st.dataframe(df_allowed, use_container_width=True, hide_index=True)
