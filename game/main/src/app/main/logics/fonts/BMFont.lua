--[[
	BM字体
--]]

local BMFont = class("BMFont", cc.LabelBMFont, require("app.main.modules.font.FontBase"))

-- 类扩展构造
function BMFont:clsctor(config)
	table.merge(self,config)
	self._alias = display.loadImage(self.image)
	self._alias:retain()

	-- 加载字体文件
	self:create("")
end

-- 类扩展析构
function BMFont:clsdtor()
	self._alias:release()
end

-- 构造函数
function BMFont:ctor(text,params)
	if params then
		table.merge(self,params)
	end
	self._scale = self.scale or 1
	self:setFntFile(self.fnt)
	self:setScale(self._scale)
	self:setString(text)
end

-- 析构函数
function BMFont:dtor()
	
end

-- 获得当前字体尺寸
function BMFont:getLabelSize()
	local lsize = self:getContentSize()
	return cc.size(lsize.width * self._scale, lsize.height * self._scale)
end

-- 获得字体的高度
function BMFont:getFontHeight()
	return self.size[2] * self._scale
end

-- 获得字符的宽度(UTF字符)
function BMFont:getCharWidth(uch)
	return ((uch < 256) and self.alphasize[1] or self.size[1]) * self._scale
end

-- 获得字符的最大宽度
function BMFont:getCharMaxWidth()
	return self.size[1] * self._scale
end

-- 获得字体名称
function BMFont:getName()
	return self.name
end

return BMFont
