from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont     # From pillow
import simplejson as json

from image_utils import ImageText       # Fork from https://gist.github.com/pojda/8bf989a0556845aaf4662cd34f21d269

from copy import deepcopy
import datetime
from glob import glob
import io
import os
import sys

app = Flask(__name__, static_url_path='/static/')

pythonanywherepath  "/home/automatingvisuals/AutomatingVisuals"
if os.path.exists(pythonanywherepath):
    os.chroot(pythonanywherepath)

with open("euchreconfig.json", "r") as infile:
    config = json.load(infile)
    shapesources = config['shapesources']
    backgroundtransparencychoices = config['backgroundtransparencychoices']
    textcolorchoices = config['textcolorchoices']
    defaults = config['defaults']
    
stockartdir = "static/stockart/"
stockthumbsdir = "static/stockthumbs/"
mainartfound = []

def build_stock_images():
    global mainartfound
    thumbsfound = []
    thumbstobuild = []
    os.makedirs(stockthumbsdir, exist_ok=True)       # Make the directory if we don't already have it
    for stockart in sorted(glob(stockartdir + "*.jpg")):
        basename = stockart.replace("\\", "/").replace(stockartdir, "")
        mainartfound.append(basename)
    for stockthumb in glob(stockthumbsdir + "*.jpg"):
        basename = stockthumb.replace("\\", "/").replace(stockthumbsdir, "")
        thumbsfound.append(basename)
    for mainart in mainartfound:
        if mainart not in thumbsfound:
            thumbstobuild.append(mainart)
    for thumbfound in thumbsfound:
        if thumbfound not in mainartfound:
            print(f"You somehow got an extra thumbnail -- {thumbfound} -- but don't have the main art. What did you do?")
    if len(thumbstobuild) > 0:
        print(f"Need to build {len(thumbstobuild):,} thumbnails.")
        thumbnailsize = 480, 360
        for thumbtobuild in thumbstobuild:
            beer = Image.open(stockartdir + thumbtobuild)
            beer.thumbnail(thumbnailsize)
            beer.save(stockthumbsdir + thumbtobuild)
        beer = None             # NOOOOOOOOOOoooooooooooooooooooooo
    return()



@app.route('/')
def choose_template():
    return(render_template('choose.html',
                           shapesources=shapesources,
                           backgroundtransparencychoices=backgroundtransparencychoices,
                           textcolorchoices=textcolorchoices,
                           mainartfound=mainartfound))

# https://stackoverflow.com/questions/11017466/flask-to-return-image-stored-in-database

                

@app.route('/generate/', methods=['GET', 'POST'])
def generate():

    sourceimage = "sourceimage.jpg"

    z = request.form
    if 'maintext1' not in z or not z['maintext1']:
        print(f"No maintext1 -- what did you do?")
        # ******************** Should go to an error message web page
    else:
        maintext = z['maintext1']

    if 'shape1' not in z or not z['shape1'] or z['shape1'] not in shapesources:
        shapewanted = defaults['shape1']
        print(f"\tDefaulting on shape1")
    else:
        shapewanted = z['shape1']

    if 'stockart1' not in z or not z['stockart1'] or z['stockart1'] not in mainartfound:
        print(f"Missing or bad stockart1. Defaulting.")
        sourceimage = stockartdir + defaults['stockart1']
    else:
        sourceimage = stockartdir + z['stockart1']
   
    if 'transparency1' not in z or not z['transparency1'] or z['transparency1'] not in backgroundtransparencychoices:
        print(f"Missing or bad transparency1. Defaulting.")
        transparencywanted = defaults['transparency1']
    else:
        transparencywanted = z['transparency1']

    if 'textcolor1' not in z or not z['textcolor1'] or z['textcolor1'] not in textcolorchoices:
        print(f"Missing or bad textcolor1. Defaulting.")
        fontcolor = defaults['textcolor1']
    else:
        fontcolor = z['textcolor1']

    fontdir = "static/fonts/"
    mainfont = fontdir + "NotoSans-SemiBold.ttf"       # ExtraLight, Light, Regular, Medium, SemiBold, Bold, ExtraBold

    targetw, targeth = shapesources[shapewanted]
    targeta = float(targetw) / float(targeth)

    # https://stackoverflow.com/questions/4744372/reducing-the-width-height-of-an-image-to-fit-a-given-aspect-ratio-how-python
    bgimage = Image.open(sourceimage)
    sourcew, sourceh = bgimage.size
    sourcea = float(sourcew) / float(sourceh)

    if sourcea > targeta:
        # Then crop the left and right edges:
        new_width = int(targeta * sourceh)
        offset = (sourcew - new_width) / 2
        resize = (offset, 0, sourcew - offset, sourceh)
    else:
        # ... crop the top and bottom:
        new_height = int(sourcew / targeta)
        offset = (sourceh - new_height) / 2
        resize = (0, offset, sourcew, sourceh - offset)

    transparencysetting = 255 - int(float(backgroundtransparencychoices[transparencywanted]) / float(100) * float(255))

    bgimage = bgimage.crop(resize).resize((targetw, targeth), Image.Resampling.LANCZOS)  # Slowest, but best quality https://pillow.readthedocs.io/en/stable/handbook/concepts.html#filters-comparison-table
    # bgimage.show()

    if transparencysetting > 0:
        filler = Image.new('RGBA', (targetw, targeth), "white")
        bgimage.putalpha(transparencysetting)
        bgimage = Image.alpha_composite(filler, bgimage)
    #     bgimage.show()
        bgimage = bgimage.convert('RGB')

    # Don't need to save the image any more
    # bgimage.save('bgimage.jpg')    # Check quality settings -- default to 80 maybe?

    # Let's figure out some text overlays. Jody's textwrap use isn't really evaluating the actual width of the characters used.
    # Some alternatives are here:
    # https://gist.github.com/turicas/1455973
    # leads to fork at https://gist.github.com/pojda/8bf989a0556845aaf4662cd34f21d269

    # for textindex, text in enumerate(texts):
    text = maintext
    tempimagefilename = "temp-textimage.png"
    localimage = deepcopy(bgimage)
    fullmarginpct = 0.26     # What percentage for margins
    textwidth = int(targetw * (1-float(fullmarginpct)))
    insetwidth = int(fullmarginpct / 2 * float(targetw))
    textimage = ImageText((targetw, targeth), background=(255, 255, 255, 0))

    textimage.write_text_box((insetwidth, insetwidth), text, box_width=textwidth, font_filename=mainfont,
                             font_size=35, color=fontcolor)
    textimage = textimage.image     # Bring this back to a PIL object so we can combine it
    localimage = localimage.convert('RGBA')
    localimage = Image.alpha_composite(localimage, textimage)
    localimage = localimage.convert('RGB')
    # Don't need to save sample image any more
    # localimage.save(f"sample-test.jpg")
    # localimage.show()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")    # Generate fresh time stamp on each export

    filename = f"test-{timestamp}.jpg"

    binarycontents = io.BytesIO()
    localimage.save(binarycontents, "JPEG")
    binarycontents.seek(0)
        
    return(send_file(binarycontents,
           mimetype='image/jpeg',
           as_attachment=True,
           download_name=filename))
    
    # return(render_template('done.html',
     #                      filename=filename))


build_stock_images()      # Run all that code above.

@app.route('/stockimages/')
def show_stock_images():
    return(render_template('stockimages.html',
                           stockthumbsdir=stockthumbsdir,
                           mainartfound=mainartfound))
                           

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
