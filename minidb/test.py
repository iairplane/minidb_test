import pytest
import minidb
import os

# 定义一个模型（对应需求中的“定义表结构”功能点）
class User(minidb.Model):
    name = str
    age = int

def test_basic_workflow():
    # 1. 初始化数据库 (测试点: Store 创建)
    db = minidb.Store(debug=True)
    db.register(User)

    # 2. 插入数据 (测试点: 保存功能)
    # 黑盒测试：等价类 - 正常输入
    u1 = User(name="Alice", age=25)
    u1.save(db)
    assert u1.id is not None

    # 3. 查询数据 (测试点: 条件负载)
    # 白盒测试：确保跑到了 load 内部的 SQL 拼接逻辑
    results = list(User.load(db, User.c.name == "Alice"))
    assert len(results) == 1
    assert results[0].age == 25

    # 4. 更新数据 (测试点: Update 逻辑)
    u1.name = "Bob"
    u1.save() # 自动识别 db
    
    # 验证更新是否成功
    updated_user = User.get(db, id=u1.id)
    assert updated_user.name == "Bob"

    db.close()