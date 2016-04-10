import pymongo
from config import config


class SongModel(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            config['default'].MONGODB_SERVER,
            config['default'].MONGODB_PORT
        )
        db = connection[config['default'].MONGODB_DB]
        self.collection = db[config['default'].MONGODB_COLLECTION]

    def get_items(self):
        items = []
        for item in self.collection.find():
            # print(item)
            if(item['name'] != None):
                items.append(item['name'])
        return items

    def get_item(self, name):
        item = self.collection.find_one({'name':name})
        if(item):
            return item
        else:
            return ''

    def put_item(self, dic):
        self.collection.find_one_and_update({'name':dic['name']},
                                            {'$set':{'url':dic['url'],
                                                     'lrc':dic['lrc']}},
                                            upsert=True)
        # self.collection.find_one_and_update()
        # if(res):
        #     self.collection.update()
        # self.collection.insert({'name':dic['name'],'url':dic['url']})

    def remove_item(self, name):
        self.collection.remove({'name':name})

if __name__ == '__main__':
    song2 = {'name':'Danielle Delaite-Love Sex Goddess.mp3',
             'url':'/home/magicyang/Music/Danielle Delaite-Love Sex Goddess.mp3',
             'lrc':'/home/magicyang/Music/Danielle Delaite-Love Sex Goddess.lrc'}
    sm = SongModel()
    sm.put_item(song2)
    str = sm.get_item(song2['name'])
    song_list = sm.get_items()
    print(song_list)
    # sm.remove_item(song2['name'])
    # song_list = sm.get_items()
    # print(song_list)

