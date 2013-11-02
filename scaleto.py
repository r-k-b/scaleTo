#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 ScaleTo - Python-fu script
 Author: Robert K. Bell
 Licence: ...
 ------------------ To Do -------------------------------------
    Watermark insertion
    Error checking
    Target filename checking
    Target filename slugification ('groß & heiße' → 'gross and heisse')
    Target folder creation (shouldn't expect users to create subfolders)
    Optional target filename modification
    Why does it choke on png/gif/anything other than jpeg?
    Verbose logging
    Check source image is in good state before modifying (layer mask active? floating selections?)
    Attach to remote debugger
    Unit tests
--------------------------------------------------------------
"""
__author__ = "Robert K. Bell"
currentversion = "v077"

config = {}
config['upload_folder'] = r'\\appserver01\Private\dubit6\Documents\CfsData'
config['output_folder'] = r'P:\Online_Presence\img'
config['watermarkfolder'] = "//dubb014/DUBB_GDRIVE/Logos/Inland group/"
config['sitelibs_path'] = r'C:\Python27\lib\site-packages'
config['debug'] = False

"""
CHANGELOG: 
v077
    Add output folder selector
v076
    Copy dep_ prefix images to second location for convenience
v075
    Add dpro_ prefix for DealerPro truck images (___x298).
v074
    Add dep_ prefix for DealerPro product images (192x176).
v073
    Allow thumbnails to be badged with ALLRig Rewards decal.
v072e
    Change indents from tab to spaces, some cody tidying.
v072
    watermarklayerid "referenced before assigned"
v071
    Watermark file was moved
v070
    Moved a misplaced comma
v069
    Changed source encoding from UTF8 to ANSI.
v068
    Added option to skip watermarking
v067
    Extraneous output from gprint removed.
v066
    Extra debug info inserted.
v065
    gimp_file_load_layers() always returns nested tuples, duh
v064
    Fix log file path
v064
    Fixed compile errors
    Made option names less cryptic
v063
    First attempt at watermark insertion
    Added file encoding declaration
v062
    File extensions will be changed to .jpg
v061
    Added currentversion variable
v060
    more corrections on prefix aspect ratios and dimensions
v059
    "med" prefix was being scaled to landscape aspect ratio, changed to 
    portrait
"""

from gimpfu import *
import os, logging, sys


# http://stackoverflow.com/questions/16797850/how-can-you-specify-a-default-value-using-a-function-in-a-gimp-python-plugin
def output_folder_func():
    try:
        return config['output_folder']
    except:
        return ""

# create an output function that redirects to gimp's Error Console
def gprint( text ):
    pdb.gimp_message(text)
    return 
    
# attempt to attach to winpdb debugger
# must manually add path (can't do it from GIMP?)
sys.path.append(config['sitelibs_path'])
if config['debug']:
    try:
        import rpdb2
        # TODO: attach to debugger
    except ImportError:
        gprint("Error: couldn't import rpdb2 from {s}".format(config['sitelibs_path']))
    
# Export the file to the location given by the prefix
# Doesn't check 
def exportfile(prefix, image):
    # this needs to be changed to a tested 'slug' function
    websafename = (
        os.path.basename(
            pdb.gimp_image_get_filename(image)
        )
    ).replace(" ", "_")
    
    # this always outputs JPEG format images, change the filename to match.
    # Assumes the image had a dot-seperated file extension.
    # TODO: add test for sane name?
    websafename = ".".join(websafename.split(".")[:-1]) + ".jpg"
    
    #if (prefix == 5) or (prefix == 6):
    truckSalesPrefixes = ['trk', 'trf', 'dpro']
    if prefix in truckSalesPrefixes:
        categoryfolder = "trucksales"
    elif prefix == "fly":
        categoryfolder = "flyers"
    else:
        categoryfolder = "products"
        
    # For debugging in console: 
    # outfile = "P:\\Online_Presence\\img\\products\\tst\\tst_" +  
    # os.path.basename(pdb.gimp_image_get_filename(gimp.image_list()[0]))
    # outfile = "P:\\Online_Presence\\img\\" + categoryfolder + "\\" + prefix + 
    # "\\" +prefix+"_"+websafename
    outfile = config['output_folder'] + "\\%s\\%s\\%s_%s" % (
        categoryfolder, prefix, prefix, websafename
    )
    logging.debug('Outpile path and file is: %s', outfile)
    
    saveresults = pdb.file_jpeg_save(
        #RUN_NONINTERACTIVE, # run-mode
        image, # input image
        pdb.gimp_image_flatten(image), # drawable to save
        outfile, # The name of the file to save the image in
        outfile, # The name of the file to save the image in
        float(0.90), # quality
        float(0), # smoothing
        1, # optimize
        1, # progressive
        "", # comment
        1, # subsmp
        1, # baseline
        0, # restart
        0); # dct algorithm
        
    #gprint("Wrote to "+outfile)
    logging.debug('Save operation returned: %s', saveresults)
    
    if prefix == 'dep':
        # Optional save to convenience folder
        full_path = os.path.join(
            config['upload_folder'], 
            prefix + '_' + websafename)
        logging.debug('Outpile path and file is: %s', full_path)
        try:
            saveresults = pdb.file_jpeg_save(
                #RUN_NONINTERACTIVE, # run-mode
                image, # input image
                pdb.gimp_image_flatten(image), # drawable to save
                full_path, # The name of the file to save the image in
                full_path, # The name of the file to save the image in
                float(0.90), # quality
                float(0), # smoothing
                1, # optimize
                1, # progressive
                "", # comment
                1, # subsmp
                1, # baseline
                0, # restart
                0); # dct algorithm
        except Exception as e:
            logging.warning('Save failed, exception follows:')
            logging.warning(e)
        finally:
            logging.debug('Save operation returned: {s}'.format(
                s = saveresults))
    return
    
def watermark(image, targetprefix) :
    skipwatermark = False
    
    # load appropriate watermark file for the size image we have
    if targetprefix == "med":
        watermarkfilename = "ITC_watermark_med.xcf"
    elif targetprefix == "pop":
        watermarkfilename = "ITC_watermark_pop.xcf"
    elif targetprefix == "six":
        watermarkfilename = "ITC_watermark_six.xcf"
    elif targetprefix == "gal":
        watermarkfilename = "ITC_watermark_gal.xcf"
    elif targetprefix == "thm":
        watermarkfilename = "ITC_watermark_thm_ARR.xcf" 
        # Not exactly a watermark, but a badge to show Rewards Discount applies.
    else:
        skipwatermark = True;
        logging.debug('Skipping watermark process.')
    
    if not skipwatermark:
        watermarkfile = config['watermarkfolder'] + watermarkfilename
        logging.debug('Watermark file: %s', watermarkfilename)
        try:
            loadedimg, watermarklayerid = pdb.gimp_file_load_layers(image,watermarkfile)
        except Exception, error:
            gprint(error)
            logging.error(error)
        logging.debug("watermarklayerid is %s", watermarklayerid)
        # gprint("watermarklayerid is %s"%watermarklayerid)
        
        # watermark file should have only 1 layer
        watermarklayer = gimp.Item.from_id(watermarklayerid[0])
        logging.debug("watermarklayer is %s", watermarklayer)
        
        # create target layer in image
        pdb.gimp_image_add_layer(image, watermarklayer, 0)
        
        # make sure watermark layer sits in the middle
        x = (image.width - watermarklayer.width) / 2
        y = (image.height - watermarklayer.height) / 2
        watermarklayer.set_offsets(x, y)
                
        # set nice layer properties for watermark
        # Hard Light at 3% opacity seems good, not too obvious
        # not required - layer properties come with imported layer
        
        # merge layers for JPEG export
        pdb.gimp_image_merge_visible_layers(image, CLIP_TO_BOTTOM_LAYER)
        
    return

# our script
def scaleto(image, drawable, int_targetprefix, AddWatermark) :
    # the log file should go to the folder that contains this script
    os.chdir(os.path.dirname(sys.argv[0]))
    
    logging.basicConfig(
        filename='ScaleTo.log', 
        level=logging.DEBUG, 
        format='%(asctime)s %(levelname)s %(message)s'
    )
    logging.debug("Scaleto version %s started.", currentversion)
    
    # "thm","med","pop","six","gal","trk","trf","fly","dep","dpro"
    # targetprefix = "tst"
    forceAspectRatio = False
    if int_targetprefix == 0: #thm
        targetwidth = 150
        targetheight = 150
        targetprefix = "thm"
        forceAspectRatio = True
    elif int_targetprefix == 1: #med
        targetwidth = 430
        targetheight = 600
        targetprefix = "med"
    elif int_targetprefix == 2: #pop
        targetwidth = 900
        targetheight = 1000
        targetprefix = "pop"
    elif int_targetprefix == 3: #six
        targetwidth = 1600
        targetheight = 1200
        targetprefix = "six"
    elif int_targetprefix == 4: #gal
        targetwidth = 675
        targetheight = 900
        targetprefix = "gal"
    elif int_targetprefix == 5: #trk
        targetwidth = 160
        targetheight = 120
        targetprefix = "trk"
    elif int_targetprefix == 6: #trf
        targetwidth = 900
        targetheight = 900
        targetprefix = "trf"
    elif int_targetprefix == 7: #fly
        targetwidth = 300
        targetheight = 424
        targetprefix = "fly"
    elif int_targetprefix == 8: #dep
        targetwidth = 192
        targetheight = 176
        targetprefix = "dep"
        forceAspectRatio = True
    elif int_targetprefix == 9: #dpro
        targetwidth = 600
        targetheight = 298
        targetprefix = "dpro"
    else:
        gprint("int_targetprefix switch broke!")
        logging.error("int_targetprefix switch broke!")
        
    logging.debug("Scaling image to %sx%s", targetwidth, targetheight)
    
    targetaspect = float(targetwidth) / float(targetheight)
    #gprint(targetheight)
    #gprint(targetwidth)
    #gprint(targetaspect)
    
    imgheight = pdb.gimp_image_height(image)
    imgwidth = pdb.gimp_image_width(image)
    imgaspect = float(imgwidth) / float(imgheight)
    #gprint(imgheight)
    #gprint(imgwidth)
    #gprint(imgaspect)
    
    pdb.gimp_image_undo_group_start(image)
    
    # we only want to shrink to fit, not enlarge:
    if (imgheight>targetheight) or (imgwidth>targetwidth):
        if  (imgaspect > targetaspect) :
            scalefactor = float(imgwidth) / float(targetwidth)
        else:
            scalefactor = float(imgheight) / float(targetheight)
        
        #gprint("Scaling image...")
        pdb.gimp_image_scale_full(
            image, 
            int(round(imgwidth/scalefactor)), 
            int(round(imgheight/scalefactor)), 
            INTERPOLATION_LANCZOS
        )
    
    #thm prefix is a special case, it must be resized exactly to 150x150
    #dep prefix must be resized to 192x176 (or same aspect ratio)
    #this block assumes the working image has only one layer
    if forceAspectRatio:
        logging.debug('Adding fixed size white layer.')
        thumblayer=image.layers[0]
        whitelayer=thumblayer.copy()
        whitelayer.name = "White Fill"
        whitelayer.mode = NORMAL_MODE
        image.add_layer(whitelayer, -1)
        #turn layer to white
        pdb.gimp_drawable_fill(whitelayer, WHITE_FILL)
        #put layer at bottom
        image.lower_layer(whitelayer) 
        #resize layer to targetwidth * targetheight (centred on top layer)
        xoffset, yoffset = 0, 0
        if image.width < targetwidth:
            xoffset=int((targetwidth - image.width) / 2)
        if image.height < targetheight:
            yoffset=int((targetheight - image.height) / 2)
        whitelayer.resize(targetwidth, targetheight, xoffset, yoffset) #
        pdb.gimp_image_resize_to_layers(image)
    
    if AddWatermark==TRUE:
        watermark(image, targetprefix)
        # There's logic inside watermark() that will avoid
        # watermarking certain target image types (thm, trk, trf).
    
    exportfile(targetprefix, image)
    
    pdb.gimp_image_undo_group_end(image)
    logging.debug("ScaleTo version %s finished", currentversion)
    return

# This is the plugin registration function
register(
    "scaleto", # name
    "ScaleTo_%s" % currentversion, # blurb  
    "This script shrinks the current image to a preset size, then saves it to the appropriate folder", # help
    "Robert K. Bell", # author
    "©2012 Inland Truck Centres", # copy
    "2012/08/24", # date
    "<Image>/MyScripts/ScaleTo", # menupath
    "*", # imagetypes
    [
        (
            PF_OPTION, 
            "int_targetprefix", 
            "Output size:", 
            0, 
            [
                "thm (Thumbnail)",               #0
                "med (Main store image)",        #1
                "pop (Poplet images)",           #2
                "six (eBay images)",             #3
                "gal (Photo Gallery images)",    #4
                "trk (Truck Thumbnails)",        #5
                "trf (Truck Pictures",           #6
                "fly (Flyer previews)",          #7
                "dep (DealerPro product images)",#8
                "dpro (DealerPro truck images)"  #9
            ]
        ), (
            PF_TOGGLE, 
            "AddWatermark", 
            "Add Watermark?", 
            0 # initially True, checked.  Alias PF_BOOL
        ), (
            PF_DIRNAME,
            "output_folder",
            "Output folder:",
            output_folder_func()
        )
    ], 
    [],
    scaleto
)

main()