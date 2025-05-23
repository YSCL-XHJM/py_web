-- 创建药物信息表
CREATE TABLE IF NOT EXISTS drugs (
    drug_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    molecular_formula TEXT,
    indication TEXT,
    side_effects TEXT,
    dosage TEXT,
    approval_year INTEGER
);

-- 创建索引优化查询
CREATE INDEX idx_drug_name ON drugs(name);