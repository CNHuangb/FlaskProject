from flask import Flask, request


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello 中国，我爱你"


@app.route("/profile")
def profile():
    return "我是个人中心"

@app.route("/blog/list")
def blog_list():
    return "我是博客列表"



# 带参数的URL
@app.route("/blog/<int:blog_id>")
def blog_detail(blog_id):
    return "您访问的博客是：%s" % blog_id


# 带参数的URL
@app.route("/book/list")
def book_list():
    
    page = request.args.get("page", default=1, type=int)

    return f"您获取的是第{page}的图书列表！"




if __name__ == "__main__":
    app.run(debug=True , host="0.0.0.0")
