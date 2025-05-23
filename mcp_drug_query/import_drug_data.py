import csv
import sqlite3


def import_data():
    conn = sqlite3.connect('database/drug_data.db')
    cursor = conn.cursor()

    # 创建表结构
    with open('database/setup_drug_db.sql', 'r') as f:
        cursor.executescript(f.read())

    # 导入CSV数据
    with open('database/drug_data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute('''
                INSERT INTO drugs (name, molecular_formula, indication, side_effects, dosage, approval_year)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                row['name'], row['molecular_formula'], row['indication'],
                row['side_effects'], row['dosage'], int(row['approval_year'])
            ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    import_data()