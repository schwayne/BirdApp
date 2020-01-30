##imports functions to detect modules

import sys
import os

#https://stackoverflow.com/questions/57593111/how-to-call-pip-from-a-python-script-and-make-it-install-locally-to-that-script
#https://stackoverflow.com/questions/49093956/how-to-install-modules-using-idle

#Adds package directories to the program, however, this only works with python version 3.4
#First it checks to see if the Python running is 32-bit or 64-bit
#if the following do not work, it will need to be installed using pip (see report)
if (sys.maxsize > 2**32):
    sys.path.append(os.path.dirname(os.path.abspath(__file__))+ "\\NecessaryModules")
    
else:
    sys.path.append(os.path.dirname(os.path.abspath(__file__))+ "\\NecessaryModules32bit")

#imports necessary packages
from PIL import ImageTk, Image
import pygame
import tkinter as tkr
import traceback
import ctypes

def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas.configure(scrollregion=canvas.bbox("all"))

#https://stackoverflow.com/questions/8863917/importerror-no-module-named-pil
#https://stackoverflow.com/questions/23901168/how-do-i-insert-a-jpeg-image-into-a-python-tkinter-window
#http://www.blog.pythonlibrary.org/2012/07/26/tkinter-how-to-show-hide-a-window/
#https://stackoverflow.com/questions/40526496/vertical-scrollbar-for-frame-in-tkinter-python

def show_error(self, *args):
    err = traceback.format_exc()
    if "pygame.error: Couldn't read from RWops" in err or\
        "pygame.error: Couldn't open" in err:
        ctypes.windll.user32.MessageBoxW(0, "There was an error with your song file", "Error",1) 
    elif "missing" in err:
        if "'title'" in err:
            ctypes.windll.user32.MessageBoxW(0, "Your bird window is missing a title.", "Error", 1)
        elif "'song_file'" in err:
            ctypes.windll.user32.MessageBoxW(0, "Your bird window is missing a song file.", "Error", 1)
        elif "'img_file'" in err:
            ctypes.windll.user32.MessageBoxW(0, "Your bird window is missing a image file.", "Error", 1)
        elif "'additional_caption'" in err:
            ctypes.windll.user32.MessageBoxW(0, "Your bird window is missing a common name.", "Error", 1)
        elif "'latin_name'" in err:
            ctypes.windll.user32.MessageBoxW(0, "Your bird window is missing a latin name.", "Error", 1)
        elif "'desc'" in err:
            ctypes.windll.user32.MessageBoxW(0, "Your bird window is missing a description.", "Error", 1)
    else:
        ctypes.windll.user32.MessageBoxW(0, str(err), "Error", 1)

tkr.Tk.report_callback_exception = show_error

#creates main window and adds a scrollbar
test = tkr.Tk()
w = 150
h = 400
ws = test.winfo_screenwidth() # width of the screen
hs = test.winfo_screenheight() # height of the screen
x = (ws/2) - (w/2)
y = 100
test.geometry("%dx%d+%d+%d" % (w, h, x, y))
canvas = tkr.Canvas(test, width = 130, height = test.winfo_reqheight())
canvas.pack(side = tkr.LEFT, fill = "both")
test.title("Bird Identifier")
scrollbar = tkr.Scrollbar(test, command = canvas.yview)
scrollbar.pack(side= "right", fill= "y")
canvas.configure(yscrollcommand = scrollbar.set)
canvas.bind('<Configure>', on_configure)
birds = tkr.Frame(canvas)
canvas.create_window((0,0), window=birds, anchor='nw')


#initializes pygame to allow for playing of media files
pygame.init()
pygame.mixer.init()

#creates a play function
def play(file):

    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

#creates a stop function
def stop():
    pygame.mixer.music.stop()

        #http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm

#a function that can be reused to create bird windows
def create_bird_window(
    parent_window: tkr.Tk,
    title: str,
    song_file: str,
    img_file: str,
    additional_caption: str,
    latin_name: str,
    desc: str = ""
    ) -> tkr.Toplevel:

#https://stackoverflow.com/questions/4770993/how-can-i-make-silent-exceptions-louder-in-tkinter



 #This function creates a window that shows the name and picture of a bird
    #together with buttons for playing corresponding songs.

    #Creates the window, gives it a title, and has the close button stop the song
    bird_window = tkr.Toplevel(parent_window)
    bird_window.title(title)
    bird_window.protocol("WM_DELETE_WINDOW", lambda:[bird_window.withdraw(), stop()])
    w, h = bird_window.winfo_screenwidth(), bird_window.winfo_screenheight()
    bird_window.geometry("%dx%d+0+0" % (w, h))
    try:

        #implements play function into a button
        play_button = tkr.Button(
            bird_window,
            text="Play Song",
            command=lambda: play(song_file)
        )

        #implements stop function into a button
        stop_button = tkr.Button(
            bird_window,
            text="Stop",
            command= lambda: [stop()]
        )

        #makes a button to hide the window
        hide_this_button = tkr.Button(
            bird_window,
            text="Hide",
            command=lambda: [bird_window.withdraw(), stop()]
        )
        

        #packs these buttons
        hide_this_button.grid(row = 5, column = 0, pady = 5)
        play_button.grid(row = 6, column = 0, pady = 5)
        stop_button.grid(row = 7, column = 0, pady = 5)

    except pygame.error as message:
        tkr.Tk.report_callback_exception = show_error



   
    bird_window.grid_columnconfigure(0, minsize=100)
    #creates a caption at the bottom
    caption = tkr.Label(bird_window, text=additional_caption)
    
    #creates the latin caption, italicized
    caption_latin = tkr.Label(
        bird_window,
        text=latin_name,
        font="Helvetica 10 italic"
    )

    #packs the captions
    caption.grid(row = 1, column = 2, columnspan = 2,  sticky = tkr.N, pady = 5)
    caption_latin.grid(row = 0, column = 2,  columnspan = 2, sticky = tkr.N, pady = 5)
    try:
        #creates an image object for the bird windows
        image_object = ImageTk.PhotoImage(Image.open(img_file))

        #creates a reference for the image, since tkinter has trouble working with images
        image_panel = tkr.Label(bird_window, image=image_object)
        image_panel.image = image_object
        image_panel.grid(row = 2, column = 2,  columnspan = 2, rowspan = 10, pady = 10)

    except Exception:
            ctypes.windll.user32.MessageBoxW(0, "Image location not correctly provided", "Error", 1)

    bird_window.grid_columnconfigure(4, minsize=640)
    
    description = tkr.Label(bird_window, text=desc, justify = "left", wraplength = 560)
    description.grid(row = 2, column = 4,  columnspan = 3, rowspan = 10, pady = 10)


    return bird_window


#creates list of buttons for the main page
buttons = [

    #creates buttons for each of the birds
    tkr.Button(
        birds,
        text="European Robin\nErithacus rubecula",
        font="Helvetica 10 italic",
        command=lambda: create_bird_window(
            parent_window=birds,
            title="European Robin",
            song_file="BirdMedia/european-robin.mp3",
            img_file="BirdMedia/european-robin.jpg",
            additional_caption="Common names (EN, DE): European Robin, Rotkehlchen",
            latin_name="Erithacus rubecula",
            desc = "        EN: The European robin (Erithacus rubecula), known simply as the robin or robin redbreast \
in the British Isles, is a small insectivorous passerine bird, specifically a chat, that was formerly classified \
as a member of the thrush family (Turdidae) but is now considered to be an Old World flycatcher (Muscicapidae). About 12.5–14.0 cm \
(5.0–5.5 inches) in length, the male and female are similar in colouration, with an orange breast and face lined with grey, \
brown upper-parts and a whitish belly. It is found across Europe, east to Western Siberia and south to North Africa; \
it is sedentary in most of its range except the far north.\
\n \n\
        DE: Das Rotkehlchen (Erithacus rubecula) ist eine Vogelart aus der Familie der Fliegenschnäpper (Muscicapidae). \
Es besiedelt Nordafrika, Europa und Kleinasien sowie die Mittelmeerinseln. \
Seine Nahrung besteht vor allem aus Insekten, kleinen Spinnen, Würmern und Schnecken. \
Die orangerote Kehle, Stirn und Vorderbrust sind leicht zu erkennen und erlauben eine einfache Bestimmung. \
Füße und Iris sind dunkelbraun, der Schnabel ist schwarzgrau bis braunschwarz. Über den Schnabelwinkeln stehen je drei bis vier Bartborste. \
Die Größe liegt bei etwa 13,5 bis 14 Zentimetern."
        )
        
    ),
    tkr.Button(
        birds,
        text="Wood Nuthatch\nSitta europaea",
        font="Helvetica 10 italic",
        command=lambda: create_bird_window(
            parent_window=birds,
            title="Wood Nuthatch",
            song_file="BirdMedia/wood-nuthatch.mp3",
            img_file="BirdMedia/wood-nuthatch.jpg",
            additional_caption="Common names (EN, DE): Wood Nuthatch, Kleiber",
            latin_name="Sitta europaea",
            desc = "        EN: The Eurasian nuthatch or wood nuthatch (Sitta europaea) is a small passerine bird found throughout \
temperate Asia and in Europe, where its name is the nuthatch. Like other nuthatches, it is a short-tailed bird with a long bill, \
blue-grey upperparts and a black eye-stripe. The adult male of the nominate subspecies, S. e. europaea is 14 cm (5.5 in) long. \
It is a vocal bird with a repeated loud dwip call. \
There are more than 20 subspecies in three main groups; birds in the west of the range have orange-buff underparts and a white throat, \
those in Russia have whitish underparts, and those in the Far East have a similar appearance to European birds, but lack the white throat. \
The Eurasian nuthatch eats mainly insects, particularly caterpillars and beetles, \
although in autumn and winter its diet is supplemented with nuts and seeds. The young are fed mainly on insects, with some seeds, \
food items mainly being found on tree trunks and large branches. The nuthatch can forage when descending trees head first, \
as well as when climbing. It readily visits bird tables, eating fatty man-made food items as well as seeds. \
It is an inveterate hoarder, storing food year-round.\
\n \n \
        DE: Der Kleiber (Sitta europaea), auch Spechtmeise, ist eine Vogelart aus der Familie der Kleiber. Der eurasische Kleiber \
kommt in Europa, Nordwest-Afrika und Asien (mit Ausnahme von Süd- und Südostasien), also von Großbritannien bis Japan, \
vor. Der Kleiber erreicht eine Körperlänge von 12 bis 14,5 Zentimetern. Der Körper ist gedrungen mit großem Kopf, sehr kurzem \
Hals und kurzem Schwanz. Der Schnabel ist lang, spitz und grau gefärbt. Die Oberseite des Gefieders ist blaugrau und die Unterseite \
je nach Unterart weiß bis ockerfarbig oder rostrot gefärbt. Auf den immer rotbraun gefärbten Oberschwanzdecken sind große, weiße Flecken. \
Der Kleiber hat einen schwarzen Augenstreifen. Die Wangen und die Kehle sind weiß. Die Iris ist schwarz und die Beine sind orangegelb.  \
Die Nahrung besteht hauptsächlich aus Insekten, Insekteneiern und -larven. Im Herbst kommen Samen, Beeren und Nüsse dazu. Größere \
Beutetiere klemmt der Kleiber in eine Rindenspalte, hängt sich kopfunter darüber und meißelt mit dem kräftigen Schnabel mundgerechte \
Bissen ab. Kleiber treten auch in lockeren Gesellschaften mit Meisen auf und nehmen wie diese gern von Menschen ausgebrachtes Futter wie Getreide \
und trockene Früchte auf."
        )
    ),

    
    tkr.Button(
        birds,
        text="Common Blackbird\nTurdus merula",
        font="Helvetica 10 italic",
        command=lambda: create_bird_window(
            parent_window=birds,
            title="Common Blackbird",
            song_file= "BirdMedia/common-blackbird.mp3",
            img_file= "BirdMedia/common-blackbird.jpg",
            additional_caption= "Common names (EN, DE): Common Blackbird, Amsel",
            latin_name= "Turdus merula",
            desc = "        EN: The common blackbird (Turdus merula) is a species of true thrush [(Turdidae)]. It is also called Eurasian blackbird \
especially in North America, to distinguish it from the unrelated New World blackbirds), or simply blackbird where this does not lead to \
confusion with a similar-looking local species. \
It breeds in Europe, Asia, and North Africa, and has been introduced to Australia and New Zealand. It has a number of subspecies across its large range; \
a few of the Asian subspecies are sometimes considered to be full species. Depending on latitude, the common blackbird may be resident, \
partially migratory, or fully migratory. The adult male of the nominate subspecies, which is found throughout most of Europe, \
is all black except for a yellow eye-ring and bill and has a rich, melodious song; the adult female and juvenile have mainly dark brown plumage.\
[Adults are] 23.5 to 29 centimetres (9.25 to 11.4 in) in length, [and have] a long tail. \
[They are] omnivorous, eating a wide range of insects, earthworms, berries, and fruits.\
\n \n \
        DE: Die Amsel (Turdus merula) oder Schwarzdrossel ist eine Vogelart der Familie der Drosseln (Turdidae). \
In Europa zählt die Amsel als einer der am weitesten verbreiteten Vertreter dieser Familie zu den bekanntesten Vögeln überhaupt. \
In Europa brütet die Amsel nahezu flächendeckend, nur nicht im hohen Norden und im äußersten Südosten. \
Darüber hinaus kommt sie in Teilen Nordafrikas und Asiens vor. In Australien und Neuseeland wurde die Amsel eingebürgert. \
In Mitteleuropa verlässt ein Teil der Vögel im Winter das Brutgebiet und zieht nach Südeuropa oder Nordafrika. \
Die Männchen sind schwarz gefärbt und haben einen gelben Schnabel, das Gefieder der Weibchen ist größtenteils dunkelbraun. \
Der melodiöse und laut vorgetragene Reviergesang der Männchen ist in Mitteleuropa hauptsächlich zwischen Anfang März und Ende Juli zu hören \
und kann bereits vor der Morgendämmerung beginnen.\
Ihre Körperlänge liegt zwischen 24 und 27 Zentimetern. Ihre Nahrung suchen Amseln vorwiegend am Boden. \
Sie ernähren sich überwiegend von tierischer Nahrung, meist Regenwürmer oder Käfer. \
Abhängig von der Verfügbarkeit steigt der Anteil gefressener Beeren und Früchte."
        )
    ),
    tkr.Button(
        birds,
        text="Chaffinch\nFringilla coelebs",
        font="Helvetica 10 italic",
        command=lambda: create_bird_window(
            parent_window=birds,
            title="Chaffinch",
            song_file="BirdMedia/chaffinch.mp3",
            img_file="BirdMedia/chaffinch.jpg",
            additional_caption="Common names (EN, DE): Chaffinch, Buchfink",
            latin_name="Fringilla coelebs",
            desc = ""
        )
    ),
    tkr.Button(
        birds,
        text="Common Crane\nGrus grus",
        font="Helvetica 10 italic",
        command=lambda: create_bird_window(
            parent_window=birds,
            title="Common Crane",
            song_file="BirdMedia/common-crane.mp3",
            img_file="BirdMedia/common-crane.jpg",
            additional_caption= "Common names (EN, DE): Common Crane, Kranich",
            latin_name="Grus grus",
            desc = ""
        )
    ),
    tkr.Button(
        birds,
        text="Common Kingfisher\nAlcedo atthis",
        font="Helvetica 10 italic",
        command=lambda: create_bird_window(
            parent_window=birds,
            title="Common Kingfisher",
            song_file="BirdMedia/common-kingfisher.mp3",
            img_file="BirdMedia/common-kingfisher.jpg",
            additional_caption="Common names (EN, DE): Common Kingfisher, Eisvogel",
            latin_name="Alcedo atthis",
            desc = ""
        )
    ),
    tkr.Button(
        birds,
        text="Eurasian Great Tit\nParus major",
        font="Helvetica 10 italic",
        command=lambda: create_bird_window(
            parent_window=birds,
            title="Eurasian Great Tit",
            song_file="BirdMedia/eurasian-great-tit.mp3",
            img_file="BirdMedia/eurasian-great-tit.jpg",
            additional_caption="Common names (EN, DE): Eurasian Great Tit, Kohlmeise",
            latin_name="Parus major",
            desc = ""
        )
    ),
    
    tkr.Button(
        birds,
        text="House Sparrow\n  Passer domesticus",
        font="Helvetica 10 italic",
        command=lambda: create_bird_window(
            parent_window=birds,
            title="House Sparrow",
            song_file="BirdMedia/house-sparrow.mp3",
            img_file="BirdMedia/house-sparrow.jpg",
            additional_caption="Common names (EN, DE): House Sparrow, Haussperling",
            latin_name="Passer domesticus",
            desc = ""
        )
    ),

    #creates an exit button
    tkr.Button(birds,
                  text = "Exit",
                  command = test.destroy)
] 


#packs all the buttons
for button in buttons:
    button.pack(fill="x")


tkr.mainloop()

