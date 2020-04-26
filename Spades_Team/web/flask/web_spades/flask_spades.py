# pip install flask
# pip3 install flask-bootstrap
# pip3 install flask-bootstrap4
# pip install flask-wtf Flask-SQLAlchemy

import time
from flask import Flask, render_template, request

from flask_bootstrap import Bootstrap


from Spades_Team.deep_learning.CNN_spades import load_CNN_model
from Spades_Team.spades_teamer_code.VGG16_spades import predict
from Spades_Team.spades_teamer_code.spades_recommend import place_recommend ,food_recommend
from Spades_Team.spades_teamer_code.route_plan import main as route_plan
from Spades_Team.spades_teamer_code.weather import weather


app = Flask(__name__) #建立 Flask 物件
# app.config['UPLOAD_FOLDER'] = upload_dir # user_test 上傳照片的存檔路徑
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

bootstrap = Bootstrap(app)   #建立 bootstrap 物件


@app.route('/')
def my_index():

    return render_template('index.html')

@app.route('/sign_up')
def sign_up():

    return render_template('sign_up.html')

@app.route('/action_number.php',methods=['GET'])
def action_number():
    name = request.args.get('username')

    return render_template('load_pic.html',username = name)

@app.route('/load_pic',methods=['GET','POST'])
def load_pic():
    return render_template('index.html')


@app.route('/upload',methods=['GET','POST'])
def action_load_pic():
    global filenames, upload_dir,place_filenames,food_filenames
    # user_test 上傳照片的存檔路徑
    upload_dir = r'E:\資策會-DB106\Python\PycharmProjects\Spades\Spades_Team\web\flask\web_spades'

    if request.method == 'POST':
        uploaded_place_files = request.files.getlist("place")
        uploaded_food_files = request.files.getlist("food")
        filenames = []
        place_filenames = []
        food_filenames = []

        for file in uploaded_place_files:
            filename = file.filename
            file.save(upload_dir + "/static/" + filename)
            place_filenames.append(filename)
            filenames.append(filename)

        for file in uploaded_food_files:
            filename = file.filename
            file.save(upload_dir + "/static/" + filename)
            food_filenames.append(filename)
            filenames.append(filename)



    print('filenames',filenames)
    return render_template('confirm.html',filenames=filenames)


@app.route('/travel_plan',methods=['GET','POST'])
def travel_plan():
    time_start = time.time()

    pred_place_dict = load_CNN_model(model_path="E:/資策會-DB106/Python/PycharmProjects/Spades/Spades_Team/deep_learning/CnnModelTrainPlace_v0.6.h5",pic_dir_path= upload_dir + "/static",pic_list=place_filenames)
    pred_food_dict = predict(pic_dir_path= upload_dir + "/static",pic_list=food_filenames)
    # print('pred_place_dict ', pred_place_dict)
    # print('pred_food_dict ', pred_food_dict)


    '''
    照片分析完成 進 類別推薦 模型 程式撰寫區
    '''

    place_recommend_list = place_recommend(pred_place_dict)
    food_recommend_list = food_recommend(pred_food_dict)
    print('place_recommend_list ', place_recommend_list)
    print('food_recommend_list ', food_recommend_list)

    '''
    得到 地點 進 路線規劃 模型 程式撰寫區
    '''
    start_place_list = ['台北車站']
    final_list , travel_suggest = route_plan(start_place_list+place_recommend_list+food_recommend_list)
    print(final_list)
    print(travel_suggest)

    weather_dict = weather()
    print(weather_dict)

    cost_time = time.time() - time_start
    print(cost_time,'秒')

    return render_template('index.html' )


#============================================================================================





if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)