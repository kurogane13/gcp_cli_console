def reading_from_file():
  file_to_read=input('Provide file name to read: ')
  openfile = open(file_to_read, 'r')
  print(openfile.read())
  openfile.close()
reading_from_file()
