from flask import Flask,render_template,request,redirect,url_for,flash,jsonify,session
from datetime import datetime
from weather import main
import ast
import pickle
import joblib
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello'


def predict_production(data):
    fi = open("./ML_model_setup/major_project/pre_pro.pkl","rb")
    combined = pickle.load(fi)
    fi.close()
    print(data)
    print(combined)
    model = joblib.load("/home/amogha/Desktop/amogha_personal/work/random_forest.joblib")
    x = []
    data[0] = combined.index(data[0].upper())+1
    data[1] = int(data[1])
    data[2] = combined.index(data[2])+1
    data[3] = combined.index(data[3])+1
    data[4] = float(data[4])
    res = model.predict([data])
    print(res)
    return res






def fetch_res():
    get_to = datetime.now().strftime("%Y-%m-%d")
    f = open("data_wth.txt","r")
    data = f.read()
    f.close()
    f = 0
    mydi = ast.literal_eval(data)
    if len(data) == 0 :
        main()
        f=1

    elif not mydi.get(get_to,None):
        main()
        f=1

    else:
        return mydi.get(get_to)

    if f==1:
        f= open('data_wth.txt','r')
        data = f.read()
        mydi=ast.literal_eval(data)
        f.close()
        return mydi.get(get_to)

    return []


@app.route('/predict_data',methods=["POST","GET"])
def predict_data():

    if request.method == "POST":
        # print(request.form.get("em1"))
        print(request.form)
        ans = fetch_res()
        print(ans)
        data = []
        data.append(request.form.get("district"))
        data.append(request.form.get("crop_year"))
        data.append(request.form.get("season"))
        data.append(request.form.get("Crop"))
        data.append(request.form.get("area"))
        data = data + ans
        res = predict_production(data)
        print(res)
        # print(request.form.get("paswd"))
        flash(f"thanks for submitting !!your value {res} ","success")
        return render_template("predict_data.html",res=res)
    else:
        print("Not enetered",request.method)
        flash("Please fill the feilds","danger")
        return render_template("predict_data.html")
    return render_template("predict_data.html")





if __name__ == '__main__':
    app.run(debug=True)