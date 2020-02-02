from datetime import datetime
import piexif

import os
import time
import re

def get_date(filename):
	date_str = re.search(r'\d+', filename).group()
	return datetime.strptime(date_str, '%Y%m%d').strftime("%Y:%m:%d %H:%M:%S")

folder = 'D://Dropbox//Photos Backup/'
filenames = [os.path.join(root, name)
             for root, dirs, files in os.walk(folder)
             for name in files
             if name.endswith((".mp4", ".jpg", ".jpeg"))]

l = len(filenames)
print(l)

for filename in filenames:
	print(filename, end = '\t')
	try:
		if filename.endswith('mp4'):
			date = get_date(filename)
			modTime = time.mktime(datetime.strptime(date, "%Y:%m:%d %H:%M:%S").timetuple())
			os.utime(filename, (modTime, modTime))

		elif filename.endswith('jpg') or filename.endswith('jpeg'):
			exif_dict = {'Exif': {piexif.ExifIFD.DateTimeOriginal: get_date(filename)}}
			exif_bytes = piexif.dump(exif_dict)
			piexif.insert(exif_bytes, filename)

		print('OK')
	except:
		print('ERROR')
		pass
print('\nDone!')