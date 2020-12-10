import tmdbsimple as tmdb
import datetime
import os
import re
from pathlib import Path
import urllib.request

tmdb.API_KEY = 'b14d33b9ffc8b0739a559a12a4117453'
# tmdb.API_LANG = 'zh-CN'

img_base_url = 'http://image.tmdb.org/t/p/w600_and_h900_bestv2'

ART_RE = r'\<name\>(.*)\</name>'
ID_RE = r'\<actor_tmdb_id\>(.*)\</actor_tmdb_id>'
DIR_RE = r'\<director_tmdb_id\>(.*)\</director_tmdb_id>'
MAX_PEOPLE_PER_ITEM = 5
PEOPLE_ROOT = ''

# 0 for renew, 1 for update
model = 1

def download_people_poster(p, poster_path):
	if 'profile_path' not in p.keys() or p['profile_path'] is None:
		return
	print(poster_path)
	img_url = img_base_url + p['profile_path']
	print(img_url)

	urllib.request.urlretrieve(img_url, filename=poster_path)
	pass

def people_from_nfo(nfo_file, people_path):
	with open(nfo_file, 'r', encoding='unicode_escape') as nfo:
		i = 0
		for line in nfo.readlines():
			i += 1

			# actors
			pid = re.findall(ID_RE, line)
			if pid == []:
				# directors
				pid = re.findall(DIR_RE, line)
				if pid == []:
					continue

			print(pid)
			person = tmdb.People(pid[0])
			p = person.info()

			print(p['name'])
			real_name = p['name'].strip('.')


			path = Path(people_path+'/'+real_name[0].upper())
			print(path)
			if not path.exists():
				path.mkdir()

			name_path = Path(people_path+'/'+real_name[0].upper()+'/'+real_name)
			print(name_path)

			if not name_path.exists():
				name_path.mkdir()

			poster_path = Path(people_path+'/'+real_name[0].upper()+'/'+real_name+'/poster.jpg')
			if poster_path.exists() and model == 1:
				continue
			download_people_poster(p, str(poster_path))

			if i > MAX_PEOPLE_PER_ITEM:
				break



if __name__ == '__main__':
	root = '/mnt/dsm'
	# root = 'Z:'
	root_path = root + '/transmission/Movies/'
	people_path = root + '/transmission/people_metadata'
	root = Path(root_path)
	for file_name in root.rglob('*.nfo'):
		print(file_name)
		people_from_nfo(str(file_name), people_path)