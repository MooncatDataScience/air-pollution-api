import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import xgboost as xgb
from flask import Flask, render_template, request

app = Flask(__name__)

def predict_model(X_train, y_train, X_test, y_test, model_name):
    if model_name == "Linear Regression":
        model = LinearRegression()
    elif model_name == "Decision Tree":
        model = DecisionTreeRegressor()
    elif model_name == "Random Forest":
        model = RandomForestRegressor()
    elif model_name == "Support Vector Machine":
        model = SVR()
    elif model_name == "Neural Network":
        model = MLPRegressor()
    elif model_name == "XGBoost":
        model = xgb.XGBRegressor()
    if isinstance(model, xgb.XGBRegressor):
        model.fit(X_train, y_train, eval_set=[(X_test, y_test)], early_stopping_rounds=10, verbose=False)
    else:
        model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return {'Model': model_name, 'MAE': mae, 'MSE': mse, 'R2': r2}

def feature_selection(table):
    ds = table[['pm2.5_avg', 'pm10_avg']]
    status = table['aqi']
    return ds, status

def split(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train.astype(float), X_test.astype(float), y_train.astype(float), y_test.astype(float)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model_name = request.form['model']
        results = []
        sites = ['沙鹿', '豐原', '大里', '忠明', '西屯']
        for site in sites:
            df = pd.read_csv("aqi.csv", encoding='utf-8')
            df.fillna(0, inplace=True)

            # Convert publishtime to datetime and extract hour
            df['publishtime'] = pd.to_datetime(df['publishtime'])
            df['hour'] = df['publishtime'].apply(lambda x: x.hour)

            table = df[df['site'] == site]

            # Split data into training and testing sets
            X, y = feature_selection(table)
            X_train, X_test, y_train, y_test = split(X, y)

            # Train and evaluate models
            site_results = predict_model(X_train, y_train, X_test, y_test, model_name)
            site_results['Site'] = site
            results.append(site_results)

        return render_template('predict.html', results=results)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
