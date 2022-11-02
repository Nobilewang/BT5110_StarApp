from flask import Blueprint,jsonify,url_for,render_template

bp=Blueprint("book",__name__,url_prefix="/book")

books=[{"id":1,"name":"yi"},
       {"id":2,"name":"er"},
       {"id":3,"name":"san"},
       {"id":4,"name":"si"}]

@bp.route('/list')
# def book_list():
#     for book in books:
#         book['url']= url_for("book_detail",book_id=book['id'])
#     return jsonify(books)

def book_render():
    return render_template("book_list.html")
