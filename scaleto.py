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
	Why does it choke on png/gif/anything other than jpeg?
	Verbose logging
	
--------------------------------------------------------------
"""
currentversion = "v070"
"""
CHANGELOG: 
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
	"med" prefix was being scaled to landscape aspect ratio, changed to portrait
"""

from gimpfu import *
import os, logging, sys

# create an output function that redirects to gimp's Error Console
def gprint( text ):
	pdb.gimp_message(text)
	return 
	
# Export the file to the location given by the prefix
# Doesn't check 
def exportfile(prefix, image):
	websafename=(os.path.basename(pdb.gimp_image_get_filename(image))).replace(" ","_")
	
	#this always outputs JPEG format images, change the filename to match.
	#Assumes the image had a dot-seperated file extension.
	websafename=".".join(websafename.split(".")[:-1])+".jpg"
	
	#if (prefix == 5) or (prefix == 6):
	if (prefix == "trk") or (prefix == "trf"):
		categoryfolder = "trucksales"
	elif prefix == "fly":
		categoryfolder = "flyers"
	else:
		categoryfolder = "products"
		
	#For debugging in console: outfile = "P:\\Online_Presence\\img\\products\\tst\\tst_"+os.path.basename(pdb.gimp_image_get_filename(gimp.image_list()[0]))
	#outfile = "P:\\Online_Presence\\img\\"+categoryfolder+"\\"+prefix+"\\"+prefix+"_"+websafename
	outfile = "P:\\Online_Presence\\img\\%s\\%s\\%s_%s" % (categoryfolder, prefix, prefix, websafename)
	logging.debug('Outpile path and file is: %s', outfile)
	
	saveresults = pdb.file_jpeg_save(
		#RUN_NONINTERACTIVE, #run-mode
		image, #input image
		pdb.gimp_image_flatten(image), #drawable to save
		outfile, #The name of the file to save the image in
		outfile, #The name of the file to save the image in
		float(0.90), #quality
		float(0), #smoothing
		1, #optimize
		1, #progressive
		"", #comment
		1, #subsmp
		1, #baseline
		0, #restart
		0); #dct algorithm
		
	#gprint("Wrote to "+outfile)
	logging.debug('Save operation returned: %s', saveresults)
	
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
	else:
		skipwatermark = True;
		logging.debug('Skipping watermark process.')
	
	if not skipwatermark:
		watermarkfile = "//dubb007/G Drive/Logos/Inland group/%s"%watermarkfilename
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
	
	logging.basicConfig(filename='ScaleTo.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')
	logging.debug("Scaleto version %s started.", currentversion)
	
	# "thm","med","pop","six","gal","trk","trf","fly"
	# targetprefix = "tst"
	if int_targetprefix == 0: #thm
		targetwidth = 150
		targetheight = 150
		targetprefix = "thm"
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
	else:
		gprint("int_targetprefix switch broke!")
		
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
	if (imgheight>targetheight) or (imgwidth>targetwidth): # we only want to shrink to fit, not enlarge
		if  (imgaspect > targetaspect) :
			scalefactor = float(imgwidth) / float(targetwidth)
		else:
			scalefactor = float(imgheight) / float(targetheight)
		
		#gprint("Scaling image...")
		pdb.gimp_image_scale_full( image, int(round(imgwidth/scalefactor)), int(round(imgheight/scalefactor)), INTERPOLATION_LANCZOS )
	
	#thm prefix is a special case, it must be resized exactly to 150x150
	#this block assumes the working image has only one layer
	if targetprefix=="thm":
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
		#resize layer to 150x150 (centred on top layer)
		xoffset,yoffset=0,0
		if image.width<150:
			xoffset=int((150-image.width)/2)
		if image.height<150:
			yoffset=int((150-image.height)/2)
		whitelayer.resize(150,150,xoffset,yoffset)
		pdb.gimp_image_resize_to_layers(image)
	
	if AddWatermark==TRUE:
		watermark(image, targetprefix)
		# There's logic inside watermark() that will avoid watermarking certain target image types (thm, trk, trf.
	
	exportfile(targetprefix, image)
	
	pdb.gimp_image_undo_group_end(image)
	logging.debug("ScaleTo version %s finished", currentversion)
	return

# This is the plugin registration function
register(
	"scaleto",	#name
	"ScaleTo_%s"%currentversion, #blurb  
	"This script shrinks the current image to a preset size, then saves it to the appropriate folder", #help
	"Robert K. Bell", #author
	"©2012 Inland Truck Centres", #copy
	"2012/08/24", #date
	"<Image>/MyScripts/ScaleTo", #menupath
	"*", #imagetypes
	[
		(PF_OPTION, "int_targetprefix", "OPTION:", 0, ["thm (Thumbnail)","med (Main store image)","pop (Poplet images)","six (eBay images)","gal (Photo Gallery images)","trk (Truck Thumbnails)","trf (Truck Pictures","fly (Flyer previews)"]),
		(PF_TOGGLE, "AddWatermark",   "Add Watermark?", 1) # initially True, checked.  Alias PF_BOOL
	], 
	[],
	scaleto
	)

main()