from flask import Flask,render_template,request,redirect 
import pandas as pd 
import numpy as np 
import pickle


apps=Flask(__name__)  
data=pd.read_csv("clean_data.csv")
@apps.route('/')
def home(): 
    location=(data["City"]+ " "+data["Location"]).unique()
    city=data["City"].unique()  
    
    bhk=sorted(data["bedrom"].unique())
    
    return render_template("index.html",location=location,city=city,bhk=bhk)

@apps.route("/predict",methods=["POST"])
def predict():
    if request.method=='POST': 
        area=int(request.form["area"]) 
        bhk=int(request.form["bhk"]) 
        city=request.form["city"] 
        location=request.form["location"]  
        orj=str(location.split(city)[1])
        la=lambda x:x.strip() 
        finalda=la(orj) 
        
        da=pd.DataFrame({"Area":[area],"Location":[finalda],"City":[city],"bedrom":[bhk]}) 
        pp=pickle.load(open("indhouse.pkl","rb"))  
        
        predict_value=float(pp.predict(da)) 
        predict_value=("%.4f" %predict_value)
         
        return render_template("predict.html",price=predict_value)
        
if __name__==("__main__"):
    apps.run(debug=True)