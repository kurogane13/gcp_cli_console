import os
import sys


step_string='Step: Main menu: - 9 - Get a list of all projects'
print('')
print('Running '+step_string+'...')
print('Listing all projects... ')

os.system('gcloud projects list')

step_string='Step: Main menu: - 10 - Get a list of all organizations'
print('')
print('Running '+step_string+'...')
print('Listing all organizations... ')

os.system('gcloud organizations list')

step_string='Step: Main menu: - 6 - Get active project'
print('')
print('Running '+step_string+'...')
print('Getting active project... ')

os.system('gcloud config get-value project ')

step_string='Step: Main menu: - 4 - Describe specific project'
print('')
print('Running '+step_string+'...')

project_name='ia-assistant-65b5f'
print('Describing project: '+project_name)
os.system('gcloud projects describe '+project_name)

step_string='Step: Main menu: - 8 - Set another project'
print('')
print('Running '+step_string+'...')

project_name='kurogane-165822'
print('Setting project: '+project_name)
os.system('gcloud config set project '+project_name)
