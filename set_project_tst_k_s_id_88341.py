import os
import sys


step_string='Step: Main menu: - 8 - Set another project'
print('')
print('Running '+step_string+'...')

project_name='regal-height-281801'
print('Setting project: '+project_name)
os.system('gcloud config set project '+project_name)

step_string='Step: Main menu: - 4 - Describe specific project'
print('')
print('Running '+step_string+'...')

project_name='regal-height-281801'
print('Describing project: '+project_name)
os.system('gcloud projects describe '+project_name)

step_string='Step: Main menu: - 5 - Get configuration list - Lists account name and project data'
print('')
print('Running '+step_string+'...')
print('Getting configuration list for project data: ')

os.system('gcloud config configurations list ')

step_string='Step: Main menu: - 6 - Get active project'
print('')
print('Running '+step_string+'...')
print('Getting active project... ')

os.system('gcloud config get-value project ')

step_string='Step: Main menu: - 2 - Retrieve billing data for another project'
print('')
print('Running '+step_string+'...')

project_name='regal-height-281801'
print('Retrieving billing data for project name: '+project_name)
os.system('gcloud beta billing projects describe '+project_name)
