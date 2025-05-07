-------------------------------------------------------
--- 此处为查询条件的组合
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

function Count(t)
    -------------------------------------------------------
    --- 此处为字段计算 local部分不用改
    -------------------------------------------------------
    local LotNumber     = t["LotNumber"]      -- 批号-
    local Price         = t["Price"]          -- 价格
    local StoreHouse    = t["StoreHouse"]     -- 存放仓库-
    local Home          = t["Home"]           -- 产地-
    local CompanyName   = t["CompanyName"]    -- 企业名称-
    local Address       = t["Address"]        -- 地址
    local Contact       = t["Contact"]        -- 联系人
    local Phone         = t["Phone"]          -- 联系人手机
    local StoreInTime   = t["StoreInTime"]    -- 入库日期
    local Tname         = t["Tname"]          -- 棉花类型
    local Packages      = t["Packages"]       -- 合计包数-
    local GrossWeight   = t["GrossWeight"]    -- 合计毛重
    local PackageWeight = t["PackageWeight"]  -- 合计皮重
    local NetWeight     = t["NetWeight"]      -- 合计净重
    local CertNumber    = t["CertNumber"]     -- 质量结果，证书标号
    local CertDate      = t["CertDate"]       -- 证书日期
    local HC            = t["HC"]             -- 平均回潮
    local HZ            = t["HZ"]             -- 平均含杂
    local Weight        = t["Weight"]         -- 合计公重
    
    -- 颜色
    local B1  = t["B1"]   -- 白棉1级-
    local B2  = t["B2"]   -- 白棉2级-
    local B3  = t["B3"]   -- 白棉3级-
    local B4  = t["B4"]   -- 白棉4级-
    local B5  = t["B5"]   -- 白棉5级
    local DD1 = t["DD1"]  -- 淡点污棉1级-
    local DD2 = t["DD2"]  -- 淡点污棉2级-
    local DD3 = t["DD3"]  -- 淡点污棉3级
    local DH1 = t["DH1"]  -- 淡黄染棉1级
    local DH2 = t["DH2"]  -- 淡黄染棉2级
    local DH3 = t["DH3"]  -- 淡黄染棉2级
    local H1  = t["H1"]   -- 黄染棉1级
    local H2  = t["H2"]   -- 黄染棉2级
    
    -- 长度
    local LAvg = t["LAvg"]  -- 长度平均值-
    local LMax = t["LMax"]  -- 长度最大值-
    local LMin = t["LMin"]  -- 长度最小值-
    local MM25 = t["MM25"]  -- 25mm-
    local MM26 = t["MM26"]  -- 26mm-
    local MM27 = t["MM27"]  -- 27mm-
    local MM28 = t["MM28"]  -- 28mm-
    local MM29 = t["MM29"]  -- 29mm-
    local MM30 = t["MM30"]  -- 30mm-
    local MM31 = t["MM31"]  -- 31mm-
    local MM32 = t["MM32"]  -- 32mm-
    
    -- 马克隆值
    local MAvg = t["MAvg"]  -- 马克隆值平均值-
    local MMax = t["MMax"]  -- 马克隆值最大值-
    local MMin = t["MMin"]  -- 马克隆值最小值-
    local MA   = t["MA"]    -- 马克隆值A-
    local MB1  = t["MB1"]   -- 马克隆值B1-
    local MC1  = t["MC1"]   -- 马克隆值C1-
    local MB2  = t["MB2"]   -- 马克隆值B2-
    local MC2  = t["MC2"]   -- 马克隆值C2-
    
    -- 轧工质量
    local YP1 = t["YP1"]  -- 轧工质量P1-
    local YP2 = t["YP2"]  -- 轧工质量P2-
    local YP3 = t["YP3"]  -- 轧工质量P3-
    
    -- 长度整齐度
    local ZAvg = t["ZAvg"]  -- 平均-
    local ZMax = t["ZMax"]  -- 最大-
    local ZMin = t["ZMin"]  -- 最小-
    local ZU1  = t["ZU1"]   -- 各整齐度比例 U1-
    local ZU1p = t["ZU1p"]  -- 各整齐度比例 U1平均-
    local ZU2  = t["ZU2"]   -- 各整齐度比例 U2-
    local ZU2p = t["ZU2p"]  -- 各整齐度比例 U2平均-
    local ZU3  = t["ZU3"]   -- 各整齐度比例 U3-
    local ZU3p = t["ZU3p"]  -- 各整齐度比例 U3平均-
    local ZU4  = t["ZU4"]   -- 各整齐度比例 U4-
    local ZU4p = t["ZU4p"]  -- 各整齐度比例 U4平均-
    local ZU5  = t["ZU5"]   -- 各整齐度比例 U5-
    local ZU5p = t["ZU5p"]  -- 各整齐度比例 U5平均-
    
    -- 断裂比强度
    local TAvg = t["TAvg"]  -- 平均-
    local TMax = t["TMax"]  -- 最大-
    local TMin = t["TMin"]  -- 最小-
    local TS1  = t["TS1"]   -- 各断裂比强度比例S1-
    local TS1p = t["TS1p"]  -- 各断裂比强度比例S1 平均-
    local TS2  = t["TS2"]   -- 各断裂比强度比例S2-
    local TS2p = t["TS2p"]  -- 各断裂比强度比例S2 平均-
    local TS3  = t["TS3"]   -- 各断裂比强度比例S3-
    local TS3p = t["TS3p"]  -- 各断裂比强度比例S3 平均-
    local TS4  = t["TS4"]   -- 各断裂比强度比例S4-
    local TS4p = t["TS4p"]  -- 各断裂比强度比例S4 平均-
    local TS5  = t["TS5"]   -- 各断裂比强度比例S5-
    local TS5p = t["TS5p"]  -- 各断裂比强度比例S5 平均-
    local RD   = t["RD"]    -- RD
    local Bplus = t["Bplus"] -- B+
    local YXXB = t["YXXB"]  -- 异性纤维包数
    local Unit = t["Unit"]  -- 检验单位
    local Checked = t["Checked"]  -- 是否公检

    local sts = '拒收'
    local reason = ''
    local returnFileds = {
        LotNumber, Tname, Home, Packages, LAvg, TAvg, MAvg, ZAvg, HZ, HC, 
        GrossWeight, Weight, StoreInTime, CertDate, CompanyName, StoreHouse, 
        sts, B1, B2, B3, MM28, MM29, MM30, MM31, MM32, MA, MB1, MB2, 
        ZU3p, ZU2p, ZU1p, TS3p, TS2p, TS1p
    }
    
    -------------------------------------------------------
    --- 计算马克50%，判断是否拒收
    -------------------------------------------------------
    local mkCount = 0
    if MA == 50 then mkCount = mkCount + 1 end
    if MB1 == 50 then mkCount = mkCount + 1 end
    if MB2 == 50 then mkCount = mkCount + 1 end
    if MC1 == 50 then mkCount = mkCount + 1 end
    if MC2 == 50 then mkCount = mkCount + 1 end

    if mkCount >= 2 then
        return {
            LotNumber, Tname, Home, Packages, LAvg, TAvg, MAvg, ZAvg, HZ, HC, 
            GrossWeight, Weight, StoreInTime, CertDate, CompanyName, StoreHouse, 
            "无法计算", B1, B2, B3, MM28, MM29, MM30, MM31, MM32, MA, MB1, MB2, 
            ZU3p, ZU2p, ZU1p, TS3p, TS2p, TS1p
        }
    end

    -------------------------------------------------------
    --- 计算sts，判断是否拒收
    -------------------------------------------------------
    if Packages > 190 or Packages < 180 then
        sts = '拒收'
        reason = '包数不合格'
        return returnFileds
    end

    if B5 > 0 or DD3 > 0 or DH1 > 0 or DH2 > 0 or DH3 > 0 or H1 > 0 or H2 > 0 then
        sts = '拒收'
        reason = 'B5>0 or DD3>0 or DH1>0 or DH2>0 or DH3>0 or H1>0 or H2>0不合格'
        return returnFileds
    end

    if MM26 > 0 or MM25 > 0 then
        sts = '拒收'
        reason = '长度不合格'
        return returnFileds
    end

    if MC1 > 0 then
        sts = '拒收'
        reason = '马值不合格'
        return returnFileds
    end

    if ZU5 > 0 then
        sts = '拒收'
        reason = 'ZU5不合格'
        return returnFileds
    end

    if TS5 > 0 then
        sts = '拒收'
        reason = 'TS5不合格'
        return returnFileds
    end

    sts = 0
    -------------------------------------------------------------------------------------------------------------
    --- 计算sts，判定是否有主体颜色级模块 满足以下条件输出100然后累加按比例计算颜色级，如果没有主体颜色级则按照比例相乘累加
    -------------------------------------------------------------------------------------------------------------
    if B1 > 80 or B2 > 80 or B3 > 80 or B4 > 80 or DD1 > 80 or DD2 > 80 then
        if (B1 > 0 and B2 == 0 and B3 == 0 and B4 == 0 and DD1 == 0 and DD2 == 0) or 
           (B1 > 0 and B2 > 0 and B3 == 0 and B4 == 0 and DD1 == 0 and DD2 == 0) or 
           (B1 > 0 and DD1 > 0 and B2 == 0 and B3 == 0 and B4 == 0 and DD2 == 0) or 
           (B1 > 0 and DD1 > 0 and B2 > 0 and B3 == 0 and B4 == 0 and DD2 == 0) or 
           (B2 > 0 and DD1 > 0 and B1 > 0 and B3 == 0 and B4 == 0 and DD2 == 0) or 
           (B2 > 0 and DD1 > 0 and B3 > 0 and B1 == 0 and B4 == 0 and DD2 == 0) or 
           (B2 > 0 and B1 > 0 and B3 > 0 and B4 == 0 and DD1 == 0 and DD2 == 0) or 
           (B2 > 0 and DD1 > 0 and B1 == 0 and B3 == 0 and B4 == 0 and DD2 == 0) or 
           (B2 > 0 and B1 > 0 and B3 == 0 and B4 == 0 and DD1 == 0 and DD2 == 0) or 
           (B2 > 0 and B3 > 0 and B1 == 0 and B4 == 0 and DD1 == 0 and DD2 == 0) then
            sts = sts + 100
        elseif (B3 > 0 and B1 == 0 and B2 == 0 and B4 == 0 and DD1 == 0 and DD2 == 0) or 
               (B3 > 0 and DD1 > 0 and B1 == 0 and B2 == 0 and B4 == 0 and DD2 == 0) or 
               (B3 > 0 and DD2 > 0 and B1 == 0 and B2 == 0 and B4 == 0 and DD1 == 0) or 
               (B3 > 0 and B2 > 0 and B1 == 0 and B4 == 0 and DD1 == 0 and DD2 == 0) or 
               (B3 > 0 and B4 > 0 and B1 == 0 and B2 == 0 and DD1 == 0 and DD2 == 0) or 
               (B3 > 0 and DD1 > 0 and DD2 > 0 and B1 == 0 and B2 == 0 and B4 == 0) or 
               (B3 > 0 and DD2 > 0 and B2 > 0 and B1 == 0 and B4 == 0 and DD1 == 0) or 
               (B3 > 0 and B2 > 0 and B4 > 0 and B1 == 0 and DD1 == 0 and DD2 == 0) or 
               (B3 > 0 and DD1 > 0 and B2 > 0 and B1 == 0 and B4 == 0 and DD2 == 0) or 
               (B3 > 0 and DD1 > 0 and B4 > 0 and B1 == 0 and B2 == 0 and DD2 == 0) or 
               (B3 > 0 and DD2 > 0 and B4 > 0 and B1 == 0 and B2 == 0 and DD1 == 0) then
            sts = sts + 100
        elseif (B4 > 0 and B1 == 0 and B2 == 0 and B3 == 0 and DD1 == 0 and DD2 == 0) or 
               (B4 > 0 and DD2 > 0 and B1 == 0 and B2 == 0 and B3 == 0 and DD1 == 0) or 
               (B4 > 0 and B3 > 0 and B1 == 0 and B2 == 0 and DD1 == 0 and DD2 == 0) or 
               (B4 > 0 and DD2 > 0 and B3 > 0 and B1 == 0 and B2 == 0 and DD1 == 0) then
            sts = sts + 100
        elseif (DD1 > 0 and B1 == 0 and B2 == 0 and B3 == 0 and B4 == 0 and DD2 == 0) or 
               (DD1 > 0 and B1 > 0 and B2 == 0 and B3 == 0 and B4 == 0 and DD2 == 0) or 
               (DD1 > 0 and B1 > 0 and B2 > 0 and B3 == 0 and B4 == 0 and DD2 == 0) or 
               (DD1 > 0 and B1 > 0 and B3 > 0 and B2 == 0 and B4 == 0 and DD2 == 0) or 
               (DD1 > 0 and B1 > 0 and DD2 > 0 and B2 == 0 and B3 == 0 and B4 == 0) or 
               (DD1 > 0 and B2 > 0 and B1 == 0 and B3 == 0 and B4 == 0 and DD2 == 0) or 
               (DD1 > 0 and B2 > 0 and B3 > 0 and B1 == 0 and B4 == 0 and DD2 == 0) or 
               (DD1 > 0 and B2 > 0 and DD2 > 0 and B1 == 0 and B3 == 0 and B4 == 0) or 
               (DD1 > 0 and B3 > 0 and B1 == 0 and B2 == 0 and B4 == 0 and DD2 == 0) or 
               (DD1 > 0 and B3 > 0 and DD2 > 0 and B1 == 0 and B2 == 0 and B4 == 0) or 
               (DD1 > 0 and DD2 > 0 and B1 == 0 and B2 == 0 and B3 == 0 and B4 == 0) then
            sts = sts + 100
        elseif (DD2 > 0 and B1 == 0 and B2 == 0 and B3 == 0 and B4 == 0 and DD1 == 0) or 
               (DD2 > 0 and B3 > 0 and B1 == 0 and B2 == 0 and B4 == 0 and DD1 == 0) or 
               (DD2 > 0 and B3 > 0 and B4 > 0 and B1 == 0 and B2 == 0 and DD1 == 0) or 
               (DD2 > 0 and B3 > 0 and DD1 > 0 and B1 == 0 and B2 == 0 and B4 == 0) or 
               (DD2 > 0 and B4 > 0 and B1 == 0 and B2 == 0 and B3 == 0 and DD1 == 0) or 
               (DD2 > 0 and B4 > 0 and DD1 > 0 and B1 == 0 and B2 == 0 and B3 == 0) or 
               (DD2 > 0 and DD1 > 0 and B1 == 0 and B2 == 0 and B3 == 0 and B4 == 0) then
            sts = sts + 100
        end
    end
    sts = sts + B1/100 * 300 + B2/100 * 150 + B3/100 * 0 + B4/100*(-300) + DD1/100*(-250) + DD2/100*(-500)

    -------------------------------------------------------------------------------------------------------------
    --- 判定平均长度范围
    -------------------------------------------------------------------------------------------------------------
    if LAvg >= 27 and LAvg < 28 then
        sts = sts - 250
    elseif LAvg >= 29 and LAvg < 30 then
        sts = sts + 150
    elseif LAvg >= 30 then
        sts = sts + 400
    end

    -------------------------------------------------------------------------------------------------------------
    --- 判定马克隆值归属档
    -------------------------------------------------------------------------------------------------------------
    local mksrc = { ['MA'] = MA, ['MB1'] = MB1, ['MB2'] = MB2, ['MC1'] = MC1, ['MC2'] = MC2 }
    local mkAnswerSet = { ['MA'] = 100, ['MB1'] = 0, ['MB2'] = 0, ['MC1'] = -150, ['MC2'] = -150 }
    sts = sts + FindMax(mksrc, mkAnswerSet)

    -------------------------------------------------------------------------------------------------------------
    --- 判定断裂比强度
    -------------------------------------------------------------------------------------------------------------
    if TAvg >= 31 then
        sts = sts + 350
    elseif TAvg >= 29 and TAvg <= 30.9 then
        sts = sts + 150
    elseif TAvg >= 26 and TAvg <= 28.9 then
        sts = sts + 0
    elseif TAvg >= 24 and TAvg <= 25.9 then
        sts = sts - 250
    else
        sts = sts + 0
    end

    -------------------------------------------------------------------------------------------------------------
    --- 判定长度整齐度归档
    -------------------------------------------------------------------------------------------------------------
    if ZAvg >= 86 then
        sts = sts + 250
    elseif ZAvg >= 83 and ZAvg <= 85.9 then
        sts = sts + 200
    elseif ZAvg >= 80 and ZAvg <= 82.9 then
        sts = sts + 0
    elseif ZAvg >= 77 and ZAvg <= 79.9 then
        sts = sts - 200
    else
        sts = sts + 0
    end

    -------------------------------------------------------------------------------------------------------------
    --- 判定轧工质量
    -------------------------------------------------------------------------------------------------------------
    local ygsrc = { ['YP1'] = YP1, ['YP2'] = YP2, ['YP3'] = YP3 }
    local ygAnswerSet = { ['YP1'] = 90, ['YP2'] = 0, ['YP3'] = -190 }
    sts = sts + YP1/100 * 90 + YP3/100 * (-300)

    -------------------------------------------------------------------------------------------------------------
    --- 判定异性纤维数量
    -------------------------------------------------------------------------------------------------------------
    if YXXB > 1 then 
        sts = sts + (YXXB - 1) * (-200)
    end

    return {
        LotNumber, Tname, Home, Packages, LAvg, TAvg, MAvg, ZAvg, HZ, HC, 
        GrossWeight, Weight, StoreInTime, CertDate, CompanyName, StoreHouse, 
        sts, B1, B2, B3, MM28, MM29, MM30, MM31, MM32, MA, MB1, MB2, 
        ZU3p, ZU2p, ZU1p, TS3p, TS2p, TS1p
    }
end

-------------------------------------------------------
--- 此处为定义Excel的一些信息
-------------------------------------------------------
title = {
    "批号", "棉花类型", "产地", "合计包数", "长度", "断裂比强度", "马克隆值", "长度整齐度", 
    "平均含杂", "平均回潮", "合计毛重", "合计公重", "入库日期", "证书日期", "企业名称", 
    "存放仓库", "升贴水", "白棉1级", "白棉2级", "白棉3级", "长度28", "长度29", "长度30", 
    "长度31", "长度32", "马值a", "马值b1", "马值b2", "u3", "u2", "u1", "s3", "s2", "s1"
}

-------------------------------------------------------
--- 此处为定义公共方法
-------------------------------------------------------
function FindMax(src, as)
    local maxKey = ''
    local max = -1
    for key, value in pairs(src) do
        if max < value then
            maxKey = key
            max = value
        end
    end
    return as[maxKey]
end