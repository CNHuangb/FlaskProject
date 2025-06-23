from flask import Flask, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate





app = Flask(__name__)

# 在APP中传入数据库的配置
# config.py
USERNAME = "root"			    # 数据库登录用户名	
PASSWORD = "bmc.123"			# 数据库登录密码
HOST = "172.16.2.219"			# 数据库服务器地址，若为远程服务器填写对应的IP地址，这里是示例地址
PORT = "3306"				    # 数据库连接端口号，MySQL默认常用端口是3306
DATABASE = "database_learn"	    # 要访问的数据库名称

# 创建统一资源标识符（URI），用于指定数据库连接的详细信息
# SQLALCHEMY_DATABASE_URI的格式为：数据库类型 + 驱动://{登录名}:{密码}@{IP地址}:{端口号}/{数据库名}?charset={编码格式}
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8mb4'





db = SQLAlchemy(app)


# with app.app_context():

#     with db.engine.connect() as conn:
#         rs = conn.execute(db.text('SELECT 1'))
#         print(rs.fetchone())


migrate = Migrate(app, db)


# ORM映射三部曲
# 1.flask db init 只执行一次
# 2.flask db migrate 识别orm模型的改变，生成迁移脚本
# 3.flask db upgrade 运行迁移脚本，同步到数据库中
# 





class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(100), nullable = False )
    password = db.Column(db.String(100), nullable = False )
    email = db.Column(db.String(100))

    signature = db.Column(db.String(100))




class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(200), nullable = False )
    content = db.Column(db.Text, nullable = False )

    # 添加作者外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # backref会自动给user模型添加一个articles的属性，用来获取文章列表
    author = db.relationship("User", backref = "articles")




# user = User(username = "张三", password = "123")


# # 初始的时候时候，后使用migrate代替
# with app.app_context():
#     db.create_all()



@app.route("/")
def hello_world():
    

    return "hello world!"



@app.route("/user/add")
def add_user(): 
    # 创建orm对象
    user = User(username = "张三", password = "123") 

    # 将orm对象添加到db.session中
    db.session.add(user)

    # 将db.session中的改变同步到数据库中
    db.session.commit()

    return "用户创建成功!"



@app.route("/user/query")
def query_user(): 
    # get操作
    
    user = User.query.get(1)
    print(f"{user.id}:{user.username}:{user.password}")



    # filter_by查找

    users = User.query.filter_by(username = "张三")

    for user in users:
        print(user.username)

    return "数据查找成功!"




@app.route("/user/update")
def update_user(): 

    # filter_by查找

    user = User.query.filter_by(username = "张三").first()

    user.password = "666"

    db.session.commit()

    return "数据更新成功!"



@app.route("/user/delete")
def delete_user(): 

    # id查找

    user = User.query.get(1)

    db.session.delete(user)

    db.session.commit()

    return "数据删除成功!"





@app.route("/article/add")
def article_add():
    
    article = Article (title = "Flask学习大纲", content = "Flask学习内容")
    article.author = User.query.get(2)

    article2 = Article (title = "Django学习大纲", content = "Django学习内容")
    article2.author = User.query.get(2)

    # 添加到session中
    db.session.add_all([article,article2])

    db.session.commit()

    return "文章添加成功!"





@app.route("/article/query")
def article_query():
    
    user = User.query.get(2)

    for article in user.articles:
        print(article.title)



    

    return "文章查找成功!"







if __name__ == "__main__":
    app.run(debug=True , host="0.0.0.0")
