##imports functions to detect modules

import sys
import os


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

#https://stackoverflow.com/questions/23901168/how-do-i-insert-a-jpeg-image-into-a-python-tkinter-window
#https://stackoverflow.com/questions/40526496/vertical-scrollbar-for-frame-in-tkinter-python

#if there is an error within tkinter, such as a missing parameter, it will try to create error here
#https://stackoverflow.com/questions/4770993/how-can-i-make-silent-exceptions-louder-in-tkinter
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

    #Creates the window, gives it a title, and has the close button stop the song
    bird_window = tkr.Toplevel(parent_window)
    bird_window.title(title)
    bird_window.protocol("WM_DELETE_WINDOW", lambda:[bird_window.withdraw(), stop()])
    w, h = bird_window.winfo_screenwidth(), bird_window.winfo_screenheight()
    bird_window.geometry("%dx%d+0+0" % (w, h))

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
    

    #configures the button column and then includes the buttons
    bird_window.grid_columnconfigure(0, minsize=100)
    play_button.grid(row = 5, column = 0, pady = 5)
    stop_button.grid(row = 6, column = 0, pady = 5)
    hide_this_button.grid(row = 7, column = 0, pady = 5)

   
    #creates a caption at the bottom
    caption = tkr.Label(bird_window, text=additional_caption)
    
    #creates the latin caption, italicized
    caption_latin = tkr.Label(
        bird_window,
        text=latin_name,
        font="Helvetica 10 italic"
    )

    #includes the captions
    caption.grid(row = 1, column = 2, columnspan = 2,  sticky = tkr.N, pady = 5)
    caption_latin.grid(row = 0, column = 2,  columnspan = 2, sticky = tkr.N, pady = 5)

    #configures the size of the description column
    bird_window.grid_columnconfigure(4, minsize=640)
    description = tkr.Label(bird_window, text=desc, justify = "left", wraplength = 560)
    description.grid(row = 2, column = 4,  columnspan = 3, rowspan = 10, pady = 10)

    #attempts to include image
    try:
        #creates an image object for the bird windows
        image_object = ImageTk.PhotoImage(Image.open(img_file))

        #creates a reference for the image, since tkinter has trouble working with images, the places it in the grid
        image_panel = tkr.Label(bird_window, image=image_object)
        image_panel.image = image_object
        image_panel.grid(row = 2, column = 2,  columnspan = 2, rowspan = 10, pady = 10)

    #if image is not found, it returns a message box error
    except Exception:
            ctypes.windll.user32.MessageBoxW(0, "Image location not correctly provided", "Error", 1)
  
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
            song_file= "BirdMedia/common-blackbid.mp3",
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
            desc = "EN: The common chaffinch (Fringilla coelebs), usually known simply as the chaffinch, is a common and widespread small passerine \
bird in the finch family. The male is brightly coloured with a blue-grey cap and rust-red underparts. \
The female is much duller in colouring, but both sexes have two contrasting white wing bars and white sides to the tail. The chaffinch is about 14.5 cm (5.7 in) \
long, with a wingspan of 24.5–28.5 cm (9.6–11.2 in) and a weight of 18–29 g (0.63–1.02 oz).\
The male bird has a strong voice and sings from exposed perches to attract a mate. \
The chaffinch breeds in much of Europe, across Asia to Siberia and in northwest Africa. The female builds a nest with a deep cup in the fork \
of a tree. Outside the breeding season, chaffinches form flocks in open countryside and forage for seeds on the ground. During the breeding season, \
they forage on trees for invertebrates, especially caterpillars, and feed these to their young. \
They are partial migrants; birds breeding in warmer regions are sedentary, while those breeding in the colder northern \
areas of their range winter further south. Its large numbers and huge range mean that chaffinches are classed as of \
least concern by the International Union for Conservation of Nature.\
\n\n\
DE: Der Buchfink (Fringilla coelebs) ist ein zur Familie der Finken (Fringillidae) gehöriger Singvogel. Er kommt in ganz \
Europa mit Ausnahme Islands und des nördlichsten Skandinaviens vor, sein Verbreitungsgebiet erstreckt sich in östlicher Richtung bis \
nach Mittelsibirien. Er ist außerdem ein Brutvogel in Nordafrika und Vorderasien bis einschließlich des Irans. \
In Neuseeland und in der Südafrikanischen Republik ist der Buchfink vom Menschen eingeführt worden. \
In Mitteleuropa ist der Buchfink einer der am weitesten verbreiteten Brutvögel. Sein Verbreitungsgebiet reicht von der Küste \
bis zur Baumgrenze im Gebirge. Die Buchfinken Nord- und Osteuropas sind Zugvögel, dagegen ist er in Mitteleuropa ein Teilzieher. \
Der Buchfink erreicht eine Körperlänge von 14 bis 18 Zentimeter. Die Individuen der Nominatform wiegen zwischen 18 und 25 Gramm. \
Bei den Männchen sind die Körperunterseite und die Kopfseiten bräunlichrosa bis rotbraun. \
Der Oberkopf, der Nacken und die Halsseiten sind im Sommerhalbjahr auffällig graublau, im Winterhalbjahr mehr bräunlichgrau. Die Stirn \
ist schwarz, der Rücken ist kastanienbraun und der Bürzel ist grünlich. Der Schnabel ist beim Männchen im Frühjahr stahlblau, ansonsten \
hornfarben. Die Weibchen sind auf der Körperoberseite olivgrau und auf der Körperunterseite etwas heller. \
Der Schnabel des Weibchens ist ganzjährig hellbraun bis hornfarben. Die Nahrung der Buchfinken besteht aus Beeren, Samen aller Art, \
Insekten und Spinnen. Die Nestlinge werden mit Insekten und deren Larven gefüttert."

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
            desc = "EN: The common crane (Grus grus), also known as the Eurasian crane, is a bird of the family Gruidae, the cranes. \
A medium-sized species, it is the only crane commonly found in Europe besides the demoiselle crane (Anthropoides virgo). Despite the species' large numbers, \
local extinctions and extirpations have taken place in part of its range, and an ongoing reintroduction project is underway in the United Kingdom.\
The common crane is a large, stately bird and a medium-sized crane. It is 100–130 cm (39–51 in) long with a 180–240 cm (71–94 in) wingspan. \
The body weight can range from 3 to 6.1 kg (6.6 to 13.4 lb), with the nominate subspecies averaging around 5.4 kg (12 lb) \
and the eastern subspecies (G. g. lilfordi) averaging 4.6 kg (10 lb). Males are slightly heavier and larger than females, \
with weight showing the largest sexual size dimorphism, followed by wing, central toe, and head length in adults and juveniles. \
This species is slate-grey overall. The forehead and lores are blackish with a bare red crown and a white streak extending from behind \
the eyes to the upper back. The overall colour is darkest on the back and rump and palest on the breast and wings. The common crane is omnivorous, \
as are all cranes. It largely eats plant matter, including roots, rhizomes, tubers, stems, leaves, fruits and seeds. They also commonly eat, \
when available, pond-weeds, heath berries, peas, potatoes, olives, acorns, cedarnuts and pods of peanuts. \
Animal foods become more important during the summer breeding season and may be the primary food source at that time of year, \
especially while regurgitating to young. Their animal foods are insects, especially dragonflies, and also snails, earthworms, crabs, \
spiders, millipedes, woodlice, amphibians, rodents, and small birds.\
\n\n\
DE: Der Kranich (Grus grus), auch Grauer Kranich oder Eurasischer Kranich, ist ein Vertreter der Familie der Kraniche (Gruidae). \
In Europa kommt er weitgehend als einzige Kranichart vor; erst ab der Schwarzmeerregion beginnt das Verbreitungsgebiet des Jungfernkranichs. \
Kraniche bewohnen Sumpf- und Moorlandschaften in weiten Teilen des nördlichen und östlichen Europas, aber auch einige Gebiete im Norden Asiens. \
Sie nehmen das ganze Jahr über sowohl tierische als auch pflanzliche Nahrung auf. Die Nahrung besteht aus Kleinsäugern, Reptilien, \
kleinen Fischen, Fröschen, Schnecken, Würmern, Insekten und deren Larven. Sie beinhaltet auch Mais-, Gersten-, Weizen- und Haferkörner, \
Sonnenblumenkerne, Erbsen, Bohnen, Erdnüsse, Oliven, Beeren, Eicheln, Gemüse, Kartoffeln, Pflanzenwurzeln, -sprossen und Halme.\
Der Bestand hat in den letzten Jahrzehnten stark zugenommen, \
so dass die Art zurzeit nicht gefährdet ist. Kennzeichnend sind die schwarz-weiße Kopf- und Halszeichnung und die federlose rote Kopfplatte. \
Der keilförmige, schlanke Schnabel ist über zehn Zentimeter lang. Das Gefieder hat abgesehen vom Kopf eine hellgraue Färbung in vielen Abstufungen. \
Sehr selten sind fast weiße und sehr dunkle Vögel. Der Schwanz sowie die Hand- und Armschwingen sind schwarz. Die Humeralfedern variieren farblich \
von Grau bis Schwarz und hängen bei Altvögeln als „Schleppe“ über den Schwanz hinweg. Zur Brutzeit wird der Schulter- und Rückenbereich mit Moorerde \
hell- bis dunkelbraun gefärbt. Die Geschlechter sind äußerlich schwer zu unterscheiden. Männchen sind jedoch durchschnittlich etwas größer \
als Weibchen. Erstere wiegen fünf bis sieben Kilogramm, letztere fünf bis sechs. Der Kranich erreicht eine Höhe von 110 bis 130 cm."
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
            desc = "EN: The common kingfisher (Alcedo atthis) also known as the Eurasian kingfisher, and river kingfisher, is a \
small kingfisher with seven subspecies recognized within its wide distribution across Eurasia and North Africa.\
It is resident in much of its range, but migrates from areas where rivers freeze in winter. \
This sparrow-sized bird has the typical short-tailed, large-headed kingfisher profile; it has blue upperparts, \
orange underparts and a long bill. It feeds mainly on fish, caught by diving, and has special visual adaptations to enable it to see prey under water. \
The adult male of the western European subspecies, A. a. ispida has green-blue upperparts with pale azure-blue back and rump, a rufous patch by the bill \
base, and a rufous ear-patch. It has a green-blue neck stripe, white neck blaze and throat, rufous underparts, and a black bill with some red at the base. \
The legs and feet are bright red. It is about 16 centimetres (6.3 in) long with a wingspan of 25 cm (9.8 in), and weighs 34–46 grams (1.2–1.6 oz).\
The female is identical in appearance to the male except that her lower mandible is orange-red with a black tip.\
\n\n\
DE:Der Eisvogel (Alcedo atthis) ist die einzige in Mitteleuropa vorkommende Art aus der Familie der Eisvögel (Alcedinidae). \
Er besiedelt weite Teile Europas, Asiens sowie das westliche Nordafrika und lebt an mäßig schnell fließenden oder stehenden, klaren \
Gewässern mit Kleinfischbestand und Sitzwarten. Seine Nahrung setzt sich aus Fischen, Wasserinsekten (Imagines und Larven), Kleinkrebsen und \
Kaulquappen zusammen. Der Bestand hat in den letzten Jahren wieder zugenommen und die Art wird derzeit in Europa als dezimiert, aber im gesamten\
Verbreitungsgebiet als wenig bedroht eingestuft. Eisvögel haben eine Körperlänge von etwa 16 bis 18 cm und wiegen 35 bis 40 g. Die Flügelspannweite \
beträgt etwa 25 cm. Oberkopf, Flügeldecken, Schultern und Schwanzfedern sind dunkelblaugrün bis \
grünblau gefärbt, wobei sich an den Kopffedern azurblaue \Querbänder und an den Flügeldecken azurblaue Spitzen befinden. \
Der Rückenstreifen ist leuchtend türkisblau. Bis auf die weiße Kehle ist die Unterseite beim Altvogel rostrot bis kastanienbraun gefärbt. \
Die Kopfzeichnung ist durch rotbraune Ohrdecken, scharf abgesetzte weiße Halsseitenflecken und einen blaugrünen oder blauen Bartstreif charakterisiert. \
Auf der Stirn befindet sich vor jedem Auge ein kastanienbrauner Fleck, der von vorn gesehen weiß erscheint. Zur Brutzeit sind die Füße orangerot. "
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
            desc = "EN: The great tit (Parus major) is a passerine bird in the tit family Paridae. It is a widespread and common species \
throughout Europe, the Middle East, Central and Northern Asia, and parts of North Africa where it is generally resident in any sort of woodland; \
most great tits do not migrate except in extremely harsh winters. The great tit remains the most widespread species in the genus Parus. \
The great tit is large for a tit at 12.5 to 14.0 cm (4.9–5.5 in) in length, and has a distinctive appearance that makes it easy to recognise. \
The great tit [has] a black head and neck, prominent white cheeks, olive upperparts and yellow underparts, \
with some variation amongst the numerous subspecies. It is predominantly insectivorous in the summer, but will consume a wider range of \
food items in the winter months, including small hibernating bats. \
The great tit has adapted well to human changes in the environment and is a common and familiar bird in urban parks and gardens.\
\n\n\
DE: Die Kohlmeise (Parus major) ist eine Vogelart aus der Familie der Meisen (Paridae). Sie ist die [...] am weitesten verbreitete \
Meisenart in Europa. Ihr Verbreitungsgebiet erstreckt sich jedoch bis in den Nahen Osten und durch die gemäßigte Zone Asiens bis nach Fernost. \
Sie zählt meist zu den häufigsten Vogelarten. Die Nahrung ist sehr vielfältig, jedoch werden hauptsächlich Insekten und deren Larven sowie \
pflanzliche Nahrung wie beispielsweise Samen oder Nussfrüchte gefressen. Die Kohlmeise zählt mit 13–15 cm Körperlänge zu den größeren Meisenarten\
und ist die größte Meise in Europa. Bei adulten Männchen der Nominatform sind der Oberkopf, der obere Nacken, die Halsseiten, die Kehle und ein \
Band auf der Brustmitte glänzend blauschwarz. Wangen und Ohrdecken sind rein weiß und werden von den schwarzen Partien sauber eingefasst. Die \
Brust- und Bauchseiten sind schwefel- bis zitronengelb. Das schwarze Band in der Mitte erweitert sich zwischen den Beinen zu einem tiefschwarzen Fleck. \
Der ursprüngliche Lebensraum der Kohlmeise sind Laub- und Mischwälder mit alten Bäumen; \
aufgrund ihrer Anpassungsfähigkeit kommt sie jedoch in fast allen Lebensräumen vor, in denen sie Höhlen zum Nisten findet.Die meisten Kohlmeisen bleiben \
im Winter in ihren Brutgebieten, wo sie teilweise in kleinen Trupps umherstreifen und sich auch mit anderen Meisen vergesellschaften."
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
            desc = "The house sparrow (Passer domesticus) is a bird of the sparrow family Passeridae, found in most parts of the world. \
It is a small bird that has a typical length of 16 cm (6.3 in) and a mass of 24–39.5 g (0.85–1.39 oz). Females and young birds are coloured pale brown \
and grey, and males have brighter black, white, and brown markings. One of about 25 species in the genus Passer, the house sparrow is native to most of \
Europe, the Mediterranean Basin, and a large part of Asia. Its intentional or accidental introductions to many regions, \
including parts of Australasia, Africa, and the Americas, make it the most widely distributed wild bird. The sexes exhibit strong dimorphism: \
the female is mostly buffish above and below, while the male has boldly coloured head markings, a reddish back, and grey underparts. \
As an adult, the house sparrow mostly feeds on the seeds of grains and weeds, but it is opportunistic and adaptable, and eats whatever foods are available.\
\n\n\
DE: Der Haussperling (Passer domesticus) – auch Spatz oder Hausspatz genannt – ist eine Vogelart aus der Familie der Sperlinge (Passeridae) \
und einer der bekanntesten und am weitesten verbreiteten Singvögel. Der Spatz hat sich vor über 10.000 Jahren als Kulturfolger dem Menschen angeschlossen. \
Nach zahlreichen absichtlichen oder versehentlichen Einbürgerungen ist er – mit Ausnahme der Tropen – fast überall anzutreffen, wo Menschen sich das \
ganze Jahr aufhalten. Nach deutlichen Bestandsrückgängen in der zweiten Hälfte des 20. Jahrhunderts vor allem im Westen Mitteleuropas wurde\
die Art in die Vorwarnliste bedrohter Arten aufgenommen. Der Haussperling ist ein kräftiger und etwas gedrungener Singvogel. Er wiegt rund 30 Gramm \
und erreicht eine Körperlänge von 14 bis 16 Zentimetern – er ist wenig größer als der nah verwandte Feldsperling. Die Männchen sind deutlich \
kontrastreicher gezeichnet als die Weibchen, sie haben eine schwarze oder dunkelgraue Kehle und einen schwarzen Brustlatz, der aber \
im Herbst nach der Mauser von helleren Federrändern verdeckt sein kann. Die Weibchen sind unscheinbarer als die Männchen und matter braun, \
aber sehr fein gezeichnet. Die Oberseite ist hell graubraun, der Rücken schwarzbraun und gelbbraun gestreift. Der Haussperling ernährt sich \
hauptsächlich von Sämereien und dabei vor allem von den Samen kultivierter Getreidearten, die in ländlichen Gebieten 75 Prozent der \
Gesamtnahrung ausmachen können. Bevorzugt werden Weizen vor Hafer und Gerste."
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

#runs the tkr, which functions as a loop
tkr.mainloop()

