import os
import pandas as pd
import pprint
FJoin = os.path.join 
def GetFiles(path):
	file_list, dir_list = [], []
	for dir, subdirs, files in os.walk(path):
		file_list.extend([FJoin(dir, f) for f in files])
		dir_list.extend([FJoin(dir, d) for d in subdirs])
	file_list = filter(lambda x: not os.path.islink(x), file_list)
	dir_list = filter(lambda x: not os.path.islink(x), dir_list)
	return file_list, dir_list
files, dirs = GetFiles(os.path.expanduser("handpose"))
for file in files:
	if file.endswith(".pickle"):
		try:
			chiso=file.rfind('/')
			link = file[0:chiso]
			namefile= file[chiso+1:len(file)]
			Files = pd.read_pickle(file, compression='infer')
			value = Files['kps2D']
			sodong=value.shape[0]
			minx=5000
			miny=5000
			maxx=0
			maxy=0
			for row in range(sodong):
				x_value=value[row,0]
				y_value=value[row,1]
				if(x_value<minx):
					minx=x_value
				if(y_value<miny):
					miny=y_value
				if(x_value>maxx):
					maxx=x_value
				if(y_value>maxy):
					maxy=y_value
			filename_new = namefile.replace("pickle", "txt")
			linktxt=link+ '/'+ filename_new
			with open(linktxt, "a") as f:
				f.truncate(0)
				f.write('{} {} {} {}'.format(minx, miny, maxx - minx, maxy - miny))
				f.close()
		except:
			print("error", file )
			with open("handpose/error.txt", "a") as f:
				pprint.pprint(file, stream=f)
				f.close()
