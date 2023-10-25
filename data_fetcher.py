#a script used to fetch musescore scores from IMSLP
#Chad Brown
#Last updated 10/24/2023
import requests
import imslp.client as imslpClient

#initialize our client and find Bach
#Note:  the imslp python library is VERY slow and inneficient, but we won't need to run this often, so that's okay for now
#       Just expect this to take a while
client = imslpClient.ImslpClient()
works = client.search_works(composer="Bach")

print(works)

