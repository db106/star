import random

place_labels_dict = {'古蹟': ['華山1914文化創意產業園區','國立故宮博物院','梁實秋故居'],
                     '海岸': ['淺水灣海濱公園','石門洞','深澳岬角'],
                     '瀑布': ['青山瀑布','十分瀑布','銀河瀑布'],
                     '燈塔': ['淡水港燈塔','富貴角燈塔','三貂角燈塔'],
                     '登山': ['金面山步道','頂山石梯嶺步道','南港山縱走親山步道'],
                     '遊樂園': ['臺北市兒童新樂園','野柳海洋世界',],
                     '淡水魚人碼頭': ['淡水魚人碼頭'],
                     '台北101': ['台北101'],
                     '紅毛城': ['紅毛城']}


food_labels_dict = {'pizza': ['Gusto Pizza','初宅 ONE HOUSE PIZZA','Papa Vito'],
                   'hot_pot': ['元和屋日式海鮮火鍋','木蘭閣','碼頭老火鍋'],
                   'ice_cream': ['永富冰淇淋','冰淇淋機場','Double V'],
                   'burrito':['NALAs Mexican Food','Macho Tacos 瑪丘墨式餅舖','Macho Tacos 瑪丘墨式餅舖 '],
                   'rotisserie':['樂軒和牛專門店','京昌園日本本格燒肉餐廳','樂軒松阪亭']}

def place_recommend(pred_place_dict):
    place_recommend_list = []
    for each_place in pred_place_dict.items():
        place_recommend_list.append(place_labels_dict[each_place[0]][random.randint(0, len(place_labels_dict[each_place[0]])-1)])

    return place_recommend_list


def food_recommend(pred_food_dict):
    food_recommend_list = []
    for each_food in pred_food_dict.items():
        food_recommend_list.append(food_labels_dict[each_food[0]][random.randint(0, len(food_labels_dict[each_food[0]]) - 1)])

    return food_recommend_list




def main():
    pred_place_dict = {'古蹟': 1, '台北101': 3, '紅毛城': 1, '海岸': 1, '燈塔': 1, '瀑布': 1,'淡水魚人碼頭':1}
    pred_food_dict = {'pizza': 1, 'hot_pot': 1, 'ice_cream': 1, 'burrito': 1, 'rotisserie': 1}

    for _ in range(0,5):
        print(place_recommend(pred_place_dict))
        print(food_recommend(pred_food_dict))



if __name__ == '__main__':
    main()