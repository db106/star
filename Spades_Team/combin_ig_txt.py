import os
import time
import json


# dir_path = 'E:\資策會-DB106\專題\Instagram\All'
dir_path = 'E:\資策會-DB106\專題\Pixnet\All'
dir_list =  os.listdir(dir_path)
txt = ''


time_start = time.time()
for each_dir in dir_list:
    dir_dir_path = dir_path +'\\'+ each_dir
    dir_dir_list = os.listdir(dir_dir_path)
    txt = ''
    for each_txt in dir_dir_list:
        if each_txt != 'shortcode.txt':
            with open(dir_dir_path+'\\'+each_txt, 'r', encoding='utf8') as f:
                #只取中文

                for each_line_word in f.readlines():

                    try:
                        each_JsData = json.loads(each_line_word, encoding='utf-8')
                        # print('each_line_word:', each_line_word)
                        txt = each_JsData['標題']
                        txt += '\n'
                        print('標題 :', txt)
                        with open('E:\資策會-DB106\專題\Pixnet\標題_'+each_dir+'.txt', 'a',encoding='utf8') as f:
                            f.write(txt)
                    except Exception as e:
                        pass




    cost_time = time.time() - time_start
    print(cost_time / 3600, '小時')

cost_time =time.time() - time_start
print(cost_time/3600,'小時')
print('Complete!!!!!!!!!!')


