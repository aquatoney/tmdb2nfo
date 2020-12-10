
import urllib.request

img_url = 'http://image.tmdb.org/t/p/w600_and_h900_bestv2/75WD73x67ILPQH8Z7KqvZgMUdpH.jpg'
poster_name = '1.jpg'

req = urllib.request.Request(
    img_url, 
    data=None, 
    headers={
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "max-age=0",
        "cookie": "__cfduid=de2f8bcee4b1e0b1b7384a885d788ef851607161527",
        "if-modified-since": "Sat, 17 Oct 2020 06:10:50 GMT",
        "if-none-match": "d6225214baa0fa077844867f6c1445e3",
        "sec-ch-ua": 'Chromium";v="86", "\"Not\\A;Brand";v="99", "Google Chrome";v="86"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
)

f = urllib.request.urlopen(req)
with open(poster_name) as poster_file:
	poster_file.write(f.read())

# opener = urllib.request.build_opener()
# opener.addheaders = [('User-agent', UA), ('Cookie', CK)]
# urllib.request.install_opener(opener)
# urllib.request.urlretrieve(img_url, filename=poster_name)