import pyttsx3
import pandas as pd
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import PySimpleGUI as sg

excel=pd.read_excel('Crop.xlsx', header=0)
print(excel)
print(excel.shape)
engine = pyttsx3.init('sapi5')                                            # Defining the speech rate, type of voice etc.
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-20)
engine.setProperty('voice',voices[0].id)


def speak(audio):                                                         # Defining a speak function. We can call this function when we want to make our program to speak something.
   engine.say(audio)
   engine.runAndWait()


le = preprocessing.LabelEncoder()                                         # Various machine learning algorithms require numerical input data, so you need to represent categorical columns in a numerical column. In order to encode this data, you could map each value to a number. This process is known as label encoding, and sklearn conveniently will do this for you using Label Encoder.
crop = le.fit_transform(list(excel["CROP"]))                              # Mapping the values in weather into numerical form.


NITROGEN = list(excel["NITROGEN"])
PHOSPHORUS = list(excel["PHOSPHORUS"])
POTASSIUM = list(excel["POTASSIUM"])
TEMPERATURE = list(excel["TEMPERATURE"])
HUMIDITY = list(excel["HUMIDITY"])
PH = list(excel["PH"])
RAINFALL = list(excel["RAINFALL"])


features = list(zip(NITROGEN, PHOSPHORUS, POTASSIUM, TEMPERATURE, HUMIDITY, PH, RAINFALL))                     # Zipping all the features together
features = np.array([NITROGEN, PHOSPHORUS, POTASSIUM, TEMPERATURE, HUMIDITY, PH, RAINFALL])                    # Converting all the features into a array form

features = features.transpose()                                                                                # Making transpose of the features
print(features.shape)                                                                                          # Printing the shape of the features after getting transposed.
print(crop.shape)                                                                                              # Printing the shape of crop. Please note that the shape of the features and crop should match each other to make predictions.

model = DecisionTreeClassifier()                                                                   # The number of neighbors is the core deciding factor. K is generally an odd number if the number of classes is 2. When K=1, then the algorithm is known as the nearest neighbor algorithm.
model.fit(features, crop)                                                                                      # fit your model on the train set using fit() and perform prediction on the test set using predict().
layout = [[sg.Text('                      Crop Recommendation Assistant', font=("Helvetica", 30), text_color = 'yellow')],                                                    # Defining the layout of the Graphical User Interface. It consist of some text, Buttons, and blanks to take Input.
         [sg.Text('Please enter the following details :-', font=("Helvetica", 20))],                                                                                          # We have defined the text size, font type, font size, blank size, colour of the text in the GUI.
         [sg.Text('Enter ratio of Nitrogen in the soil                                  :', font=("Helvetica", 20)), sg.Input(font=("Helvetica",20), size = (20,1) )],
         [sg.Text('Enter ratio of Phosphorous in the soil                           :', font=("Helvetica", 20)), sg.Input(font=("Helvetica", 20),size = (20,1))],
         [sg.Text('Enter ratio of Potassium in the soil                               :', font=("Helvetica", 20)), sg.Input(font=("Helvetica", 20),size = (20,1))],
         [sg.Text('Enter average Temperature value around the field        :', font=("Helvetica", 20)), sg.Input(font=("Helvetica", 20),size = (20,1)), sg.Text('*C', font=("Helvetica", 20))],
         [sg.Text('Enter average percentage of Humidity around the field :', font=("Helvetica", 20)), sg.Input(font=("Helvetica", 20),size = (20,1)), sg.Text('%', font=("Helvetica", 20))],
         [sg.Text('Enter PH value of the soil                                            :', font=("Helvetica", 20)), sg.Input(font=("Helvetica", 20),size = (20,1))],
         [sg.Text('Enter average amount of Rainfall around the field        :', font=("Helvetica", 20) ), sg.Input(font=("Helvetica", 20),size = (20,1)),sg.Text('mm', font=("Helvetica", 20))],
         [sg.Text(size=(50,1),font=("Helvetica",20) , text_color = 'yellow', key='-OUTPUT1-' )],
         [sg.Button('Submit', font=("Helvetica", 20)),sg.Button('Quit', font=("Helvetica", 20))] ]
window = sg.Window('Crop Recommendation Assistant', layout)

while True:
   event, values = window.read()
   if event == sg.WINDOW_CLOSED or event == 'Quit':                                                                                            # If the user will press the quit button then the program will end up.
      break
   print(values[0])
   nitrogen_content =         values[0]                                                                                                        # Taking input from the user about nitrogen content in the soil.
   phosphorus_content =       values[1]                                                                                                        # Taking input from the user about phosphorus content in the soil.
   potassium_content =        values[2]                                                                                                        # Taking input from the user about potassium content in the soil.
   temperature_content =      values[3]                                                                                                        # Taking input from the user about the surrounding temperature.
   humidity_content =         values[4]                                                                                                        # Taking input from the user about the surrounding humidity.
   ph_content =               values[5]                                                                                                        # Taking input from the user about the ph level of the soil.
   rainfall =                 values[6]                                                                                                        # Taking input from the user about the rainfall.
   predict1 = np.array([nitrogen_content, phosphorus_content, potassium_content, temperature_content, humidity_content, ph_content, rainfall],dtype=float)  # Converting all the data that we collected from the user into a array form to make further predictions.
   print(predict1)                                                                                                                             # Printing the data after being converted into a array form.
   predict1 = predict1.reshape(1, -1)                                                                              # Reshaping the input data so that it can be applied in the model for getting accurate results.
   print(predict1)                                                                                                # Printing the input data value after being reshaped.
   predict1 = model.predict(predict1)                                                                             # Applying the user input data into the model.
   print(predict1)                                                                                                # Finally printing out the results.
   crop_name = str()
   if predict1 == 0:                                                                                              # Above we have converted the crop names into numerical form, so that we can apply the machine learning model easily. Now we have to again change the numerical values into names of crop so that we can print it when required.
      crop_name = 'Apple(सेब)(ஆப்பிள்)'
   elif predict1 == 1:
      crop_name = 'Banana(केला)(வாழை)'
   elif predict1 == 2:
      crop_name = 'Blackgram(काला चना)(உளுந்து)'
   elif predict1 == 3:
      crop_name = 'Chickpea(काबुली चना)(சுண்டல்)'
   elif predict1 == 4:
      crop_name = 'Coconut(नारियल)(தேங்காய்)'
   elif predict1 == 5:
      crop_name = 'Coffee(कॉफ़ी)(காபி பயிர்)'
   elif predict1 == 6:
      crop_name = 'Cotton(कपास)(பருத்தி)'
   elif predict1 == 7:
      crop_name = 'Grapes(अंगूर)(திராட்சை)'
   elif predict1 == 8:
      crop_name = 'Jute(जूट)(சணல்)'
   elif predict1 == 9:
      crop_name = 'Kidneybeans(राज़में)(கிட்னி பீன்ஸ்)'
   elif predict1 == 10:
      crop_name = 'Lentil(मसूर की दाल)(பருப்பு)'
   elif predict1 == 11:
      crop_name = 'Maize(मक्का)(சோளம்)'
   elif predict1 == 12:
      crop_name = 'Mango(आम)(மாங்கனி)'
   elif predict1 == 13:
      crop_name = 'Mothbeans(मोठबीन)(அந்துப்பூச்சி பீன்ஸ்)'
   elif predict1 == 14:
      crop_name = 'Mungbeans(मूंग)(பாசிப்பயறு)'
   elif predict1 == 15:
      crop_name = 'Muskmelon(खरबूजा)(முலாம்பழம்)'
   elif predict1 == 16:
      crop_name = 'Orange(संतरा)(ஆரஞ்சு)'
   elif predict1 == 17:
      crop_name = 'Papaya(पपीता)(பப்பாளி)'
   elif predict1 == 18:
      crop_name = 'Pigeonpeas(कबूतर के मटर)(துவரை)'
   elif predict1 == 19:
      crop_name = 'Pomegranate(अनार)(மாதுளை)'
   elif predict1 == 20:
      crop_name = 'Rice(चावल)(அரிசி)'
   elif predict1 == 21:
      crop_name = 'Watermelon(तरबूज)(தர்பூசணி)'

   if int(humidity_content) >=1 and int(humidity_content)<= 33 :
      humidity_level = 'low humid'
   elif int(humidity_content) >=34 and int(humidity_content) <= 66:
      humidity_level = 'medium humid'
   else:
      humidity_level = 'high humid'

   if int(temperature_content) >= 0 and int(temperature_content)<= 6:
      temperature_level = 'cool'
   elif int(temperature_content) >=7 and int(temperature_content) <= 25:
      temperature_level = 'warm'
   else:
      temperature_level= 'hot'

   if int(rainfall) >=1 and int(rainfall) <= 100:
      rainfall_level = 'less'
   elif int(rainfall) >= 101 and int(rainfall) <=200:
      rainfall_level = 'moderate'
   elif int(rainfall) >=201:
      rainfall_level = 'heavy rain'

   if int(nitrogen_content) >= 1 and int(nitrogen_content) <= 50:
      nitrogen_level = 'less'
   elif int(nitrogen_content) >=51 and int(nitrogen_content) <=100:
      nitrogen_level = 'not to less but also not to high'
   elif int(nitrogen_content) >=101:
      nitrogen_level = 'high'

   if int(phosphorus_content) >= 1 and int(phosphorus_content) <= 50:
      phosphorus_level = 'less'
   elif int(phosphorus_content) >= 51 and int(phosphorus_content) <=100:
      phosphorus_level = 'not to less but also not to high'
   elif int(phosphorus_content) >=101:
      phosphorus_level = 'high'

   if int(potassium_content) >= 1 and int(potassium_content) <=50:
      potassium_level = 'less'
   elif int(potassium_content) >= 51 and int(potassium_content) <= 100:
      potassium_level = 'not to less but also not to high'
   elif int(potassium_content) >=101:
      potassium_level = 'high'

   if float(ph_content) >=0 and float(ph_content) <=5:
      phlevel = 'acidic'
   elif float(ph_content) >= 6 and float(ph_content) <= 8:
      phlevel = 'neutral'
   elif float(ph_content) >= 9 and float(ph_content) <= 14:
    phlevel = 'alkaline'

print(crop_name)
print(humidity_level)
print(temperature_level)
print(rainfall_level)
print(nitrogen_level)
print(phosphorus_level)
print(potassium_level)
print(phlevel)

speak("Sir according to the data that you provided to me. The ratio of nitrogen in the soil is  " + nitrogen_level + ". The ratio of phosphorus in the soil is  " + phosphorus_level + ". The ratio of potassium in the soil is  " + potassium_level + ". The temperature level around the field is  " + temperature_level + ". The humidity level around the field is  " + humidity_level + ". The ph type of the soil is  " + phlevel + ". The amount of rainfall is  " + rainfall_level )
window['-OUTPUT1-'].update('The best crop that you can grow : ' + crop_name )
speak("The best crop that you can grow is  " + crop_name)
from twilio.rest import Client

account_sid = 'ACeb1979425edec51ce5dcde07f58cdc9c'
auth_token = 'a0c91721cafeaf9ce922871af1d1a959'

client = Client(account_sid, auth_token)
message = client.messages \
   .create(
   body= "Sir according to the data that you provided to me. The ratio of nitrogen in the soil is  " + nitrogen_level + ". The ratio of phosphorus in the soil is  " + phosphorus_level + ". The ratio of potassium in the soil is  " + potassium_level + ". The temperature level around the field is  " + temperature_level + ". The humidity level around the field is  " + humidity_level + ". The ph type of the soil is  " + phlevel + ". The amount of rainfall is  " + rainfall_level+".The best crop that you can grow : "+ crop_name ,
   from_='+16504204677',
   to='+919345444811'
)
print(message.sid)
window.close()