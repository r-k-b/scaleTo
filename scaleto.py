#!/usr/bin/env python

# ScaleTo - Python-fu script
# Author: Robert K. Bell
# 
# 
#------------------ To Do -------------------------------------
#	Watermark insertion
#	Error checking
#	
#--------------------------------------------------------------
# CHANGELOG: v059
#	"med" prefix was being scaled to landscape aspect ratio, changed to portrait


from gimpfu import *
import os

# create an output function that redirects to gimp's Error Console
def gprint( text ):
	pdb.gimp_message(text)
	return 
	
# Export the file to the location given by the prefix
# Doesn't check 
def exportfile(prefix, image):
	websafename=(os.path.basename(pdb.gimp_image_get_filename(image))).replace(" ","_")
	
	#if (prefix == 5) or (prefix == 6):
	if (prefix == "trk") or (prefix == "trf"):
		categoryfolder = "trucksales"
	elif prefix == "fly":
		categoryfolder = "flyers"
	else:
		categoryfolder = "products"
		
	#outfile = "P:\\Online_Presence\\img\\"+categoryfolder+"\\"+prefix+"\\"+prefix+"_"+websafename
	#For debugging in console: outfile = "P:\\Online_Presence\\img\\products\\tst\\tst_"+os.path.basename(pdb.gimp_image_get_filename(gimp.image_list()[0]))
	outfile = "P:\\Online_Presence\\img\\%s\\%s\\%s_%s" % (categoryfolder, prefix, prefix, websafename)
	#gprint(outfile)
	pdb.file_jpeg_save(
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
	gprint("Wrote to "+outfile)
	return

# our script
def scaleto(image, drawable, int_targetprefix) :
	# "thm","med","pop","six","gal","trk","trf","fly"
	#targetprefix = "tst"
	if int_targetprefix == 0: #thm
		targetheight = 150
		targetwidth = 150
		targetprefix = "thm"
	elif int_targetprefix == 1: #med
		targetheight = 600
		targetwidth = 430
		targetprefix = "med"
	elif int_targetprefix == 2: #pop
		targetheight = 1000
		targetwidth = 700
		targetprefix = "pop"
	elif int_targetprefix == 3: #six
		targetheight = 1600
		targetwidth = 1200
		targetprefix = "six"
	elif int_targetprefix == 4: #gal
		targetheight = 900
		targetwidth = 675
		targetprefix = "gal"
	elif int_targetprefix == 5: #trk
		targetheight = 160
		targetwidth = 120
		targetprefix = "trk"
	elif int_targetprefix == 6: #trf
		targetheight = 1024
		targetwidth = 768
		targetprefix = "trf"
	elif int_targetprefix == 7: #fly
		targetheight = 300
		targetwidth = 424
		targetprefix = "fly"
	else:
		gprint("int_targetprefix switch broke!")
	
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
	
	exportfile(targetprefix, image)
	pdb.gimp_image_undo_group_end(image)
	
	return

# This is the plugin registration function
register(
	"scaleto",	#name
	"ScaleTo_v0.50", #blurb  
	"This script shrinks the current image to a preset size, then saves it to the appropriate folder", #help
	"Robert K. Bell", #author
	"©2012 Inland Truck Centres", #copy
	"2012/08/24", #date
	"<Image>/MyScripts/ScaleTo", #menupath
	"*", #imagetypes
	[
		(PF_OPTION, "int_targetprefix", "OPTION:", 0, ["thm","med","pop","six","gal","trk","trf","fly"])
	], 
	[],
	scaleto
	)

main()