import tmdbsimple as tmdb
import datetime
import os
import re
from pathlib import Path
import urllib.request


tmdb.API_KEY = 'b14d33b9ffc8b0739a559a12a4117453'
tmdb.API_LANG = 'zh-CN'
template_nfo_name = 'template_info.nfo'
img_base_url = 'http://image.tmdb.org/t/p/w600_and_h900_bestv2'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
MAX_PAGE = 8

# 0 for renew, 1 for update, 2 for update with tmdb_id in nfo
model = 2

def is_year(year):
  try:
    real_year = int(year)
    if real_year < 1940 or real_year > datetime.datetime.now().year:
      return False
    return True
  except:
    return False

def extract_filename(file_name):
  name = ''
  year = ''
  item_name = file_name.split('/')[-1]
  item_name = item_name.replace(' ', '.')
  token_list = item_name.split('.')
  print(token_list)
  for i, token in enumerate(reversed(token_list)):
    if is_year(token):
      year = token
      name = ' '.join(token_list[:-(i+1)])
      break
  if year == '' or name == '':
    return None, None
  print(name, year)
  return name, year

def search_item(itype, name, year=''):
  search = tmdb.Search()
  results = []
  page = 1
  while results == [] and page <= MAX_PAGE:
    response = search.movie(query=name, year=year, page=page)
    results = sorted(search.results, key=lambda x: x['popularity'], reverse=True)
    # for r in results:
    #   print(page, r)

    # double check
    for r in results:
      if year in r['release_date']:
        item = tmdb.Movies(r['id'])
        return item

    page += 1

  return None

def generate_entry(field, value, field_end=''):
  if field_end == '':
    field_end = field
  return "<{0}>{1}</{2}>\n".format(field, value, field_end)

def generate_info(item, file_name):
  s = item.info()
  info = ''
  info += generate_entry('title', s['title'])
  info += generate_entry('tagline', s['tagline'])
  info += generate_entry('originaltitle', s['original_title'])
  info += generate_entry('plot', s['overview'])
  info += generate_entry('rating', s['vote_average'])
  info += generate_entry('releasedate', s['release_date'])
  info += generate_entry('runtime', s['runtime'])
  info += generate_entry('uniqueid default="true" type="imdb"', s['imdb_id'], 'uniqueid')
  info += generate_entry('tmdb_id', str(s['id']))
  # genres
  for g in s['genres']:
    info += generate_entry('genre', g['name'])

  # director
  c = item.credits()['crew']
  for p in c:
    if p['job'] == 'Director':
      info += generate_entry('director', p['name'])
      info += generate_entry('director_tmdb_id', str(p['id']))
      break

  # actors
  c = item.credits()['cast']
  for p in c:
    if p['known_for_department'] == 'Acting':
      an_actor = ''
      an_actor += generate_entry('name', p['name'])
      an_actor += generate_entry('role', p['character'])
      an_actor += generate_entry('type', 'Actor')
      an_actor += generate_entry('actor_tmdb_id', str(p['id']))
      an_actor = generate_entry('actor', '\n'+an_actor)
      info += an_actor

  # poster
  poster_name = '.'.join(file_name.split('.')[:-1]) + '.jpg'
  img_url = img_base_url + s['poster_path']
  print(img_url)

  urllib.request.urlretrieve(img_url, filename=poster_name)

  poster = generate_entry('poster', poster_name)
  info += generate_entry('art', poster)

  # print(info)
  return info

def generate_nfo(file_name, real_model=model, concrete_id=-1):
  lock_name = '.'.join(file_name.split('.')[:-1]) + '.lock'
  nfo_name = '.'.join(file_name.split('.')[:-1]) + '.nfo'
  path = Path(lock_name)
  if path.exists():
    # print('nfo has been collected before')
    if real_model == 0:
      # print('refreshing')
      pass
    elif real_model == 1:
      # print('ignoring')
      return
    elif real_model == 2:
      # print('update with concrete id')
      try:
        with open(nfo_name, 'r', encoding='unicode_escape') as existed_nfo:
          for line in existed_nfo.readlines():
            tid = re.findall(r'\<tmdb_id\>(.*)\</tmdb_id\>', line)
            if tid != []:
              concrete_id = int(tid[0])
              break
      except:
        print('do not find tmdb_id, refreshing')

  if concrete_id != -1:
    item = tmdb.Movies(concrete_id)
  else:
    item_name, item_year = extract_filename(file_name)
    if item_name is None or item_year is None:
      print('name/year not found', file_name)
      return

    item = search_item('movie', item_name, item_year)
    if item is None:
      print('not found by name+year', item_name + ' ' + item_year)
      item = search_item('movie', item_name)

  if item is None:
    print('not found by name or concrete_id')
    return

  print(item.info()['title'])

  info = generate_info(item, file_name)

  write_nfo = open(nfo_name, 'w', encoding='utf8')
  template_nfo = open(template_nfo_name, 'r', encoding='utf8')
  for entry in template_nfo.readlines():
    entry = entry.replace('NFO_OTHERS', info)
    write_nfo.write(entry)
  template_nfo.close()
  write_nfo.close()
  # leave a lock file
  lock_file = open(lock_name, 'w', encoding='utf8')
  lock_file.write(str(int(datetime.datetime.now().timestamp())))
  lock_file.close()


if __name__ == '__main__':
  root_path = '/mnt/dsm/transmission/Movies/'
  root = Path(root_path)
  # single_file = 'Rage.2016.1080p.BluRay.x264.DTS-WiKi/Rage.2016.1080p.BluRay.x264.DTS-WiKi.mkv'
  # generate_nfo(root_path+single_file, real_model=0, concrete_id=359344)
  single_file = 'Bilal.A.New.Breed.of.Hero.2015.1080p.FRA.BluRay.AVC.DTS-HD.MA.5.1-DiY@HDHome/Bilal.A.New.Breed.of.Hero.2015.1080p.FRA.BluRay.AVC.DTS-HD.MA.5.1-DiY@HDHome.mkv'
  generate_nfo(root_path+single_file, real_model=0)
  exit()
  for file_name in root.rglob('*.mkv'):
    if 'Sample' in str(file_name):
      continue
    print(file_name)
    generate_nfo(str(file_name))
  for file_name in root.rglob('*.mp4'):
    if 'Sample' in str(file_name):
      continue
    print(file_name)
    generate_nfo(str(file_name))
  for file_name in root.rglob('*.ts'):
    if 'Sample' in str(file_name):
      continue
    print(file_name)
    generate_nfo(str(file_name))
