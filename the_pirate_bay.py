import requests, os
from bs4 import BeautifulSoup as bs

#Configurations
path="/Desktop" #give_path-download_folder
pirate_bay_active_site="" #give_link-pirate_bay.link



Pbpl=[pirate_bay_active_site]
#find_pirate_bay_live_proxy
if pirate_bay_active_site=="":
	print("Looking to find a Pirate Bay Server ...")
	site="https://pirateproxy.wtf/"
	page0=requests.get(site)
	soup0=bs(page0.text,"html.parser")
	Pbpl=[]
	for pbpl in soup0.find_all("a"):
		Pbpl.append(pbpl.text)
	Pbpl=Pbpl[1:15]
	print("{} Pirate Bay Proxy Servers Found!".format(len(Pbpl)))


#find_numbrer_of_results_and_pages
#example: https://unblockpirate.uk/search.php?q=la+casa&category=0&page=0&orderby=99
search=str(input("Tor search bar: "))
search_=search.split()
search=""
for i in search_:
	search+=i+"+"
search=search[:-1]
for pbpl in Pbpl:
	try:
		print("Trying to connect to {}".format(pbpl))
		link="http://"+pbpl+"/search.php?q="+search+"&category=0&page=0&orderby=99"
		page1=requests.get(link)
		soup1=bs(page1.text,"html.parser")
		results=int((soup1.find("h2").text).split()[-2])
		break
	except ValueError:
		print("Server is not Responding! Moving to the next one!")
	except:
		print("Critical Error! Maybe the pirate_bay_active_site is not compatible!")
		raise SystemExit
#find_page_number---
if results%30==0:
	pages=results//30
else:
	pages=results//30+1

D={}
k=1
for page in range(pages):
	os.system("clear")
	print("{} Results Found in {} Pages!".format(results,pages))
	print("Printing Results ...\n")
	link="http://"+pbpl+"/search.php?q="+search+"&category=0&page="+str(page)+"&orderby=99"
	page=requests.get(link)
	soup=bs(page.text,"html.parser")	
	for i in soup.find_all("a"):
		if i.get("class")==['detLink']:
			D[k]=[i.text,i.get("href")]
			k+=1
	#print_results:
	for i in D.keys():
		print("{}:  {}".format(i,D[i][0]))
	if pages>=1:
		more_r="n"
		if pages!=1:
			more_r=input("More Results? (y/n): ")
		if more_r!="y" or pages==1:
			number=int(input("Check torrent with number (Press 0 to continue searching):  "))
			if number in D.keys():
				site="http://"+pbpl+str(D[number][1])
				page2=requests.get(site)
				soup2=bs(page2.text,"html.parser")
				info=soup2.find("pre").text
				os.system("clear")
				print(info)
				X=input("\n\nGet torrent? (y/n): ")
				if X=="y":
					for i in soup.find_all("a"):
						if "magnet:?" in i.get("href"):
							magnet=i.get("href")
							break
					os.system("clear")
					print("Downloading torrent ...\n")
					os.system("transmission-cli ""{}"" -w ~{}".format(str(magnet),path))
					break
			elif (number!=0) and (number not in D.keys()):
				print("Number not exist!")
			else:#number=0	
				continue


