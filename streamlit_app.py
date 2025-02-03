
import sreamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

import json
key_dict = json.loads(st.secrets["textkey"])
creds= service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="names-project-demo")

dbNames = db.collections("names")

st.header("Nuevo registro")

index = st.text_input("Index")
name = st.text_input("Name")
sex = st.selectbox(
    'Select Sex',
    ('F','M','Other'))

submit = st.button("Crear nuevo registro")

#Once the name has submitted, upload into the database
if index and name and sex and submit:
  doc_ref = db.collection("names").document(name)
  doc_ref.set({
      "index":index,
      "name": name,
      "sex": sex
    })
  st.sidebar.write("Registro insertado correctamente")

names_ref = list(db.collection(u'names').stream())
names_dict = list(map(lambda x: x.to_dict(),names_ref))
names_dataframe = pd.DataFrame(names_dict)
st.dataframe(names_dataframe)

st.header("Buscar registro")

def loadByName(name):
  names_ref= dbNames.where(u'name', u'==' ,name) # se filtra por nombre en la base
  currentName = None
  for myname in names_ref.stream():
    currentName=myname
    return currentName

st.sidebar.subheader("Buscar nombre")
nameSearch = st.sidebar.text_input("nombre")
bntFiltrar = st.sidebar.button("Buscar")



if bntFiltrar:
  doc = loadByName(nameSearch)
  if doc is None:
    st.sidebar.write("nombre no existe")
  else:
    st.sidebar.write(doc.to_dict())


#Eliminacion de documento:
#    a) Crea un boton para la operacion de eliminar
#    b)Si el botón es presionado, llama a la funcion de busqueda para validar existencia de ese documento
#    c) sin no existe enviar mensaje de error
#    d) Si existe crear una referencia al documento y eliminar usando el metodo delete()


st.sidebar.markdown("""___""")
bntEliminar = st.sidebar.button("Eliminar")

if bntEliminar:
  deletename=loadByName(nameSearch)
  if deletename is None:
    st.sidebar.write(f"{nameSearch} no existe")
  else:
    dbNames.document(deletename.id).delete()
    st.sidebar.write(f"{nameSearch} eliminado")

#....
st.sidebar.markdown("___")

# Codificar proceso para actualizar un documento
#   a) Crear un texto para capturar el nuevo nombre
#   b) Crear un boton para actualizar
#   C) Si el boton de actualizacion es presionado llamar a la fundion de busqueda para validar la existencia
#   d) Sino existe mandar mensaje de error
#   e) Si existe crear una referencia al documento y actualizar el campo nombre usando el métod update()
st.sidebar.subheader("Actualizar")
new_name = st.sidebar.text_input("nuevo nombre: ")
bntUpdate = st.sidebar.button("Actualzar")

if bntUpdate:
    updatename=loadByName(nameSearch)
    if updatename is None:
      st.sidebar.write(f"{nameSearch}, no existe")
    else:
      myupdatename=dbNames.document(updatename.id)
      myupdatename.update(
          {
              "name":new_name
          }
      )

