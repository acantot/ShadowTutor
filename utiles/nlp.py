frases_con_huecos=""
frases_normales=""

def procesar(texto_pegado):
    import spacy
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(texto_pegado)
    frases= []
    palabras = []

    for sent in doc.sents:
        if len(sent.text)<90:
            if len(sent.text)>10:
                frases.append(sent.text)

    for token in doc:
        palabras.append(token)

    palabras_y_frases=[]
    palabras_y_frases.append(palabras)
    palabras_y_frases.append(frases)

    return palabras_y_frases

def sub_a_texto(self):
    import pysrt
    subs = pysrt.open(self.fileName_srt[0])
    for sub in subs:
        self.texto += sub.text
    self.texto = self.texto.replace("\n", " ")
    self.texto = self.texto.replace(".", ". ")
    self.texto = self.texto.replace("?", "? ")
    self.texto = self.texto.replace("!", "! ")
    self.texto = self.texto.replace("  ", " ")

def randomize_palabras(palabras):
    import random
    palabras_azar=random.sample(palabras, 4)
    return palabras_azar


def seleccionar_vocabulario(palabras):
    verbos=[]
    adjetivos=[]
    sustantivos=[]
    for token in palabras:
        if len(token) > 2:
            if not token.is_stop:
                if token.is_alpha:
                    if token.pos_ == "VERB":
                        verbos.append(f"to {token.lemma_}")
                    if token.pos_ == "ADJ":
                        adjetivos.append(token.lemma_)
                    if token.pos_ == "NOUN":
                        sustantivos.append(token.lemma_)

    verbos=list(dict.fromkeys(verbos))
    adjetivos=list(dict.fromkeys(adjetivos))
    sustantivos=list(dict.fromkeys(sustantivos))
    vocabulario_final=[]
    vocabulario_final.append(sustantivos)
    vocabulario_final.append(adjetivos)
    vocabulario_final.append(verbos)

    return vocabulario_final