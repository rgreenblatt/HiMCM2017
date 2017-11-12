import os

for filename in os.listdir('.'):
    if filename.endswith('.kml'):
        os.rename(filename, filename[:-3]+'xml')
