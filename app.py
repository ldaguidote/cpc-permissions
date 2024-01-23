import streamlit as st
import pandas as pd
import os
import time

# Import datasets
df = pd.read_csv('Permissions.csv')
valid_users =  pd.read_csv('Users.csv').users.to_list()

# Create folder for requesters
if not os.path.exists('requests'):
    os.mkdir('requests')

# Read the folder `requests` and get all requesters
requesters = [i[::-1][4:][::-1] for i in os.listdir('requests')]

st.title(':lock: Qlik QVD Permission Request')

name = st.text_input('Place your employee name here to search your existing QlikFile folder permissions')

if name not in valid_users and name == '':
    pass
    # st.info('Input your name in the box above') 

elif name not in valid_users and name != '':
    st.error('You are not a valid requester at this moment. Please contact DSAI for further instructions [laguidote@semirarampc.com]', icon="🚨")

else:
    if name != '' and name in requesters:
        st.warning('**You already have an ongoing request**', icon="⚠️")

        st.markdown('You have requested access to the following folders:')
        df_ongoing = pd.read_csv(f'requests/{name}.csv')
        st.dataframe(df_ongoing, use_container_width=True, hide_index=True)

        time.sleep(1)
        st.error('**WARNING:**\n\n You may do another request by clicking the button below, but this will delete your old request. '
                'After clicking the button below, the operation cannot be undone.', icon="🚨")

        time.sleep(2)
        if st.button('DO ANOTHER REQUEST', type='primary'):
            os.remove(f'requests/{name}.csv')
            st.rerun()

    elif name != '' and name not in requesters:
        st.subheader('')
        st.subheader(':unlock: Access List')
        st.markdown('You currently have access to the following QVD folders:')

        df_allowed = df.query(f'User == "{name}"').reset_index(drop=True)
        allowed_folders = df_allowed['Folder Name'].unique()
        st.dataframe(df_allowed, use_container_width=True, hide_index=True)


        st.subheader(':key: Request Access')
        st.markdown('You currently **DO NOT** have access to the following folders. Check the box to request access to this folder.')

        df_denied = pd.DataFrame()
        df_denied['Folder Name'] = [n for n in df['Folder Name'].unique() if n not in allowed_folders]
        df_denied['Access'] = False

        df_request = st.data_editor(
            df_denied,
            column_config={
                'Access': st.column_config.CheckboxColumn(
                    'Request Access?',
                    help='Check the box below if you want to gain access to the folder',
                )
            },
            disabled=['User', 'Folder Name', 'Permissions'],
            use_container_width=True,
            hide_index=True
        )

        requests_list = df_request.query('Access == True')['Folder Name'].values
        if len(requests_list) > 0:
            if st.button(':green[SUBMIT REQUEST]'):

                df_request.query('Access == True').to_csv(f'requests/{name}.csv', index=False)
                st.success(f'You have requested for the following: {", ".join(requests_list)}.')
