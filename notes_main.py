from PyQt5.QtCore import Qt
from PyQt5.QtWidgets  import  QApplication,  QWidget,  QPushButton,  QLabel,  QListWidget,  QLineEdit,  QTextEdit,  QInputDialog,  QHBoxLayout,  QVBoxLayout 
import json


nota = {}


app_note = QApplication([])
note_ventana = QWidget()
note_ventana.setWindowTitle("notas")

layout_prin = QHBoxLayout()
layout_vert1 = QVBoxLayout()
layout_vert2 = QVBoxLayout()

layout_aux1 =QHBoxLayout() 
layout_aux2 =QHBoxLayout()

cuerpo_note = QTextEdit()

list_nota = QListWidget()
list_nota_label = QLabel("lista de nota")

new_nota = QPushButton("crear nueva nota")
del_note = QPushButton("eliminar nota")
save_note = QPushButton("salvar nota")

list_tags = QListWidget()
list_tags_label = QLabel("lista de etiqueta")

tag_finder =QLineEdit()
tag_finder.setPlaceholderText('Ingresar  etiqueta…') 
new_tag = QPushButton("crear nueva etiqueta")
del_tag = QPushButton("eliminar etiqueta")
search_tag = QPushButton("buscar etiqueta")

layout_vert1.addWidget(list_nota_label)
layout_vert1.addWidget(list_nota)

layout_aux1.addWidget(new_nota)
layout_aux1.addWidget(del_note)
layout_vert1.addLayout(layout_aux1)
layout_vert1.addWidget(save_note)
layout_vert1.addWidget(list_tags_label)

layout_vert1.addWidget(list_tags)
layout_vert1.addWidget(tag_finder)

layout_aux2.addWidget(new_tag)
layout_aux2.addWidget(del_tag)
layout_vert1.addLayout(layout_aux2)
layout_vert1.addWidget(search_tag)

layout_vert2.addWidget(cuerpo_note)

layout_prin.addLayout(layout_vert2,stretch=2)
layout_prin.addLayout(layout_vert1,stretch=1)

def mostrar_nota():
    key = list_nota.selectedItems()[0].text()
    cuerpo_note.setText(nota[key]["texto"])
    list_tags.clear()
    list_tags.addItems(nota[key]["etiqueta"])

def nueva_nota():
    note_name, ok = QInputDialog.getText(note_ventana,'Añadir nota', 'nombre de nota:')
    if ok and note_name != '':
        nota[note_name] = {'texto':'','etiqueta': []}
        list_nota.addItem(note_name)
        list_tags.clear()

note_ventana.setLayout(layout_prin)


with open('notas.json', 'r') as file:
    nota = json.load(file)

def guardar_nota():
    if list_nota.selectedItems():
        key = list_nota.selectedItems()[0].text()
        nota[key]['texto'] = cuerpo_note.toPlainText()
        with open('notas.json', 'w') as file:
            json.dump(nota,file,sort_keys= True)
    else:
        print("nada seleccionado")



def borrar_nota():
    if list_nota.selectedItems():
        key = list_nota.selectedItems()[0].text()
        del nota[key]
        list_nota.clear()
        list_tags.clear()
        cuerpo_note.clear()
        list_nota.addItems(nota)
        with open('notas.json', 'w') as file:
            json.dump(nota,file,sort_keys= True)
    else:
        print("nada seleccionado")
        
def add_tag():
    if list_nota.selectedItems():
        key = list_nota.selectedItems()[0].text()
        tag = tag_finder.text()
        if not tag in nota[key]['etiqueta'] and tag !='':
            nota[key]['etiqueta'].append(tag)
            list_tags.addItem(tag)
            tag_finder.clear()
        with open('notas.json', 'w') as file:
            json.dump(nota,file,sort_keys= True)
    else:
        print("no a selecionado nada")

def borrar_tag():
    if list_nota.selectedItems():
        key = list_nota.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        nota[key]['etiqueta'].remove(tag)
        list_tags.clear()
        list_tags.addItems(nota[key]["etiqueta"])
        with open('notas.json', 'w') as file:
            json.dump(nota,file,sort_keys= True)
    else:
        print("no a selecionado nada")


list_nota.addItems(nota)
list_nota.itemClicked.connect(mostrar_nota)
new_nota.clicked.connect(nueva_nota)
save_note.clicked.connect(guardar_nota)
del_note.clicked.connect(borrar_nota)
new_tag.clicked.connect(add_tag)
del_tag.clicked.connect(borrar_tag)
note_ventana.show()
app_note.exec()
