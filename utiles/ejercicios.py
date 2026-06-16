from PySide6.QtCore import QSize

def siguiente(self):
    self.i+=1
    ejercicios(self)
    return self.i
    
def anterior(self):
    self.i-=1
    ejercicios(self)
    self.boton_siguiente.setText("Next phase")
    self.boton_siguiente.clicked.disconnect()
    self.boton_siguiente.clicked.connect(lambda: siguiente(self))
    return self.i

def siguiente_subejercicio(self):
    self.subindice+=1
    if self.subindice==len(self.subtitulos_texto)-1:
        self.boton_extracto_siguiente.hide()
    if self.subindice>0:
        self.boton_extracto_anterior.show()
    if self.subindice >= self.numero_limite:
        cambio(self, self.enunciados_ejercicios_shadowing)
    self.fabrica_de_hilos(self.archivos[self.subindice], self.caja_subtitulos, self.subindice, self.subtitulos_texto, "no")

def siguiente_subejercicio_TBLT(self):
    self.indice_tlbt+=1
    cambio(self, self.enunciados_TBLT)

def anterior_subejercicio_TBLT(self):
    self.indice_tlbt-=1
    cambio(self, self.enunciados_TBLT)
  
def anterior_subejercicio(self):
    if self.subindice!=len(self.subtitulos_texto):
        self.boton_extracto_siguiente.show()
    self.subindice-=1
    if self.subindice==0:
        self.boton_extracto_anterior.hide()
    self.fabrica_de_hilos(self.archivos[self.subindice], self.caja_subtitulos, self.subindice, self.subtitulos_texto, "no")

def ejercicios(self):
    self.instrucciones.setIconSize(QSize(25, 25))
    if self.i==1:
        asimilación_del_audio(self)
    if self.i==2:
        ejercicios_de_shadowing(self)
    if self.i==3:
        tlbt(self)

def asimilación_del_audio(self):
    abrir_media(self.archivo_video)
    abrir_media(self.archivo_subs)
    self.instrucciones.setText("Listen twice. If you need to, read the subtitles.")
    self.boton_repetir.clicked.connect(lambda: abrir_media(self.archivo_video))
    self.boton_repetir.clicked.connect(lambda: abrir_media(self.archivo_subs))
    self.instrucciones.setIcon(self.icono_cascos)
    self.partes.setText(f"Phase {self.i}: Listening")
    self.boton_repetir.show()
    self.boton_tts.hide()
    self.boton_anterior.hide()
    self.boton_extracto_anterior.hide()
    self.boton_extracto_siguiente.hide()

def ejercicios_de_shadowing(self):
    self.boton_anterior.show()
    self.boton_siguiente.show()
    from .extract import parse_subtitle_file, audio_y_subs
    self.boton_extracto_anterior.setText("Previous extract")
    self.boton_extracto_siguiente.setText("Next extract")
    self.boton_repetir.show()
    self.subtitulos = parse_subtitle_file(self.archivo_subs, 300)
    self.archivos=audio_y_subs(self.subtitulos[0], self.archivo_video)
    self.subtitulos_texto=self.subtitulos[1]
    self.boton_repetir.clicked.disconnect()
    self.boton_repetir.clicked.connect(lambda: self.fabrica_de_hilos(self.archivos[self.subindice], self.caja_subtitulos, self.subindice, self.subtitulos_texto, "no"))
    cambio(self, self.enunciados_ejercicios_shadowing)
    self.fabrica_de_hilos(self.archivos[self.subindice], self.caja_subtitulos, self.subindice, self.subtitulos_texto, "no")
    self.boton_tts.show()
    self.boton_tts.clicked.connect(lambda: tts(self, "media_temp/tts_temp.wav", self.caja_subtitulos, self.subindice, self.subtitulos_texto, "sí"))
    self.instrucciones.setIcon(self.icono_cascos)
    self.partes.setText(f"Phase {self.i}: Shadowing")
    self.boton_extracto_siguiente.show()
    self.boton_repetir.setText("Again")

def tlbt(self):
    self.boton_extracto_anterior.setText("Previous exercise")
    self.boton_extracto_siguiente.setText("Next exercise")
    cambio(self, self.enunciados_TBLT)
    self.boton_tts.hide()
    self.instrucciones.setIcon(self.burbuja_icono)
    self.partes.setText(f"Last phase: TBLT")
    self.boton_siguiente.setText("Finish")
    self.boton_siguiente.clicked.disconnect()
    self.boton_siguiente.clicked.connect(fin)
    self.boton_extracto_anterior.hide()
    self.boton_extracto_siguiente.show()
    self.boton_extracto_siguiente.clicked.disconnect()
    self.boton_extracto_anterior.clicked.disconnect()
    self.boton_repetir.clicked.disconnect()
    self.boton_repetir.clicked.connect(lambda: cambio(self, self.enunciados_TBLT))
    self.boton_extracto_siguiente.clicked.connect(lambda: siguiente_subejercicio_TBLT(self))
    self.boton_extracto_anterior.clicked.connect(lambda: anterior_subejercicio_TBLT(self))

def abrir_media(archivo_multimedia):
    from os import startfile
    startfile(archivo_multimedia)

def grabar(caja_subtitulos, segundos, subs):
    from scipy.io.wavfile import write
    import sounddevice as sd
    freq = 44100
    recording = sd.rec(int(segundos * freq), 
					samplerate=freq, channels=2)
    caja_subtitulos.setText(f"[ Recording ... ]\n\n [ {subs} ] ")
    sd.wait()
    write("media_temp/recording.mp3", freq, recording)
    caja_subtitulos.setText("[ Recording complete ]")
    leer()

def leer():
    import soundfile as sf
    import sounddevice as sd
    import os
    data, samplerate = sf.read("media_temp/recording.mp3")
    sd.play(data, samplerate)
    if os.path.exists("recording.mp3"):
        os.remove("recording.mp3")

def cambio(self, enunciado):
    import random
    self.numero_limite+=5
    self.ejercicio_elegido=random.choice(enunciado)
    self.instrucciones.setText(self.ejercicio_elegido)
    if enunciado==self.enunciados_ejercicios_shadowing:
        if random.randint(1, 1)==1:
            self.variante_elegida=random.choice(self.mas_variantes_shadowing)
            self.instrucciones_finales=self.ejercicio_elegido+self.variante_elegida
            self.instrucciones_finales = self.instrucciones_finales.replace("\n", " ")
            self.instrucciones.setText(f"{self.instrucciones_finales}")
    else:
        subejercicio_tlbt(self)
        if self.indice_tlbt==1:
            self.boton_extracto_anterior.hide()
        else:
            self.boton_extracto_anterior.show()
        if self.indice_tlbt==self.numero_ejercicios_tlbt:
            self.boton_extracto_siguiente.hide()
        else:
            self.boton_extracto_siguiente.show()

def tts(self, archivos, texto_caja, subindice, subs, tts):
    from gtts import gTTS
    tts_generado = gTTS(subs[subindice])
    tts_generado.save(archivos)
    self.fabrica_de_hilos(archivos, texto_caja, subindice, subs, tts)

def subejercicio_tlbt(self):
    self.caja_subtitulos.setText(None)
    if "sentence" in self.ejercicio_elegido:
        frases_tlbt(self)
    if "word" in self.ejercicio_elegido:
        palabras_tlbt(self)

def palabras_tlbt(self):
    import random
    palabras_totales=[]
    palabras_str=""
    sustantivos_azar=random.sample(self.palabras[0], 2)
    adjetivos_azar=random.sample(self.palabras[1], 2)
    verbos_azar=random.sample(self.palabras[2], 2)
    palabras_totales.extend(sustantivos_azar)
    palabras_totales.extend(adjetivos_azar)
    palabras_totales.extend(verbos_azar)
    random.shuffle(palabras_totales)
    palabras_str = ", ".join(palabras_totales)
    self.caja_subtitulos.setText(palabras_str)

def frases_tlbt(self):
    import random
    numero_extractos_maximos=len(self.frases)-2
    indice_tlbt=random.randint(1, numero_extractos_maximos)
    subs_juntos = f"{self.frases[indice_tlbt]} \n {self.frases[indice_tlbt+1]}"
    self.caja_subtitulos.setText(subs_juntos)

def fin():
    eliminar_archivos_temporales()
    import sys
    sys.exit()

def eliminar_archivos_temporales():
    import os
    archivos = os.listdir("media_temp\\")
    for a in archivos:
        os.remove("media_temp\\"+a)

def reproducir_todo(archivos, caja_subtitulos, subindice, subs, tts):
    if tts=="sí":
        mensaje=f"[ Playing extract {subindice+1} of {len(subs)}: TTS ]"
    else:
        mensaje=f"[  Playing extract {subindice+1} of {len(subs)} ... ]"
    caja_subtitulos.setText(mensaje)
    import sounddevice as sd
    import soundfile as sf
    data, fs = sf.read(archivos)
    sd.play(data, fs)
    sd.wait()
    caja_subtitulos.setText(f"[ {subs[subindice]} ]")

def calcular_tiempo(archivos):
    import soundfile as sf
    f = sf.SoundFile(archivos)
    seconds=f.frames / f.samplerate
    return seconds