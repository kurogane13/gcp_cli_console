import os
import sys


step_string='Step: Main menu: - 1 - Retrieve billing data for default project: byoid-ui-testing-project'
print('')
print('Running '+step_string+'...')
byoid_ui_testing_project='byoid-ui-testing-project'
print('Retrieving billing data for project name: '+byoid_ui_testing_project)
os.system('gcloud beta billing projects describe '+byoid_ui_testing_project)

step_string='Step: Main menu: - 3 - Describe project byoid-ui-testing-project'
print('')
print('Running '+step_string+'...')

project_name='byoid-ui-testing-project'
print('Describing project: '+project_name)
os.system('gcloud projects describe '+project_name)

step_string='Step: Main menu: - 10 - Get a list of all organizations'
print('')
print('Running '+step_string+'...')
print('Listing all organizations... ')

os.system('gcloud organizations list')

step_string='Step: Main menu: - 5 - Get configuration list - Lists account name and project data'
print('')
print('Running '+step_string+'...')
print('Getting configuration list for project data: ')

os.system('gcloud config configurations list ')
