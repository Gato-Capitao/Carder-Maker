"""
Made by: https://github.com/Gato-Capitao

----Master Carder----
Abstract: A software that can make 

Introduction: a project for students at my school where they could create 
their own personalized cards and use at school. 
These cards are used to get lunch, 
and you need to have a barcode with the student's registration number.

Objective: that the user can make small edits simply and quickly, 
in order to create a card. It also has the function of generating a barcode.

--Instructions--
1-Put the images you want to edit in the "input" folder.
These are the images that the program will be able to select.

2-When u save ur project it will be in "output" folder.

3-If u want write something u need to put the font file in the "fonts" folder.
The only font format is True Type. Ex: font.ttf

4-U can delete the "temp" folder when ur project is saved.
"""
import PySimpleGUI as sg
from PIL import Image, ImageTk
from editor import adicionarMargem, adicionarTexto, botarCodigo, juntar, nomeCartao, gerarCodigo
from os import listdir, getcwd, mkdir
from requests import get


def criarPastas():
    #This function will create all the necessary folders for the program.
    """
    Explanation: it checks if the necessary folders are in the directory. 
    If the folder is not in the directory, it will create it. 
    If any of the necessary files (like the icon) is not found, it will download.
    """

    def baixarBorda():
        with open("images/border.png", "wb") as arquivo:
            pagina = get("https://filedropper.com/d/s/download/uWmcVAC4CjfpHTzk6YuHzR7jP3xSnD")
            arquivo.write(pagina.content)
    def baixarIcone():
        with open("images/masterCarderIcon.ico", "wb") as arquivo:
            pagina = get("https://filedropper.com/d/s/download/DpJR186hXFET4wgBjAIafTvplIM3wa")
            arquivo.write(pagina.content)
    endereco = getcwd()
    pastas = listdir(endereco)
    if not "images" in pastas:
        mkdir(endereco+"/images")
        baixarBorda()
        baixarIcone()
    else:
        arquivos = listdir(endereco+"/images")
        if not "border.png" in arquivos:
            baixarBorda()
        if not "masterCarderIcon.ico" in arquivos:
            baixarIcone()
    if not "input" in pastas:
        mkdir(endereco+"/input")
    if not "temp" in pastas:
        mkdir(endereco+"/temp")
    if not "output" in pastas:
        mkdir(endereco+"/output")
    if not "fonts" in pastas:
        mkdir(endereco+"/fonts")
criarPastas()
padraoSize = (440, 590)#Base size used for the images
dadosCapa = {"nome":"", "imagem":None}
dadosCartao = {"nome":"", "imagem":None}
icone = "images/masterCarderIcon.ico"


########################################
"""
Folders are put in lists(Just the name of their files).
This will be used to find the files directory when needed.
"""
fontes = listdir(getcwd()+"/fonts")
imagens = listdir(getcwd()+"/images")
inputPasta = listdir(getcwd()+"/input")
########################################

def layout_principal() -> sg.Window:
    """
    It will return the main window, 
    which is a set of various objects in lists, separated by tabs and frames.
    Each window component has a key that can be used to identify an object event or get some value from it.
    """
    def layout_capa() -> list:
        """
        This will return the Front tab.
        It serves to edit only a part of the complete card, where you can add text and barcode.
        """
        #####Barcode Layout######
        tab_codigo = [
            [sg.Text("Cod"), sg.Input(key="entrada_numCodigo", size=(10, 1)), sg.Button("Create", key="botao_createCod")],
            [sg.Text("Size"), sg.Input(key="entrada_sizeCod", size=(5, 1), default_text="70")],
            [sg.Text("X"), sg.Input(key="entrada_xCod", size=(3, 1), default_text="0"), sg.Text("Y"), sg.Input(key="entrada_yCod", size=(3, 1), default_text="0")],
            [sg.Checkbox(text="Center X", key="check_centerXCod"), sg.Checkbox(text="Center Y", key="check_centerYCod")],
            [sg.Button("Confirm", key="botao_confirmCod"), sg.Button("Add", key="botao_addCod"), sg.Button("Remove", key="botao_removeCod")]
        ]
        #########################
        
        
        #####Add text layout#####
        frame_texto = [
            [sg.Text(text="Text"), sg.Input(key="entrada_text", size=(24, 1))],
            [sg.Text("Font"), sg.Combo(values=fontes, key="combo_font", size=(10, 1)), sg.Text("Size"), sg.Input(key="entrada_sizeText", size=(3, 1), default_text="25")],
            [sg.Text("X"), sg.Input(key="entrada_xText", size=(3, 1), default_text="0"), sg.Text("Y"), sg.Input(key="entrada_yText", size=(3, 1), default_text="0")],
            [sg.Checkbox(text="Center X", key="check_centerXText"), sg.Checkbox(text="Center Y", key="check_centerYText")],
            [sg.Button("Confirm", key="botao_confirmText"), sg.Button("Add", key="botao_addText"), sg.Button("Remove", key="botao_removeText")]
        ]
        #The layout of the frame that you can choose the color of the text
        frame_detalhes = [
            [sg.Text("R"), sg.Slider((0, 255), key="slider_colorRText", orientation="horizontal")],
            [sg.Text("G"), sg.Slider((0, 255), key="slider_colorGText", orientation="horizontal")],
            [sg.Text("B"), sg.Slider((0, 255), key="slider_colorBText", orientation="horizontal")],
            [sg.Image(key="image_corText")]
        ]
        #The layout of the tab that you can add text
        tab_texto = [[sg.Frame(title="Add Text", layout=frame_texto), sg.Frame(title="Colors", layout=frame_detalhes)]]
        
        #########################
        
        #######Main layout#######
        layout = [
            [sg.TabGroup([[sg.Tab("Text", tab_texto), sg.Tab("Cod", tab_codigo)]])],
            [sg.Text("File"), sg.Combo(values=inputPasta, key="combo_imagemCarregar", size=(30, 1), enable_events=True), sg.Button("Refresh", key="botao_refreshFront")],
            [sg.Push(), sg.Image(key="capa", size=(int(padraoSize[0]/2), int(padraoSize[1]/2))), sg.Push()],
            [sg.Button("save", key="botao_saveFront")]
            ]
        #########################
        
        return layout
    
    def layout_Juntar() -> list:
        """
        It will return the Carder layout.
        This layout servers to join 2 images, and put border if u want.
        """
        
        ########Load Frame#######
        frame_mudancas = [
            [sg.Text("Front"), sg.Combo(values=inputPasta, size=(10, 1), key="combo_front")],
            [sg.Text("Back"), sg.Combo(values=inputPasta, size=(10, 1), key="combo_back")],
            [sg.Button("Create", key="botao_createCarder"), sg.Button("Refresh", key="botao_refreshCarder")]
            ]
        #########################
        
        ########Add border#######
        frame_margem = [
            [sg.Button("Add", key="botao_addBorder"), sg.Button("Remove", key="botao_removeBorder")]
        ]
        #########################
        
        #######Main layout#######
        layout = [
            [sg.Push(), sg.Frame("Images", frame_mudancas), sg.Frame("Border", frame_margem), sg.Push()],
            [sg.VPush()],
            [sg.Push(), sg.Image(key="cartao", size=(padraoSize[0], int(padraoSize[1]/2))), sg.Push()],
            [sg.VPush()],
            [sg.Button("Save", key="botao_saveCarder"), sg.Push()]
        ]
        #########################
        
        return layout
    
    #The main layout
    """
    This has the tabs that contain the others layouts on it.
    """
    layout = [
        [sg.TabGroup([[sg.Tab("Front", layout=layout_capa()), sg.Tab("Carder", layout=layout_Juntar())]])]
    ]
    return sg.Window(title="Card Creater", layout=layout, finalize=True, grab_anywhere=True, icon=icone)
def converterParaMostrar(imagem:Image, tip:int = 1) -> ImageTk.PhotoImage:
    """
    This will convert a variable of type Image to PhotoImage, so that it can appear on the screen.
    This will resize the imagem to a suitable size for the screen, which is half the original size.
    """
    
    #Resizing images#
    if tip == 1:
        imagem = imagem.resize((int(padraoSize[0]/2), int(padraoSize[1]/2)))
    else:
        imagem = imagem.resize((padraoSize[0], int(padraoSize[1]/2)))
    #################
    
    return ImageTk.PhotoImage(imagem)
def abrirImagem(diretorio:str) -> Image:
    """
    This will open the image and turn it with the default settings
    """
    imagem = Image.open(diretorio)
    imagem = imagem.resize((440, 590))
    
    return imagem
def recarregarImagens():
    """
    It will reload the files available in the input folder and update the combos.
    
    Fuction: it server in case an image is added to input folder after
    the program has been executed, then u need to reload the data and update the combos.
    """
    inputPasta = listdir(getcwd()+"/input")
    janela["combo_imagemCarregar"].update(values=inputPasta)
    janela["combo_front"].update(values=inputPasta)
    janela["combo_back"].update(values=inputPasta)


janela = layout_principal()

while True:
    evento, valor = janela.read()
    if evento == sg.WINDOW_CLOSED:
        #if the X in the window was pressed
        break
    #Tab Front
    elif evento == "combo_imagemCarregar":
        #It will load the image to be edited.
        """
        --Algorithm--
        1-Open the image from input folder.
        2-Save the file name and the image
        3-Convert Image to PhotoImage to show it on screen
        """
        try:
            dadosCapa["imagem"] = abrirImagem(f"input/{valor['combo_imagemCarregar']}")
            
            dadosCapa["nome"] = valor["combo_imagemCarregar"]
            mostrar = converterParaMostrar(dadosCapa["imagem"], 1)
            janela["capa"].update(data=mostrar)
            dadosCapa["imagem"].save(f"temp/{valor['combo_imagemCarregar']}")
        except:
            sg.popup("Error trying to load image. Make sure the image format is in PNG, and restart the program.")
    elif evento == "botao_addText":
        #Add text to a image
        """
        --Algorithm--
        1-Check if the center X or the center Y was marked. 
        If it's true, it will don't matter about the x or y values.
        
        2-Add the text to image.
        
        3-Show the image on screen.
        """
        try:
            if valor["check_centerXText"]:
                valor["entrada_xText"] = "0"
            if valor["check_centerYText"]:
                valor["entrada_yText"] = "0"
            dadosCapa["imagem"] = adicionarTexto(dadosCapa["imagem"], valor["entrada_text"], valor["check_centerXText"], valor["check_centerYText"],int(valor["entrada_xText"]), int(valor["entrada_yText"]), valor["combo_font"], int(valor["entrada_sizeText"]), (int(valor["slider_colorRText"]), int(valor["slider_colorGText"]), int(valor["slider_colorBText"])))
            janela["capa"].update(data=converterParaMostrar(dadosCapa["imagem"], 1))
        except:
            sg.popup("An error occurred when trying to add the text, check if you filled in the data correctly")
    elif evento == "botao_removeText":
        #This will remove the unconfirmed editions.
        """
        Explain: return to the last image that u have saved on temp folder.
        
        --Algorithm--
        1-Open the image from temp.
        2-Show the image.
        """
        try:
            dadosCapa["imagem"] = Image.open(f"temp/{dadosCapa['nome']}")
            janela["capa"].update(data=converterParaMostrar(dadosCapa["imagem"], 1))
        except:
            sg.popup("Error removing the text, check if the image save is in temp folder.")
    elif evento == "botao_confirmText":
        #This will save ur image on temp folder.
        """
        Explanation: To confirm ur edition we need to save ur image temporaly.
        Confirmed edition can't be removed.
        """
        try:
            dadosCapa["imagem"].save(f"temp/{dadosCapa['nome']}")
        except:
            sg.popup("Error saving image, make a little update on image and try again.")
    elif evento == "botao_saveFront":
        #Save ur image on output folder.
        try:
            dadosCapa["imagem"].save(f"output/carder_{dadosCapa['nome']}")
        except:
            sg.popup("Error saving image, verify if the original image name is valid.")
    elif evento == "botao_refreshFront":
        #this will reload the files from input folders.
        try:
            recarregarImagens()
        except:
            sg.popup('Error loading files, check if "input" folder is in this directory')
    elif evento == "botao_confirmCod":
        #This will confirm the barcode on image,
        #once u do this u will not be able to remove the barcode.
        try:
            dadosCapa["imagem"].save(f"temp/{dadosCapa['nome']}")
        except:
            sg.popup('Error applying the effect, verify if the folder "temp" is on this directory.')
    elif evento == "botao_addCod":
        #Add barcode to a image
        """
        --Algorithm--
        1-Check if the center X or the center Y was marked. 
        If it's true, it will don't matter about the x or y values.
        
        2-Add the barcode to image.
        
        3-Show the image on screen.
        """
        try:
            if valor["check_centerXCod"]:
                valor["entrada_xCod"] = "0"
            if valor["check_centerYCod"]:
                valor["entrada_yCod"] = "0"
            dadosCapa["imagem"] = botarCodigo(dadosCapa["imagem"], valor["check_centerXCod"], valor["check_centerYCod"], int(valor["entrada_yCod"]), int(valor["entrada_xCod"]), int(valor["entrada_sizeCod"]))
            janela["capa"].update(data=converterParaMostrar(dadosCapa["imagem"], 1))
        except:
            sg.popup("Error adding barcode, check if barcode was generated.")
    elif evento == "botao_removeCod":
        #This will reload ur last confirmed edition.
        """
        --Algorithm--
        1-Open the image from temp folder.
        2-show the image on screen.
        """
        try:
            dadosCapa["imagem"] = Image.open(f"temp/{dadosCapa['nome']}")
            janela["capa"].update(data=converterParaMostrar(dadosCapa["imagem"], 1))
        except:
            sg.popup('Error removing the barcode, check if the save of project is in the folder named "temp".')
    elif evento == "botao_createCod":
        #This will generate ur code and save it in output folder.
        try:
            gerarCodigo(valor["entrada_numCodigo"])
        except:
            pass
    
    #Tab Carder
    elif evento == "botao_createCarder":
        #This will generate the carder
        """
        --Algorithm--
        1-Get the name of carder
        2-Collect as images
        3-Join the images
        4-Show the carder
        """
        try:
            #Get the name of carder
            dadosCartao["nome"] = nomeCartao()
            
            #Collect as images
            img1 = Image.open(f"input/{valor['combo_front']}")
            img2 = Image.open(f"input/{valor['combo_back']}")
            
            #Join the images
            dadosCartao["imagem"] = juntar(img1, img2)
            dadosCartao["imagem"].save(f"temp/{dadosCartao['nome']}.png")
            
            #Show the carder
            mostrar = converterParaMostrar(dadosCartao["imagem"], 2)
            janela["cartao"].update(data=mostrar)
        except:
            sg.popup('Error loading images, check that both are PNG and that they are in the input folder.')
    elif evento == "botao_addBorder":
        #This will add border to the carder
        """
        --Algorithm--
        1-Add border to image.
        2-Update the image on screen.
        """
        try:
            dadosCartao["imagem"] = adicionarMargem(dadosCartao["imagem"])
            
            mostrar = converterParaMostrar(dadosCartao["imagem"], 2)
            janela["cartao"].update(data=mostrar)
        except:
            sg.popup('Error adding border, check if the "border.png" file is in the "images" folder, otherwise restart the program.')
    elif evento == "botao_removeBorder":
        #Remove the border from image
        """
        --Algorithm--
        1-Load the image from temp folder.
        2-Update the image on screen.
        """
        try:
            dadosCartao["imagem"] = Image.open(f"temp/{dadosCartao['nome']}.png")
            
            mostrar = converterParaMostrar(dadosCartao["imagem"], 2)
            janela["cartao"].update(data=mostrar)
        except:
            sg.popup('Error removing the border, check if the save of project is in the folder named "temp".')
    elif evento == "botao_saveCarder":
        #This will save the image on output folder.
        try:
            dadosCartao["imagem"].save(f"output/{dadosCartao['nome']}.png")
        except:
            sg.popup('Error saving the project, just try again.')
    elif evento == "botao_refreshCarder":
        #this will reload the files from input folders.
        try:
            recarregarImagens()
        except:
            sg.popup('Error loading files, check if "input" folder is in this directory')

