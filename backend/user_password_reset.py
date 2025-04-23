from db.sys_db import SessionLocal
from app.dependencies.auth_dep import pwd_context
from app.models.sys import SysUser


def update():
    username = input("请输入用户名: ")
    print(f"您输入的用户名: {username}")

    session = SessionLocal()

    try:
        user = session.query(SysUser).filter_by(username=username).first()
        if user is None:
            print(f"用户 {username} 不存在")
            return
        password = input_pass()
        password = pwd_context.hash(password)
        user.password = password
        session.commit()
        print("用户密码修改成功")
    finally:
        session.close()


def input_pass():
    password = input("请输入密码: ")

    repeat_pass = input("请重复密码：")

    if password != repeat_pass:
        print("两次输入的密码不匹配")
        return input_pass()
    return password


try:
    update()
except KeyboardInterrupt as e:
    print('用户中断操作')
except Exception as e:
    print(e)
