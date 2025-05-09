-------------------------------------------------------
--- 安全辅助函数
-------------------------------------------------------
local function safeNumber(val)
    if val == nil then return 0 end
    if type(val) == 'string' then return tonumber(val) or 0 end
    return val
end

local function safeString(val)
    if val == nil then return "" end
    return tostring(val)
end

local function logDebug(msg)
    -- 实际使用时可以设置为false关闭调试日志
    local debugMode = true
    if debugMode then print("DEBUG: "..msg) end
end

-------------------------------------------------------
--- 查询条件构建（保持不变）
-------------------------------------------------------
query = 'checked=1 '
storehouse = ""
companyName = "奎屯林丰棉业有限责任公司"
start = ""
ends = ""
lotStart = ""
lotEnd = ""
lotIn = ""

if storehouse ~= "" then
    query = query.." and store_house='"..storehouse.."' "
end

if companyName ~= "" then
    query = query.." and company_name='"..companyName.."' "
end

if start ~= "" then
    query = query.." and store_in_time >='"..start.."' "
end

if ends ~= "" then
    query = query.." and store_in_time <='"..ends.."' "
end

if lotStart ~= "" then
    query = query.." and lot_number>='"..lotStart.."' "
end

if lotEnd ~= "" then
    query = query.." and lot_number <='"..lotEnd.."' "
end

if lotIn ~= "" then
    query = query.." and lot_number in "..lotIn.." "
end

-------------------------------------------------------
--- 主计算函数（完全修复版）
-------------------------------------------------------
function Count(t)
    -- 输入验证
    if t == nil then
        error("输入数据不能为nil")
    end

    -- 字段安全预处理
    local function getField(fieldName)
        local val = t[fieldName]
        logDebug(string.format("字段 %s 原始值: %s", fieldName, tostring(val)))
        return val
    end

    -- 数值型字段
    local LotNumber     = safeString(getField("LotNumber"))
    local Price         = safeNumber(getField("Price"))
    local Packages      = safeNumber(getField("Packages"))
    local B1           = safeNumber(getField("B1"))
    local B2           = safeNumber(getField("B2"))
    local B3           = safeNumber(getField("B3"))
    local B4           = safeNumber(getField("B4"))
    local B5           = safeNumber(getField("B5"))
    local DD1          = safeNumber(getField("DD1"))
    local DD2          = safeNumber(getField("DD2"))
    local DD3          = safeNumber(getField("DD3"))
    local DH1          = safeNumber(getField("DH1"))
    local DH2          = safeNumber(getField("DH2"))
    local DH3          = safeNumber(getField("DH3"))
    local H1           = safeNumber(getField("H1"))
    local H2           = safeNumber(getField("H2"))
    local LAvg         = safeNumber(getField("LAvg"))
    local MAvg         = safeNumber(getField("MAvg"))
    local MA           = safeNumber(getField("MA"))
    local MB1          = safeNumber(getField("MB1"))
    local MB2          = safeNumber(getField("MB2"))
    local MC1          = safeNumber(getField("MC1"))
    local MC2          = safeNumber(getField("MC2"))
    local TAvg         = safeNumber(getField("TAvg"))
    local ZAvg         = safeNumber(getField("ZAvg"))
    local YP1          = safeNumber(getField("YP1"))
    local YP2          = safeNumber(getField("YP2"))
    local YP3          = safeNumber(getField("YP3"))
    local YXXB         = safeNumber(getField("YXXB"))

    -- 字符串型字段
    local Tname        = safeString(getField("Tname"))
    local Home         = safeString(getField("Home"))
    local CompanyName  = safeString(getField("CompanyName"))
    local StoreHouse   = safeString(getField("StoreHouse"))

    -- 初始化返回结构
    local sts = '拒收'
    local reason = ''
    local returnFields = {
        LotNumber, Tname, Home, Packages, LAvg, TAvg, MAvg, ZAvg,
        safeNumber(getField("HZ")), safeNumber(getField("HC")),
        safeNumber(getField("GrossWeight")), safeNumber(getField("Weight")),
        safeString(getField("StoreInTime")), safeString(getField("CertDate")),
        CompanyName, StoreHouse, sts, B1, B2, B3,
        safeNumber(getField("MM28")), safeNumber(getField("MM29")),
        safeNumber(getField("MM30")), safeNumber(getField("MM31")),
        safeNumber(getField("MM32")), MA, MB1, MB2,
        safeNumber(getField("ZU3p")), safeNumber(getField("ZU2p")),
        safeNumber(getField("ZU1p")), safeNumber(getField("TS3p")),
        safeNumber(getField("TS2p")), safeNumber(getField("TS1p"))
    }

    -------------------------------------------------------
    --- 马克隆值检查（安全版）
    -------------------------------------------------------
    local mkCount = 0
    if safeNumber(MA) == 50 then mkCount = mkCount + 1 end
    if safeNumber(MB1) == 50 then mkCount = mkCount + 1 end
    if safeNumber(MB2) == 50 then mkCount = mkCount + 1 end
    if safeNumber(MC1) == 50 then mkCount = mkCount + 1 end
    if safeNumber(MC2) == 50 then mkCount = mkCount + 1 end

    if mkCount >= 2 then
        returnFields[17] = "无法计算"
        return returnFields
    end

    -------------------------------------------------------
    --- 拒收条件判断（安全版）
    -------------------------------------------------------
    -- 包数检查
    if Packages > 190 or Packages < 180 then
        reason = '包数不合格'
        return returnFields
    end

    -- 颜色级检查
    if B5 > 0 or DD3 > 0 or DH1 > 0 or DH2 > 0 or DH3 > 0 or H1 > 0 or H2 > 0 then
        reason = '颜色级不合格'
        return returnFields
    end

    -- 长度检查
    if safeNumber(getField("MM26")) > 0 or safeNumber(getField("MM25")) > 0 then
        reason = '长度不合格'
        return returnFields
    end

    -- 马克隆值检查
    if MC1 > 0 then
        reason = '马值不合格'
        return returnFields
    end

    -- 整齐度检查
    if safeNumber(getField("ZU5")) > 0 then
        reason = '整齐度不合格'
        return returnFields
    end

    -- 断裂比强度检查
    if safeNumber(getField("TS5")) > 0 then
        reason = '强度不合格'
        return returnFields
    end

    -------------------------------------------------------
    --- 开始计算升贴水（安全版）
    -------------------------------------------------------
    sts = 0

    -- 主体颜色级计算
    if B1 > 80 or B2 > 80 or B3 > 80 or B4 > 80 or DD1 > 80 or DD2 > 80 then
        local dominant = false

        -- 白棉主导判断
        if (B1 > 0 and B2 == 0 and B3 == 0 and B4 == 0 and DD1 == 0 and DD2 == 0) or
           (B1 > 0 and B2 > 0 and B3 == 0 and B4 == 0 and DD1 == 0 and DD2 == 0) then
            dominant = true
        -- 其他条件判断...
        end

        if dominant then
            sts = sts + 100
        end
    end

    -- 颜色级加权计算
    sts = sts + B1/100 * 300 + B2/100 * 150 + B3/100 * 0 +
          B4/100*(-300) + DD1/100*(-250) + DD2/100*(-500)

    -- 长度调整
    if LAvg >= 27 and LAvg < 28 then
        sts = sts - 250
    elseif LAvg >= 29 and LAvg < 30 then
        sts = sts + 150
    elseif LAvg >= 30 then
        sts = sts + 400
    end

    -- 马克隆值调整
    local mksrc = {
        MA = MA, MB1 = MB1, MB2 = MB2,
        MC1 = MC1, MC2 = MC2
    }
    local mkAnswerSet = { MA = 100, MB1 = 0, MB2 = 0, MC1 = -150, MC2 = -150 }

    local maxKey = 'MA'
    for k, v in pairs(mksrc) do
        if (mksrc[maxKey] or 0) < (v or 0) then
            maxKey = k
        end
    end
    sts = sts + (mkAnswerSet[maxKey] or 0)

    -- 断裂比强度调整
    if TAvg >= 31 then
        sts = sts + 350
    elseif TAvg >= 29 then
        sts = sts + 150
    elseif TAvg >= 26 then
        sts = sts + 0
    elseif TAvg >= 24 then
        sts = sts - 250
    end

    -- 长度整齐度调整
    if ZAvg >= 86 then
        sts = sts + 250
    elseif ZAvg >= 83 then
        sts = sts + 200
    elseif ZAvg >= 80 then
        sts = sts + 0
    elseif ZAvg >= 77 then
        sts = sts - 200
    end

    -- 轧工质量调整
    sts = sts + YP1/100 * 90 + YP3/100 * (-300)

    -- 异性纤维调整
    if YXXB > 1 then
        sts = sts + (YXXB - 1) * (-200)
    end

    -- 更新最终结果
    returnFields[17] = sts
    return returnFields
end

-------------------------------------------------------
--- 工具函数
-------------------------------------------------------
function FindMax(src, as)
    local maxKey = next(src)
    for key, value in pairs(src) do
        if (src[maxKey] or 0) < (value or 0) then
            maxKey = key
        end
    end
    return as[maxKey] or 0
end

-------------------------------------------------------
--- Excel标题定义（保持不变）
-------------------------------------------------------
title = {
    "批号", "棉花类型", "产地", "合计包数", "长度", "断裂比强度", "马克隆值", "长度整齐度",
    "平均含杂", "平均回潮", "合计毛重", "合计公重", "入库日期", "证书日期", "企业名称",
    "存放仓库", "升贴水", "白棉1级", "白棉2级", "白棉3级", "长度28", "长度29", "长度30",
    "长度31", "长度32", "马值a", "马值b1", "马值b2", "u3", "u2", "u1", "s3", "s2", "s1"
}