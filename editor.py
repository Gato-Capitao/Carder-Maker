from PIL import Image, ImageDraw, ImageFont
from barcode import Code128, writer
from random import randint

def gerarCodigo(value:str):
    """Generate the code on output folder."""
    
    codigo = Code128(value, writer=writer.ImageWriter())
    codigo.save("output/cod")
def adicionarMargem(imagem:Image) -> Image:
    """
    This will add a border on the image
    """
    #Load the border
    margem = Image.open("images/border.png")
    
    #Put the border on image
    margem = margem.convert("RGBA")
    margem = margem.resize(imagem.size)
    
    imagem.paste(margem, (0, 0), margem)
    
    return imagem
def juntar(imagem1:Image, imagem2:Image) -> Image:
    """
    It will join the images.
    """
    #Resize the images
    if imagem1.size != (440, 590):
        imagem1 = imagem1.resize((440, 590))
    if imagem2.size != (440, 590):
        imagem2 = imagem2.resize((440, 590))

    #Join the images
    novaImagem = Image.new("RGBA", (imagem2.size[0]*2, imagem2.size[1]), (250,250,250))

    novaImagem.paste(imagem1, (0, 0))
    novaImagem.paste(imagem2, (imagem2.size[0], 0))
    
    return novaImagem
def adicionarTexto(imagem:Image, texto:str, centerX:bool, centerY:bool, x:int, y:int, fonteArquivo:str, tamanho:int, rgb:tuple) -> Image:
    """
    Add text to ur image
    """
    
    resultado = ImageDraw.Draw(imagem)
    fonte = ImageFont.truetype(font=f"fonts/{fonteArquivo}", size=tamanho)
    
    #Take the measurements
    _, _, caixaX, caixaY = resultado.textbbox((0, 0), texto, font=fonte)
    imagemX, imagemY = imagem.size
    
    #Get the X/Y if centerX/Y
    if centerX:
        x = (imagemX-caixaX)/2
    if centerY:
        y = (imagemY-caixaY)/2
    
    #Add text
    resultado.text((x, y), texto, fill=rgb, font=fonte)
    
    return imagem
def botarCodigo(imagem:Image, centerX:bool, CenterY:bool, y:int, x:int, resize:int) -> Image:
    """
    it will put the barcode on your image.
    """
    #Load the barcode
    cod = Image.open("output/cod.png")
    
    #Resize the barcode
    reX = int((resize*cod.size[0])/100)
    reY = int((resize*cod.size[1])/100)
    cod = cod.resize((reX, reY))
    
    #Center X/Y if necessary
    if centerX:
        x = int((imagem.size[0]-cod.size[0])/2)
    if CenterY:
        y = int((imagem.size[1]-cod.size[1])/2)
    
    #Add the barcode on carder.
    imagem.paste(cod, (x, y))
    
    return imagem
def nomeCartao() -> str:
    """
    It will generate a random carder name.
    """
    caracteres = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    tamanho = randint(1, 20)
    nome = "carder_"
    
    #Generate the name
    while len(nome) < tamanho+7:
        #take a caracter a number
        if randint(0, 1) == 1:
            nome += caracteres[randint(0, len(caracteres)-1)]
        else:
            nome += str(randint(0, 9))
    
    
    return nome