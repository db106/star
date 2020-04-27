
import time
import json

# need pip install bs4
# need pip install selenium
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from itertools import permutations

from decimal import Decimal
import datetime
import math




def google_distance(search_tag_list):
    google_distance_list = []
    # 建立Chrome物件
    driver = Chrome('./chromedriver')
    url = 'https://www.google.com.tw/maps/dir///@24.9554014,121.2384829,17z/data=!4m2!4m1!3e0?hl=zh-TW'
    for start in search_tag_list:
        for end in search_tag_list:

            if start == end:
                pass
            else:

                driver.get(url)
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="sb_ifc50"]/input').send_keys(start.replace('\n', ''))  # --- 輸入起點

                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="sb_ifc51"]/input').send_keys(end.replace('\n', ''))  # --- 輸入目的

                time.sleep(2)
                driver.find_element_by_xpath('//*[@id="sb_ifc51"]/input').send_keys(Keys.ENTER)
                time.sleep(5)
                driver.find_element_by_css_selector('span#section-directions-trip-details-msg-0').click()
                time.sleep(3)


                soup = BeautifulSoup(driver.page_source, 'html.parser')

                a = soup.select('h1[class="section-trip-summary-title"]')
                c = soup.select('h2[class="directions-mode-group-title"]')
                # print(c)
                address = [d.text for d in c]

                # print(b)
                for i in a:
                    # print(i.text.split('-')[0])
                    # time.sleep(1)

                    save_data_dict = {'出發地點': start.replace('\n', ''),
                                      '目的地': end.replace('\n', ''),
                                      '所需時間': i.text.split('-')[0],
                                      '路徑': address}


                    save_data_js = json.dumps(save_data_dict, ensure_ascii=False)

                    # print(save_data_js)
                    google_distance_list.append(save_data_js)




    driver.close()

    return google_distance_list

def google_staytime(search_tag_list):
    google_staytime_list = []

    driver = Chrome('./chromedriver')
    url = 'https://www.google.com/webhp'
    count = 0
    search_tag_set = set()

    for search_tag in search_tag_list:
        search_tag = search_tag.replace('\n', '')
        if search_tag not in search_tag_set:
            search_tag_set.add(search_tag)
            # print(search_tag)

            driver.get(url)
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(
                search_tag)  # 搜索
            # print(search_tag)
            # time.sleep(5)
            if url == driver.current_url:
                driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(
                    Keys.ENTER)  # Enter
            time.sleep(1)
            html = driver.page_source
            # print(html)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            a = soup.select('div[class="UYKlhc"]')
            # print(a)
            try:
                stop_time = a[0].text
            except:
                stop_time = 'NA'
            count += 1
            # print(type(count))

            time.sleep(1)
            save_data_dict = {'地點': search_tag,
                              '停留時間': stop_time}
            # print(save_data_dict)

            save_data_js = json.dumps(save_data_dict, ensure_ascii=False)

            google_staytime_list.append(save_data_js)



    driver.close()



    for i in google_staytime_list:  # 逐筆讀取
        each_content = json.loads(i)  # 將各筆轉成json
        # print(type(each_content), each_content)
        place_word = each_content.get('地點') # ; print(place_word)
        stoptime_word = each_content.get('停留時間') # ; print(stoptime_word)

        if stoptime_word.find('到') > 0: # 訪客通常會在此停留 20 分鐘到 1 小時
            seperate_1 = stoptime_word.split('到')[0]
            s_1 = ''.join(([x for x in seperate_1 if x.isdigit()]))
            seperate_2 = stoptime_word.split('到')[1]
            s_2 = ''.join(([x for x in seperate_2 if x.isdigit()]))

            if s_1 > s_2:
                # stay_s1s2 = (int(s_1)/60 + int(s_2))/2
                staytime = (int(s_1) / 60 + int(s_2)) / 2
                # print('停留時間:', staytime, '小時')

        elif stoptime_word.find('-') > 0: # 訪客通常會在此停留 1-2 小時
            seperate_3 = stoptime_word.split('-')[0]
            s_3 = ''.join(([x for x in seperate_3 if x.isdigit()]))
            seperate_4 = stoptime_word.split('-')[1]
            s_4 = ''.join(([x for x in seperate_4 if x.isdigit()]))
            # stay_s3s4 = (int(s_3) + int(s_4)) / 2
            staytime = (int(s_3) + int(s_4)) / 2
            # print('停留時間:', staytime, '小時')

        elif stoptime_word.find('.') > 0:

            # if stoptime_word.find('過'):
            #     # print(stoptime_word)
            #     seperate_5 = stoptime_word.split('過')[1]
            # else:
            #     seperate_5 = stoptime_word.split('會在此停留')[1]
            #
            #
            # # s_5 = float(seperate_5.split(' 小時')[0])
            # staytime = float(seperate_5.split(' 小時')[0])
            # print('停留時間:', staytime, '小時')
            staytime = float(stoptime_word.split(' ')[1])
        elif stoptime_word == 'NA':
            staytime = '0'

        else:
            staytime = ''.join(([x for x in stoptime_word if x.isdigit()]))
            # print('停留時間:', staytime, '小時')


        each_content["停留時間"] = staytime
        google_staytime_list[int(google_staytime_list.index(i))] = each_content


        # stoptime_js[place_word] = staytime
        # print(place_word, ': 停留時間', staytime, '小時')




    return google_staytime_list

def google_bestpath(search_tag_list,google_distance_list):
    google_bestpath_dict = {}
    each_spend_time_list = []
    return_routeplan = ''

    # 列出所有的排列組合
    p = search_tag_list  # ; print('p:', p)

    p_num = len(p)
    perm_all = list(permutations(p, p_num))  # ; print('perm_all:', perm_all) # 所有排列組合

    vs_distance = {}
    vs_time = {}
    for a in range(0, len(perm_all)):
        # print('perm_all[a])[0]', list(perm_all[a])[0])
        # print('p[0]', p[0])
        if list(perm_all[a])[0] == p[0]:
            path = list(perm_all[a])
            # print('試算路線', a + 1, ':', path)
            # print('check:', list(perm_all[a])[-1])

            all_distance = 0
            all_spend = 0

            # print(path)
            for each in range(0, len(path) - 1):
                p_start = path[each]
                p_end = path[each + 1]
                # print(each, p_start, each+1, p_end)

                # 列出google跑出的資訊

                for i in google_distance_list:  # 逐筆讀取
                    each_content = json.loads(i)  # 將各筆轉成json
                    # print('google txt:', each_content)
                    g_start = each_content.get('出發地點');
                    # print('g_start:', g_start)
                    g_end = each_content.get('目的地');
                    # print('g_end:', g_end)

                    try:
                        g_spend_time = int(each_content.get('所需時間').split('分 (')[0]);
                    except:
                        g_spend_time = 0
                        print(each_content.get('所需時間'))
                        if '小時' in each_content.get('所需時間'):
                            g_spend_time += int(each_content.get('所需時間').split('小時')[0]) * 60
                            g_spend_time += int(each_content.get('所需時間').split('小時')[1].split('分 (')[0])

                    # print('g_spend_time(', g_start, '-', g_end, '):',g_spend_time)

                    g_distance = str(each_content.get('所需時間').split('分 (')[1][:-6]);
                    # print('g_distanc(', g_start, '-', g_end, '):',g_distance)

                    # 列出所有試算路線
                    if g_start == p_start and g_end == p_end:
                        routeplan = a + 1, path, g_start, g_end, g_spend_time, g_distance
                        # print('routeplan:', routeplan)
                        return_routeplan += str(routeplan)
                        # print(return_routeplan)

                        each_spend_time_list.append(g_spend_time)
                        # print(g_start, '--', g_end, ': 時間', g_spend_time, '分鐘  距離', g_distance, '公里')
                        all_spend += int(g_spend_time);
                        # print('all_spend+', all_spend)
                        all_distance += float(g_distance);
                        # print('all_distance+', all_distance)

                        # 計算各路線的總時間與總距離
                        if g_end == list(perm_all[a])[-1] or g_start == list(perm_all[a])[-1]:
                            tt_time = all_spend / 60;
                            # print('總時間:', tt_time, '小時')
                            tt_distance = all_distance;
                            # print('總距離:', tt_distance, '公里')
                            vs_distance[str(
                                path)] = all_distance  # ; print(type(vs_distance), 'vs_distance:', vs_distance)
                            vs_time[str(all_distance)] = each_spend_time_list
                            each_spend_time_list = []

                    else:
                        pass


    # 找出最短路徑
    min_result = min(vs_distance.values())
    min_schadule = list(vs_distance.keys())[list(vs_distance.values()).index(min_result)]
    # print('建議路徑:', '\n', min_schadule, '\n', '總距離:', min_result, '公里')

    google_bestpath_dict = {'建議路徑':min_schadule,
                            '總距離':min_result,
                            '總時間':tt_time,
                            "各段時間": vs_time[str(min_result)]}

    return google_bestpath_dict , return_routeplan

def dpades_travel_plan(google_bestpath_dict,routeplan,google_staytime):
    final_list = []
    # 載入推薦路線
    departure = datetime.datetime(2020, 5, 15, 8, 00, 00)

    suggest_path = google_bestpath_dict['建議路徑']
    suggest_path = suggest_path[2:-2]
    suggest_path_list = list(suggest_path.split("', '"))
    # print('推薦路線:', suggest_path_list)
    # print('出發時間:', departure)
    # print()

    for each_path in range(0, len(suggest_path_list) - 1):
        # print(suggest_path_list[each_path], '--', suggest_path_list[each_path+1]) # 推薦路線

        sub_tt_time = 0
        departure = departure

        # 比對推薦路線在所有推薦的位置

        routeplan = str(routeplan)
        # print('routeplan',routeplan)

        all_suggest = routeplan[2:-2]  # ; print('all_suggest:', all_suggest)
        all_suggest_list = list(all_suggest.split(")("))  # ; print('all_suggest_list:', all_suggest_list)

        for index, content in enumerate(all_suggest_list):
            if str(suggest_path_list) in content:
                # print(index, content) # 找出推薦的位置及所有內容
                take = content[len(str(suggest_path_list)) + 4:].split(",")  # ; print('take:', take)
                trafficetime = round(Decimal((float(take[-2]) / 60)), 1)  # 交通時間

                # print('all_suggest_list',all_suggest_list)
                # print('suggest_path_list',suggest_path_list)
                # print('content', content)
                # print('take',take)


                # print('google_staytime',google_staytime)
                # 載入各點的停留時間
                tmp_google_staytime = json.dumps(google_staytime,ensure_ascii=False)
                stop_each = json.loads(tmp_google_staytime)

                # print(stop_each.get(suggest_path_list[each_path + 1]))
                stoptime = round(Decimal(stop_each.get(suggest_path_list[each_path + 1])), 1)  # 停留時間

                tt_time = trafficetime + stoptime
                sub_tt_time += tt_time  # 交通+停留時間(累加)

                # print('suggest_path_list[each_path]',suggest_path_list[each_path])
                # print('take[-4][2:-1]',take[-4][1:-1])
                # print('suggest_path_list[each_path + 1]',suggest_path_list[each_path + 1])
                # print('take[-3][2:-1]',take[-3][2:-1])
                # print('='*50)

                if suggest_path_list[each_path] == take[-4][2:-1] and suggest_path_list[each_path + 1] == take[-3][2:-1]:
                    stay_min = list(math.modf(tt_time))  # ; print(stay_min)
                    traffic_stay_time = datetime.timedelta(hours=stay_min[1], minutes=stay_min[0] * 60)
                    departure += traffic_stay_time;  # print('departure1', departure)

                    # 各欄位數字
                    final = {'出發': take[-4],
                             '到達': take[-3],
                             '距離': take[-1],
                             '交通時間': trafficetime,
                             '停留時間': stoptime,
                             '交通+停留時間': tt_time,
                             '累積時間': sub_tt_time,
                             '離開時間': departure
                             }
                    # print(final)

                    final_list.append(final)
                else:
                    pass

    # print('sub_tt_time',sub_tt_time)
    travel_suggest = '累積時數:{} 小時___'.format(sub_tt_time)
    if sub_tt_time > 10:
        # print('行程太滿, 請刪減景點!')
        travel_suggest += '行程太滿, 請刪減景點!'

    elif sub_tt_time < 5:
        # print('行程有點少, 請考慮增加景點‧')
        travel_suggest += '行程有點少, 請考慮增加景點'

    else:
        # print('祝您旅途愉快!!')
        travel_suggest += '祝您旅途愉快!!!'


    return final_list , travel_suggest

def main(search_tag_list = ['台北車站','富貴角燈塔', '十分瀑布', '木蘭閣']):

    google_distance_list = google_distance(search_tag_list)
    # print('google_distance_list',google_distance_list)


    google_staytime_list = google_staytime(search_tag_list)
    # print('google_staytime_list',google_staytime_list)

    # google_staytime_list = [{'地點': '台北車站', '停留時間': '0'}, {'地點': '富貴角燈塔', '停留時間': '30'}, {'地點': '十分瀑布', '停留時間': '0'}, {'地點': '木蘭閣', '停留時間': '0'}]


    google_staytime_dict = {}
    for each_google_staytime in google_staytime_list:
        if each_google_staytime['地點'] not in google_staytime_dict:
            google_staytime_dict[each_google_staytime['地點']] = each_google_staytime['停留時間']

    # print(google_staytime_dict)


    google_bestpath_dict,routeplan = google_bestpath(search_tag_list,google_distance_list)
    # print('google_bestpath_dict',google_bestpath_dict)
    # print('routeplan', routeplan)

    final_list , travel_suggest = dpades_travel_plan(google_bestpath_dict,routeplan,google_staytime_dict)
    # print('final_list',final_list)
    # print('travel_suggest',travel_suggest)



    return final_list , travel_suggest


if __name__ == '__main__':
	time_start = time.time()
	main()
	cost_time = time.time() - time_start
	print(cost_time / 3600, '小時',cost_time)
	print('Complete!!!!!!!!!!')