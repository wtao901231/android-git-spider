import json
import os
import base64
import urllib.request
from multiprocessing import Process

target_dir = 'asop'

def mkdir_p(path):
    try:
    	dir = os.path.dirname(path)
    	os.makedirs(dir)
    except:
        pass

def checkinvalid(path):
	if not os.path.exists(path):
		return 1
	if (os.stat(path).st_size == 0):
		return 1
	return 0

def download(url, path, idx, cnt):
	if not checkinvalid(path):
		print('%d/%d: skip exists %s' % (idx, cnt, path))
		return
	try:
		print('%s >> %s' % (url, path))
		resp = urllib.request.urlopen(url)
		print('%d/%d: status [%d] %s' % (idx, cnt, resp.getcode(), url))
		data = resp.read()
		base64txt = data.decode('utf8')
		txt = base64.b64decode(base64txt).decode('utf8')
		text_file = open(path, "w")
		text_file.write(txt)
		text_file.close()
	except urllib.error.HTTPError as e:
		print(e)
	except:
		pass

def sync(gitList, indexFrom, indexTo, cnt, taskid):
	print('task#%d range[%d,%d) sync...' % (taskid, indexFrom, indexTo))
	idx = indexFrom
	for item in gitList[indexFrom:indexTo]:
		idx = idx + 1
		url = item['base64-content-download-url']
		path = '%s/%s' % (target_dir, item['saved_path'])
		mkdir_p(path)
		download(url, path, idx, cnt)
	print('task#%d done.' % taskid)

def main():
	with open('aosp_git_mk.json.ok') as json_data:
	    gitList = json.load(json_data)
	cnt = len(gitList)
	syncj = 5

	# for i in range(syncj):
	# 	indexFrom = int(i * cnt / syncj);
	# 	indexTo = int((i+1) * cnt / syncj);
	# 	indexTo = min(indexTo, cnt)
	# 	p = Process(target=sync, args=(indexFrom, indexTo, cnt, i))
	# 	p.start()
	# 	p.join()

	fail_cnt = 0
	idx = 0
	for item in gitList:
		idx = idx + 1
		url = item['base64-content-download-url']
		path = '%s/%s' % (target_dir, item['saved_path'])
		if checkinvalid(path):
			fail_cnt = fail_cnt + 1
			print('warn: %s >> %s' % (url, path))
			download(url, path, idx, cnt)
	print("total: %d fail count: %d" % (cnt, fail_cnt))
main()