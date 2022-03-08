import requests
from constantes import API_KEY
from PIL import Image

# This function will pass your text to the machine learning model
# and return the top result with the highest confidence

def storeText(key, text, label):
  #checkApiKey(key)
    
  url = ("https://machinelearningforkids.co.uk/api/scratch/" + 
         key + 
         "/train")

  response = requests.post(url, 
                           json={ "data" : text, "label" : label })

  if response.ok == False:
    # if something went wrong, display the error
    print (response.json())

#Esta función ejecuta la creación de un nuevo modelo de entrenamiento con las palabras nuevas que
#hemos agregado.

def trainModel(key):
  #checkApiKey(key)
  
  url = ("https://machinelearningforkids.co.uk/api/scratch/" + 
         key + 
         "/models")

  response = requests.post(url)

  if response.ok == False:
    # if something went wrong, display the error
    print (response.json())


def checkModel(key):
  #checkApiKey(key)
  
  url = ("https://machinelearningforkids.co.uk/api/scratch/" + 
         key + 
         "/status")

  response = requests.get(url)

  if response.ok:
    responseData = response.json()

    status = {
      2 : "ready to use",
      1 : "training is in progress",
      0 : "problem"
    }

    return { 
      "status" : status[responseData["status"]], 
      "msg" : responseData["msg"] 
    }
  else:
    # if something went wrong, display the error
    print (response.json())



def ingresarNuevoEjemplo(text):
    
    respuestaUsuario = input("¿Quiere añadir la palabra al modelo de entrenamiento? (S/N) ")
    respuestaUsuario = respuestaUsuario.lower()

    if respuestaUsuario == 's':
        print()
        print("Vamos a añadir un nuevo texto, el texto va a ser: ", text)

        etiqueta = input("¿Dónde quieres añadir el ejemplo? (cosas_buenas o cosas_malas)")
        etiqueta = etiqueta.lower()

        if etiqueta == 'cosas_buenas':
            print()
            print("Vamos a añadir", text, "a la etiqueta", etiqueta)
            storeText(API_KEY, text, etiqueta)
            print("Entrenando...")
            trainModel(API_KEY)
            print("Ya está añadida el nuevo texto y entrenado.")

        
        elif etiqueta == 'cosas_malas':
            print()
            print("Vamos a añadir", text, "a la etiqueta", etiqueta)
            storeText(API_KEY, text, etiqueta)
            print("Entrenando...")
            trainModel(API_KEY)
            print("Ya está añadido el nuevo texto y entrenado.")

        else:
            print("La respuesta tiene que ser cosas_buenas o cosas_malas, una de las dos opciones")



    elif respuestaUsuario == 'n':
        print("Has respondido NO")
    
    else:
        print("Tienes que responder con S para Si o con N para No")



def classify(text):
    key = API_KEY
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"
    
    response = requests.get(url, params={ "data" : text })

    if response.ok:
        responseData = response.json()
        confidence = responseData[0]

        print(responseData)
        print()
        
        if confidence['confidence'] >= 60:
            topMatch = responseData[0]
            return topMatch

        else:
            print("No entiendo la respuesta")
            ingresarNuevoEjemplo(text)

    else:
        response.raise_for_status()

def respuesta(recognized):

    label = recognized['class_name']

    if label == "cosas_buenas":
        print("Muchas gracias, eres muy agradable")
        img = Image.open('img/feliz.png')
        #print(img) #<PIL.PngImagePlugin.PngImageFile image mode=RGB size=640x438 at 0x7F0D12A351F0>
        debug=img.show()
        #print(debug)

    else:
        print("No me ha gustado lo que has dicho")
        img = Image.open('img/triste.png')
        #print(img)
        debug=img.show()
        #print(debug)



# Cambiamos a partir de aquí la forma de usar el módelo de entrenamiento. 
#demo = classify("Eres bonito")

#label = demo["class_name"]
#confidence = demo["confidence"]

# CHANGE THIS to do something different with the result
#print ("result: '%s' with %d%% confidence" % (label, confidence))

def run():

    siEntrenado = checkModel(API_KEY)

    if siEntrenado['status'] == 'ready to use':
        texto = input('¿Que quieres decirme? ')

        recognized = classify(texto)
        if recognized != None:
            respuesta(recognized)
    else:
        print(siEntrenado)
    

if __name__ == '__main__':
    run()

   