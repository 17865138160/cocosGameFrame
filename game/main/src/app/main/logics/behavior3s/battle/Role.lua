--[[
	获得战斗的角色
]]

local b3 = require("app.main.modules.behavior3.b3")
local Action = require("app.main.modules.behavior3.core.Action")
local Role = class("Role", Action)

--[[
	Creates an instance of Role.
	properties
		label	标签
]]
function Role:ctor(config)
	config = config or {}
	config.name = config.name or "Role"
	config.title = config.title or "Role <>"
	Action.ctor(self, config)
	self._label = self.properties.label
end

-- Tick method.
function Role:tick(tick)
	if self._label then
		tick.blackboard:set(self._label, tick.target:getRole())
		return b3.SUCCESS
	end
    return b3.FAILURE
end

return Role
