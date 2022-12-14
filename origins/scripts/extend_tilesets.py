# -*- coding: utf-8 -*-

import os,tools
from PIL import Image

'''瓦片集更新器'''
class TilesetUpdater:
	def __init__(self):
		self.curpath = os.path.split(os.path.realpath(__file__))[0]
		self.basepath = self.curpath
		self.tlsfile = self.basepath + "/configs/tilesets.json"
	
	def update(self):
		if not os.path.exists(self.tlsfile):
			print("瓦片集配置文件:" + self.tlsfile + "不存在!")
			return
		self.tlsconf = tools.read_json(self.tlsfile)
		self.tlsdir,_ = os.path.split(self.tlsfile)
		
		# 各种配置路径
		self.source = self.tlsdir + "/" + self.tlsconf["source"]
		self.dest = self.tlsdir + "/" + self.tlsconf["dest"]
		
		# 遍历所有配置
		if os.path.isdir(self.source):
			if not os.path.isdir(self.dest):
				os.makedirs(self.dest)
			for tlconf in self.tlsconf["tilesets"]:
				self.gen_tileset(tlconf)
	
	def gen_tileset(self,tlconf):
		imgname = tlconf["image"]
		tilesize = tlconf["tilesize"]
		scale = tlconf["scale"]
		padding = tlconf["padding"]
		dtilesize = [tilesize[0] * scale, tilesize[1] * scale]
		
		iimg = Image.open(self.source + "/" + imgname)
		itsize = (iimg.size[0]//tilesize[0],iimg.size[1]//tilesize[1])
		
		oimg = Image.new(iimg.mode,(itsize[0]*(dtilesize[0]+2*padding),itsize[1]*(dtilesize[1]+2*padding)))
		for iy in range(itsize[1]):
			for ix in range(itsize[0]):
				# 截图
				pc = tools.scale_image(iimg.crop((tilesize[0]*ix,tilesize[1]*iy,tilesize[0]*(ix+1),tilesize[1]*(iy+1))),scale)
				pl = tools.scale_image(iimg.crop((tilesize[0]*ix,tilesize[1]*iy,tilesize[0]*ix+padding,tilesize[1]*(iy+1))),scale)
				pr = tools.scale_image(iimg.crop((tilesize[0]*(ix+1)-padding,tilesize[1]*iy,tilesize[0]*(ix+1),tilesize[1]*(iy+1))),scale)
				pt = tools.scale_image(iimg.crop((tilesize[0]*ix,tilesize[1]*iy,tilesize[0]*(ix+1),tilesize[1]*iy+padding)),scale)
				pb = tools.scale_image(iimg.crop((tilesize[0]*ix,tilesize[1]*(iy+1)-padding,tilesize[0]*(ix+1),tilesize[1]*(iy+1))),scale)
				plt = tools.scale_image(iimg.crop((tilesize[0]*ix,tilesize[1]*iy,tilesize[0]*ix+padding,tilesize[1]*iy+padding)),scale)
				prt = tools.scale_image(iimg.crop((tilesize[0]*(ix+1)-padding,tilesize[1]*iy,tilesize[0]*(ix+1),tilesize[1]*iy+padding)),scale)
				plb = tools.scale_image(iimg.crop((tilesize[0]*ix,tilesize[1]*(iy+1)-padding,tilesize[0]*ix+padding,tilesize[1]*(iy+1))),scale)
				prb = tools.scale_image(iimg.crop((tilesize[0]*(ix+1)-padding,tilesize[1]*(iy+1)-padding,tilesize[0]*(ix+1),tilesize[1]*(iy+1))),scale)
				
				# 粘贴
				dx = ix * (dtilesize[0]+2*padding)
				dy = iy * (dtilesize[1]+2*padding)
				oimg.paste(pc,(dx+padding,dy+padding,dx+padding+dtilesize[0],dy+padding+dtilesize[1]))
				oimg.paste(pl,(dx,dy+padding,dx+padding,dy+padding+dtilesize[1]))
				oimg.paste(pr,(dx+padding+dtilesize[0],dy+padding,dx+2*padding+dtilesize[0],dy+padding+dtilesize[1]))
				oimg.paste(pt,(dx+padding,dy,dx+padding+dtilesize[0],dy+padding))
				oimg.paste(pb,(dx+padding,dy+padding+dtilesize[1],dx+padding+dtilesize[0],dy+2*padding+dtilesize[1]))
				oimg.paste(plt,(dx,dy,dx+padding,dy+padding))
				oimg.paste(prt,(dx+padding+dtilesize[0],dy,dx+2*padding+dtilesize[0],dy+padding))
				oimg.paste(plb,(dx,dy+padding+dtilesize[1],dx+padding,dy+2*padding+dtilesize[1]))
				oimg.paste(prb,(dx+padding+dtilesize[0],dy+padding+dtilesize[1],dx+2*padding+dtilesize[0],dy+2*padding+dtilesize[1]))
				
		oimg.save(self.dest + "/" + imgname)
		
		print("更新瓦片集:" + imgname)
	
if __name__ == "__main__":
	'''
	try:
		TilesetUpdater().update()
		print("瓦片集生成完成")
	except Exception:
		print("异常发生!!!")
	'''
	TilesetUpdater().update()
	
	#print("此脚本已弃用!!!")
	os.system("pause")
	