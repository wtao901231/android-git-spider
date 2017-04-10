import json
import collections

with open('repo_master.json.all') as json_data:
    gitList = json.load(json_data)

remote2localMap = {}
for gitItem in gitList:
	remote2localMap[gitItem['name']] = gitItem['localPath']

googlesource = 'https://android.googlesource.com/'
prefix_len = len(googlesource)
rev = "/master"
rev_len = len(rev)

url2localPathMap = {}

for i in {1, 2}:
	mkfilename = 'aosp_git_mk.json.part%d' % i
	#print('merge %s' % mkfilename)
	with open(mkfilename) as mkfile:
		mkfileLns = mkfile.readlines()
		for ln in mkfileLns:
			mkfile = json.loads(ln)
			url = mkfile['url']
			idxOfPlus = url.index('+')
			gitname = url[prefix_len:idxOfPlus-1]
			path = url[idxOfPlus+1+rev_len:]
			localDir = remote2localMap[gitname]
			path = localDir + path
			url2localPathMap[url] = path

url2localPathMap = collections.OrderedDict(sorted(url2localPathMap.items()))

print('[')
for k in url2localPathMap:
	print('{\'base64-content-download-url\':\'%s?format=TEXT\', \'saved_path\':\'%s},' % (k, url2localPathMap[k]))
print(']')