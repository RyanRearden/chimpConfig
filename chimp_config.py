import pandas as pd

# Reads the csv list
df = pd.read_csv('members_list.csv',
                 usecols=['id',
                          'email',
                          'name_of_school_leader_principal_head',
                          'name_of_teacher_s',
                          'name_of_parent_homeschool_coop_latin_teacher',
                          'email_of_school_leader_principal_head',
                          'email_of_teacher_s',
                          'email_of_parent_homeschool_coop_latin_teacher',
                          'firstname',
                          'lastname',
                          'username'])

#combines the first and last name
df["Full Name"] = df['firstname'] + " " + df['lastname']

#Checks if a name doesn't exist for the user. If not, it makes the user name the name 
all_null = df[['firstname', 'lastname', 'name_of_school_leader_principal_head', 'name_of_teacher_s', 'name_of_parent_homeschool_coop_latin_teacher']].isnull().all(axis=1)
df.loc[all_null, 'Full Name'] = df.loc[all_null, 'username']


df_list = df[['id', 
              'Full Name',
                'email', 
                'name_of_parent_homeschool_coop_latin_teacher',
                  'email_of_parent_homeschool_coop_latin_teacher', 
                  'name_of_school_leader_principal_head', 
                  'email_of_school_leader_principal_head',
                  'name_of_teacher_s',
                  'email_of_teacher_s']].copy()

#df_homeschoolNormalSchool = pd.merge(df_homeschoolNormal, df_school, on='id')

#df_list['name_of_teacher_s'] = df['name_of_teacher_s'].str.split('\n')
#df_list['email_of_teacher_s'] = df['email_of_teacher_s'].str.split('\n')
#df_list = df_list.explode(['name_of_teacher_s', 'email_of_teacher_s']).reset_index(drop=True)

#checks if the email and homeschool email are the same. If it is, it deletes the homeschool email
df_list.loc[df_list['email'] == df_list['email_of_parent_homeschool_coop_latin_teacher'], 'email_of_parent_homeschool_coop_latin_teacher'] = None

df_list['Full Name'] = df_list['Full Name'].fillna(df_list['name_of_parent_homeschool_coop_latin_teacher'])
df_list.drop('name_of_parent_homeschool_coop_latin_teacher', axis=1, inplace=True)

df_list.loc[(df_list['Full Name'].isnull()) | (df_list['Full Name'] == df_list['name_of_school_leader_principal_head']), 'Full Name'] = df_list['name_of_school_leader_principal_head']
df_list.drop('name_of_school_leader_principal_head', axis=1, inplace=True)

df_list.loc[df_list['email_of_teacher_s'] == df_list['email'], ['name_of_teacher_s', 'email_of_teacher_s']] = ''
df_list.loc[df_list['email_of_school_leader_principal_head'] == df_list['email'], ['email_of_school_leader_principal_head']] = ''

# Replace NaN values with empty strings in the columns
df_list['email'].fillna('', inplace=True)
df_list['email_of_school_leader_principal_head'].fillna('', inplace=True)
df_list['email_of_teacher_s'].fillna('', inplace=True)
df_list['email_of_parent_homeschool_coop_latin_teacher'].fillna('', inplace=True)
df_list['Full Name'].fillna('', inplace=True)
df_list['name_of_teacher_s'].fillna('', inplace=True)

# Combine columns under 'email' with line breaks
df_list['email'] = df_list['email'] + '\n' + df_list['email_of_school_leader_principal_head'] + '\n' + df_list['email_of_teacher_s'] + '\n' + df_list['email_of_parent_homeschool_coop_latin_teacher']

# Combine columns under 'Full Name' with line breaks
df_list['Full Name'] = df_list['Full Name'] + '\n' + df_list['name_of_teacher_s']

df_list.drop(['name_of_teacher_s', 'email_of_school_leader_principal_head', 'email_of_teacher_s', 'email_of_parent_homeschool_coop_latin_teacher'], axis=1, inplace=True)

#df_list['Full Name'] = df['Full Name'].str.split('\n')
#df_list['email'] = df['email'].str.split(',')
#df_list = df_list.explode(['Full Name', 'email']).reset_index(drop=True)

df_list.sort_values(by = 'id', inplace=True)
df_list.to_csv('compiledMemberList.csv', index=False)