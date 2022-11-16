import flask
import json
import pandas

app1 = flask.Flask("__name__")


@app1.route("/")
def hello():
    return flask.render_template("home.html")


@app1.route("/selectDistrict")
def selectDistrict():
    return flask.render_template("selectDistrict.html")


@app1.route("/getDistrict", methods=["POST"])
def getDistrict():
    city = flask.request.form.get('city')
    print(city, type(city))

    data_url = "https://sip.einvoice.nat.gov.tw/ods-main/ODS308E/download/3886F055-EB77-4DF9-98E2-F3F49A7D3434/1/E265F67E-6CDA-4FB2-B4E9-ACF40ECA3476/0/?fileType=csv"
    data = pandas.read_csv(data_url, encoding='utf8', usecols=[
                           "縣市代碼", "縣市名稱", "鄉鎮市區代碼", "鄉鎮市區名稱", "行業名稱"])
    filter_City = (data["縣市名稱"] == city)
    # 去除該縣市中，重複的區
    dataDistricts = data[filter_City]["鄉鎮市區名稱"].drop_duplicates()
    # dataframe to json
    result = dataDistricts.to_json(orient="values")
    parsed = json.loads(result)
    json_string = json.dumps(parsed, ensure_ascii=False).encode('utf8')
    print("json_string.decode(): ", json_string.decode(), "type: ",
          type(json_string.decode()))  # json_string.decode() is a str

    # convert string to  object
    json_object = json.loads(json_string.decode())
    # check new data type
    print("json_object: ", json_object, "type: ",
          type(json_object))  # json_object is a list
    return json_object


@app1.route("/getCity", methods=["GET"])
def getCity():
    data_url = "https://sip.einvoice.nat.gov.tw/ods-main/ODS308E/download/3886F055-EB77-4DF9-98E2-F3F49A7D3434/1/E265F67E-6CDA-4FB2-B4E9-ACF40ECA3476/0/?fileType=csv"
    data = pandas.read_csv(data_url, encoding='utf8', usecols=["縣市名稱"])
    dataCity = data["縣市名稱"].drop_duplicates()
    result = dataCity.to_json(orient="values")
    parsed = json.loads(result)
    json_string = json.dumps(parsed, ensure_ascii=False).encode('utf8')
    print("json_string.decode(): ", json_string.decode(), "type: ",
            type(json_string.decode())) #json_string.decode() is a str

    #convert string to  object
    json_object = json.loads(json_string.decode())
    #check new data type
    print("json_object: ",json_object,"type: ",type(json_object)) # json_object is a list
    return json_object


if __name__ == "__main__":
    app1.run()
