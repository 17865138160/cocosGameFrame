--[[
	日志管理器
--]]
local THIS_MODULE = ...

-- 日志等级
local C_LEVEL = {
	VERBOSE = 1,	-- 啰嗦
	DEBUG 	= 2,	-- 调试
	INFO 	= 3,	-- 信息
	WARN 	= 4,	-- 警告
	ERROR 	= 5,	-- 错误
	SILENT 	= 6,	-- 寂静,用于关闭日志
}

-- 日志等级标识
local C_LFLAG = {
	[C_LEVEL.VERBOSE] 	= "V",
	[C_LEVEL.DEBUG] 	= "D",
	[C_LEVEL.INFO] 		= "I",
	[C_LEVEL.WARN] 		= "W",
	[C_LEVEL.ERROR] 	= "E",
	[C_LEVEL.SILENT] 	= "S",
}

local utils = cc.safe_require("utils")
local LogManager = class("LogManager")

LogManager.LEVEL = C_LEVEL	-- 日志等级

-- 获得单例对象
local instance = nil
function LogManager:getInstance()
	if instance == nil then
		instance = LogManager:create()
	end
	return instance
end

-- 构造函数
function LogManager:ctor()
	self._loglevel = C_LEVEL.VERBOSE								-- 日志输出等级
	self._logformat = handler(self,LogManager._defaultLogFormat)	-- 日志格式函数
end

--[[
	默认日志格式化函数
	config	
		level	等级
		tag		标签
		thread	线程
	content		日志内容
]]
function LogManager:_defaultLogFormat(config, content)
	return string.format("%s %s %s%s - ", 
		os.date("%m-%d %H:%M:%S"), 
		config.thread or "[NET]", 
		C_LFLAG[config.level], 
		config.tag and ("/" .. config.tag) or "") .. content
end

-- 设置日志输出等级
function LogManager:setLogLevel(level)
	self._loglevel = level
end

-- 设置刷新缓冲区等级
function LogManager:setFlushLevel(level) end

-- 设置日志缓冲区大小
function LogManager:setBufferSize(size) end

--[[
	设置日志格式化函数
	format		格式化函数
]]
function LogManager:setLogFormat(format)
	self._logformat = format
	if not format then
		self._logformat = handler(self,LogManager._defaultLogFormat)
	end
end

--[[
	写入日志
	config	
		level	等级
		tag		标签
		thread	线程	
	fmt			格式字符串
	... 		日志参数
]]
function LogManager:_writeLog(config, fmt, ...)
	if config.level >= self._loglevel then
		local content = string.format(fmt, ...)
		local log = self._logformat(config, content)
		self:_writeContent(config.level, log)
	end
end

--[[
	写入日志内容
	log		日志字符串
]]
function LogManager:_writeContent(level, log)
	writeChannel:push("LOG", level, log)
end

-- 完全写入日志缓冲
function LogManager:flushLog() end

-- 输出 VERBOSE 日志
function LogManager:verbose(config, fmt, ...)
	if type(config) ~= "table" then
		config = { tag = config }
	end
	config.level = C_LEVEL.VERBOSE
	self:_writeLog(config, fmt, ...)
end

-- 输出 DEBUG 日志
function LogManager:debug(config, fmt, ...)
	if utils.isDebug() then
		if type(config) ~= "table" then
			config = { tag = config }
		end
		config.level = C_LEVEL.DEBUG
		self:_writeLog(config, fmt, ...)
	end
end

-- 输出 INFO 日志
function LogManager:info(config, fmt, ...)
	if type(config) ~= "table" then
		config = { tag = config }
	end
	config.level = C_LEVEL.INFO
	self:_writeLog(config, fmt, ...)
end

-- 输出 WARN 日志
function LogManager:warn(config, fmt, ...)
	if type(config) ~= "table" then
		config = { tag = config }
	end
	config.level = C_LEVEL.WARN
	self:_writeLog(config, fmt, ...)
end

-- 输出 ERROR 日志
function LogManager:error(config, fmt, ...)
	if type(config) ~= "table" then
		config = { tag = config }
	end
	config.level = C_LEVEL.ERROR
	self:_writeLog(config, fmt, ...)
end

return LogManager
