import discord
from discord.ext import tasks
import feedparser
from datetime import datetime
import linecache

def rss_picker():
    RSS_URL = 'https://automaton-media.com/feed/'
    no_news_flag = 1
    news_list = []
    log_path = 'data/log.txt'
    latest_URL = ''

    with open(log_path, mode='r') as f:
        old_news_url = f.read()
        print('前回取得したニュースURL:' + old_news_url)


    d = feedparser.parse(RSS_URL)

    for entry in d.entries:
        if old_news_url == entry.link:
            print(d.channel.title + 'のニュースは以上です')
            break

        if '無料' in entry.title:
            no_news_flag = 0
            print(entry.title, entry.link)
            news_list.append(entry.title + '\r\n' + entry.link) 
            if latest_URL == '':
                latest_URL = entry.link
            

    if no_news_flag == 0:
        with open(log_path, mode='w') as f:
            f.write(latest_URL)
            print(latest_URL)

    else:
        news_list.append('最新のゲーム無料配布ニュースはありません')

    print('news_list=', news_list)

    return news_list

data = linecache.getline("./data/secret.txt", 1)
ID = linecache.getline("./data/secret.txt", 2)

TOKEN = data
NEWS_CHANNEL_ID = ID

client = discord.Client()

@client.event
async def on_ready():
    print('ログインしました')

@tasks.loop(seconds=60)
async def loop():
    now = datetime.now().strftime('%H:%M')
    if now == '18:00':
        channel = client.get_channel(NEWS_CHANNEL_ID)
        print('channel = ', channel)
        news_list = rss_picker()
        for news in news_list:
            await channel.send(news)

loop.start()
client.run(TOKEN)
