# -*- coding: utf-8 -*-

import os,tools,traceback,getopt,sys
from PIL import Image

# 处理图片filter: NEAREST , BILINEAR , BICUBIC , ANTIALIAS
def deal_image(infile, outfile):
	img = Image.open(infile)
	
	img = img.resize((img.size[0]*3,img.size[1]*3),Image.NEAREST)
	
	img.save(outfile)
	
# 处理图片文件
def do_images(input,output,*args):
	if input == None and len(args)>0:
		input = args[0]
	if output == None:
		output = input
		
	if os.path.isfile(input):
		deal_image(input, output)
	elif os.path.isdir(input):
		for file in [x for x in os.listdir(input) if x.upper().endswith(".PNG")]:
			deal_image(input + "/" + file, output + "/" + file)
			
# 执行函数
if __name__== '__main__' :
	input = None
	output = None
	
	# 解析命令行
	try:
		opts, args = getopt.getopt(sys.argv[1:], "i:o", ["input=","output="])
		
		for o, a in opts:
			if o in ("-i", "--input"):
				input = a
			elif o in ("-o", "--output"):
				output = a
			
		# 执行命令
		do_images(input,output,*args)
		
	except Exception as e:
		traceback.print_exc()
		os.system('pause')
	

