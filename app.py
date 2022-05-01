import requests
import re
from bs4 import BeautifulSoup,SoupStrainer
import gdown
import psycopg2
import os
import shutil
import time



def bot():
    #database
    conn=psycopg2.connect(dbname='test',user='masum',password='masum1011',host='localhost',port='5432')
    cur=conn.cursor()
    print('connected')
    cur.execute('create table if not exists links(id SERIAL,link text)')
    conn.commit()
    conn.close()
    
    
    connection_error=False
    try:
        r=requests.get(url='http://www.bteb.gov.bd/site/page/a34671e3-a81c-4927-834f-19d6afc41217/%E0%A6%A1%E0%A6%BF%E0%A6%AA%E0%A7%8D%E0%A6%B2%E0%A7%8B%E0%A6%AE%E0%A6%BE-%E0%A6%AA%E0%A6%B0%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A7%9F')
    except:
        connection_error=True
        print('connection error')
    if not connection_error:
        soup=BeautifulSoup(r.text,parse_only=SoupStrainer('a'),features="lxml")
        l=soup.findAll('a')
        
        for i in range(51,58):
            #if not isSame(link,previousLink):
                
                link=l[i]
            
                if re.search('Army|Naval',str(link))==None:
                    
                    x=re.search("Diploma in (Engg|Engineering)",str(link))
                    if x != None:
                        conn=psycopg2.connect(dbname='test',user='masum',password='masum1011',host='localhost',port='5432')
                        cur=conn.cursor()
                        cur.execute('select link from links where link=%s',(str(link.attrs['href']),))
                        rows=cur.fetchall()
                        
                        if len(rows)==0:
                                
                                cur.execute('INSERT into links(link) values (%s)',(link.attrs['href'],))
                                conn.commit()
                                
                                if "open?id="in str(link) or "file" in str(link) or "uc?id=" in str(link):
                                    file_id=link.attrs['href'].replace('https://drive.google.com/file/d/','').replace('/view?usp=sharing','')
                                    print(file_id)
                                    gdown.download("https://drive.google.com/uc?id={}".format(file_id),quiet=True,output='current_result/{}.pdf'.format(link.text))
                                if "drive/folders" in str(link):
                                    gdown.download_folder(link.attrs['href'],quiet=True,output='current_result')
                                    
                                break
                        else:
                            print('already exists')
                    
                else:
                    print('yes')        





    #post
    if len(os.listdir('current_result'))!=0:
        for filename in os.listdir('current_result'):
            f=open(os.path.join('current_result',filename),'rb')
            requests.post('http://localhost:8080/',files={'filename':f})
            os.remove(os.path.join('current_result',filename))
        time.sleep(60*60*24*15)
    
def run_bot_infinitely():
    bot()
    time.sleep(60*60)
    run_bot_infinitely()
run_bot_infinitely()