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
    if name != '' and name in requesters:
        st.warning('**You already have an ongoing request**', icon="⚠️")
        st.subheader('')
        st.markdown('You have requested access to the following folders:')

        df_ongoing = pd.read_csv(f'requests/{name}.csv')
        st.dataframe(df_ongoing, use_container_width=True, hide_index=True)
        st.subheader('')

        time.sleep(2)
        st.error('**WARNING:**\n\n'
                 'You may do another request by clicking the button below, but this will delete your old request. '
                 'After clicking the button below, the operation cannot be undone.',
                 icon="🚨")

        time.sleep(2)
        if st.button('DO ANOTHER REQUEST', type='primary'):
            os.remove(f'requests/{name}.csv')
            st.rerun()

    elif name != '' and name not in requesters:
        st.subheader('')
        st.subheader(':unlock: Access List')
        st.markdown('You currently have access to the following QVD folders:')

        df_allowed = df.query(f'User == "{name}"').drop_duplicates()
        allowed_folders = df_allowed['Folder Name'].unique()
        st.dataframe(df_allowed, use_container_width=True, hide_index=True)

        st.subheader('')
        st.subheader(':key: Request Access')
        st.markdown('You currently **DO NOT** have access to the following folders. '
                    'Check the box to request access to this folder and indicate the reason for the request. '
                    'Note that the requests are subject to approval.')

        df_denied = pd.DataFrame()
        df_denied['Folder Name'] = [n for n in valid_table if n not in allowed_folders]
        df_denied['Access'] = False
        df_denied['Reason'] = ''

        df_request = st.data_editor(
            df_denied,
            column_config={
                'Access': st.column_config.CheckboxColumn(
                    'Request Access?',
                    help='Check the box below if you want to gain access to the folder',
                ),
                'Reason': st.column_config.TextColumn(
                    'Reason for Request',
                    help='Indicate the reason for the request'
                )
            },
            disabled=['Folder Name'],
            use_container_width=True,
            hide_index=True
        )

        requests_list = df_request.query('Access == True')['Folder Name'].values
        if len(requests_list) > 0:
            if st.button(':green[SUBMIT REQUEST]'):

                df_request.query('Access == True').to_csv(f'requests/{name}.csv', index=False)
                st.success(f'You have requested for the following: {", ".join(requests_list)}.')

        if name == 'laguidote':

            st.subheader('')
            st.subheader('Download Requests')
            to_download = pd.DataFrame()
            ongoing_requests_list = os.listdir('requests')
            for filename in ongoing_requests_list:
                username = filename[::-1][4:][::-1]
                file = pd.read_csv(f'requests/{filename}')
                file['user'] = username

                to_download = pd.concat([to_download, file], axis=0)

            to_download.to_csv(index=False)
            st.download_button('DOWNLOAD ALL REQUESTS',
                               to_download.to_csv(index=False),
                               'file.csv',
                               'text/csv')