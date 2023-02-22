import os
import sys


step_string='Step: Main menu: - 5 - Get configuration list - Lists account name and project data'
print('')
print('Running '+step_string+'...')
print('Getting configuration list for project data: ')

os.system('gcloud config configurations list ')

step_string='Step: Main menu: - 10 - Get a list of all organizations'
print('')
print('Running '+step_string+'...')
print('Listing all organizations... ')

os.system('gcloud organizations list')
