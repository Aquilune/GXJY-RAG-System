CREATE DEFINER = CURRENT_USER TRIGGER `gxjy_rag_system`.`filter_app_productdata_AFTER_INSERT` AFTER INSERT ON `filter_app_productdata` FOR EACH ROW
BEGIN
    DECLARE is_xinjiang BOOLEAN;
    -- 检查新插入记录的仓库是否在新疆仓库列表中
    SELECT
        CASE
            WHEN NEW.warehouse IN (
                '库尔勒汇', '奎屯农资', '兵棉宏泰', '阿拉尔鹏', '库尔勒恒', '新疆中新', '阿克苏银', '伽师瑞利',
                '新疆西部', '乌市诸天', '巴楚棉储', '阿克苏益', '奎屯陆德', '阿克苏铁', '巴楚润金', '库尔勒银',
                '兵棉润泽', '中储库尔', '奎屯银棉', '阿克苏兵', '中供乌苏', '新疆象道', '益美达仓', '昌吉华嵘',
                '阿克苏华', '新疆天运', '乌市棉麻', '大河沿二', '哈密供销', '巴州尉棉', '中锦胡杨', '郓城众誉',
                '新疆锦葵', '奎屯中亚', '莎车中联', '博州新棉', '新疆港汇', '奎屯新亚', '石河子通', '库尔勒大',
                '乌市米泉'
            ) THEN TRUE
            ELSE FALSE
        END INTO is_xinjiang;
    -- 根据判断结果更新 warehouse_area 字段
    IF is_xinjiang THEN
        UPDATE `filter_app_productdata`
        SET warehouse_area = '新疆'
        WHERE id = NEW.id;
    ELSE
        UPDATE `filter_app_productdata`
        SET warehouse_area = '内地'
        WHERE id = NEW.id;
    END IF;
END;