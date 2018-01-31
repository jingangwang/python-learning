import re

from bs4 import BeautifulSoup, Comment

html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
# 或者打开某个html文件 soup = BeautifulSoup(open("index.html"))
soup = BeautifulSoup(html_doc, "html.parser")

tag = soup.p
# 获取标签的类型
print(type(tag))  # <class 'bs4.element.Tag'>
# 获取标签的名字
print(tag.name)   # p
# 获取标签的class属性的值
print(tag['class'])  # ['title']
# 获取标签的所有属性
print(tag.attrs)    # {'class': ['title']}

css_soup = BeautifulSoup('<p class="body strikeout"></p>', "html.parser")
# 获取多值属性
print(css_soup.p['class'])  # ['body', 'strikeout']
# 获取标签内容
print(tag.string)  # The Dormouse's story
# 获取标签内容的类型，字符串用NavigableString来包装
print(type(tag.string))  # <class 'bs4.element.NavigableString'>

# 将标签的内容替换
tag.string.replace_with("No longer bold")
print(tag)     # <p class="title"><b>No longer bold</b></p>

# BeautifulSoup 对象表示的是一个文档的全部内容
print(soup.name)  # [document]

markup = "<b><!--Hey, buddy. Want to buy a used parser?--></b>"
soup = BeautifulSoup(markup, "html.parser")
comment = soup.b.string
# 获取注释的类型Comment，Comment 对象是一个特殊类型的 NavigableString 对象
print(type(comment))  # <class 'bs4.element.Comment'>
# 以漂亮的格式输出
# <b>
#  <!--Hey, buddy. Want to buy a used parser?-->
# </b>
print(soup.b.prettify())

# 遍历文档树
soup = BeautifulSoup(html_doc, "html.parser")
# 直接获取head节点
print(soup.head)  # <head><title>The Dormouse's story</title></head>
# 直接获取title节点
print(soup.title)  # <title>The Dormouse's story</title>
# 获取body元素内的第一个b标签
print(soup.body.b)  # <b>The Dormouse's story</b>
# 获取文档内的第一个a标签
print(soup.a)  # <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
# 获取文档内的所有a标签
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister"
# href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie"
# id="link3">Tillie</a>]
print(soup.find_all('a'))
# 通过.contents 获取head标签的所有子节点，以列表形式返回
print(soup.head.contents)  # [<title>The Dormouse's story</title>]
# 通过.children获取head的所有子节点
# 结果：<title>The Dormouse's story</title>
for child in soup.head.children:
    print(child)
# 通过.descendants获取head的所有子孙节点
# 结果：
# <title>The Dormouse's story</title>
# The Dormouse's story
for child in soup.head.descendants:
    print(child)
# 获取整个文档的子节点也就是一个html节点
print(len(list(soup.children)))  # 1
# 获取整个文档的所有子孙节点的数量
print(len(list(soup.descendants)))  # 26
# 获取文档内的所有的字符串
# 结果：
# "The Dormouse's story"
# '\n'
# '\n'
# "The Dormouse's story"
# '\n'
# 'Once upon a time there were three little sisters; and their names were\n'
# 'Elsie'
# ',\n'
# 'Lacie'
# ' and\n'
# 'Tillie'
# ';\nand they lived at the bottom of a well.'
# '\n'
# '...'
# '\n'
for string in soup.strings:
    print(repr(string))
# 获取文档内的所有字符串，去除多余的空白
# 结果：
# "The Dormouse's story"
# "The Dormouse's story"
# 'Once upon a time there were three little sisters; and their names were'
# 'Elsie'
# ','
# 'Lacie'
# 'and'
# 'Tillie'
# ';\nand they lived at the bottom of a well.'
# '...'
for string in soup.stripped_strings:
    print(repr(string))

title_tag = soup.title
# 通过.parent 查找title节点的父节点
print(title_tag.parent)  # <head><title>The Dormouse's story</title></head>
# 获取所有title_tag的父节点
# 结果：
# head
# html
# [document]
for parent in title_tag.parents:
    print(parent.name)

sibling_soup = BeautifulSoup("<a><b>text1</b><c>text2</c></b></a>", "html.parser")
# 通过.next_sibling获取节点的下一个兄弟节点
print(sibling_soup.b.next_sibling)  # <c>text2</c>
print(sibling_soup.c.next_sibling)  # None
# 通过.previous_sibling获取节点的前一个系统第节点
print(sibling_soup.c.previous_sibling)  # <b>text1</b>
print(sibling_soup.b.previous_sibling)  # None
# 通过.next_siblings查找a标签的所有兄弟节点
# 结果：
# ',\n'
# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
# ' and\n'
# <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
# ';\nand they lived at the bottom of a well.'
for sibling in soup.a.next_siblings:
    print(repr(sibling))
# 通过.previous_siblings查找id为link3的所有前置兄弟节点
# 结果：
# ' and\n'
# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
# ',\n'
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
# 'Once upon a time there were three little sisters; and their names were\n'
for sibling in soup.find(id="link3").previous_siblings:
    print(repr(sibling))

last_a_tag = soup.find("a", id="link3")
# 查找最后一个a标签的下一个被解析的对象
# 和next_sibling 区别在于是被解析的下一个对象，不是下一个对象
print(last_a_tag.next_element)  # Tillie
# 查找最后一个a标签的上一个被解析的对象
print(repr(last_a_tag.previous_element))  # ' and\n'
# 查找最后一个a标签之后的所有被解析对象
# 结果：
# 'Tillie'
# ';\nand they lived at the bottom of a well.'
# '\n'
# <p class="story">...</p>
# '...'
# '\n'
for element in last_a_tag.next_elements:
    print(repr(element))

# 查找文档的所有b标签
print(soup.find_all('b'))   # [<b>The Dormouse's story</b>]
# 查找所有以b开头的标签
# 结果：
# body
# b
for tag in soup.find_all(re.compile("^b")):
    print(tag.name)
# 查找所有包含t的标签
# 结果：
# html
# title
for tag in soup.find_all(re.compile("t")):
    print(tag.name)
# 传入一个列表查找元素
# 结果：[<b>The Dormouse's story</b>, <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister"
# href="http://example.com/tillie" id="link3">Tillie</a>]
print(soup.find_all(['a', 'b']))
# 匹配所有元素，但是不会返回字符串节点
for tag in soup.find_all(True):
    print(tag.name)


# 定义过滤方法
def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')


# 通过自定义方法实现过滤
# 结果： [<p class="title"><b>The Dormouse's story</b></p>, <p class="story">Once upon a time there were
# three little sisters; and their names were <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and <a class="sister"
# href="http://example.com/tillie" id="link3">Tillie</a>; and they lived at the bottom of a well.</p>,
# <p class="story">...</p>]
print(soup.find_all(has_class_but_no_id))
# 查找id为link2的元素
print(soup.find_all(id='link2'))  # [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
# 查找href包含elsie的元素
print(soup.find_all(href=re.compile("elsie")))  # [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
# 查找所有包含id属性的元素
# 结果： [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister"
# href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie"
# id="link3">Tillie</a>]
print(soup.find_all(id=True))
# 多条件查找元素
# 结果：
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
print(soup.find_all(href=re.compile("elsie"), id='link1'))

data_soup = BeautifulSoup('<div data-foo="value">foo!</div>', 'html.parser')
# 对于一些特殊的属性，可以通过attrs的形式查找标签
print(data_soup.find_all(attrs={"data-foo": "value"}))  # [<div data-foo="value">foo!</div>]
# 通过css类名查找元素，因为class是python的关键字，所以用class_代替、
# 结果： [<a class="sister" href="http://example.com/elsie"
# id="link1">Elsie</a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister"
# href="http://example.com/tillie" id="link3">Tillie</a>]
print(soup.find_all('a', class_='sister'))
# class_也可以用正则来过滤
print(soup.find_all(class_=re.compile("itl")))  # [<p class="title"><b>The Dormouse's story</b></p>]


def has_six_characters(css_class):
    return css_class is not None and len(css_class) == 6


# 通过自定义过滤方法过滤元素
# 结果：[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister"
# href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie"
# id="link3">Tillie</a>]
print(soup.find_all(class_=has_six_characters))
# 查找文档中的字符串为Elsie的
print(soup.find_all(text="Elsie"))  # ['Elsie']
# 正则表达式查找text
print(soup.find_all(text=re.compile("Dormouse")))  # ["The Dormouse's story", "The Dormouse's story"]
# 通过limit限制返回的结果集数量
# 结果：
# [<a class="sister" href="http://example.com/elsie" id
# ="link1">Elsie</a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
print(soup.find_all("a", limit=2))
# 默认会查找文档的所有子孙节点，如果recursive指定为False则只会查找子节点
print(soup.find_all('title', recursive=False))  # []
# 等价于 soup.find_all("a")
print(soup("a"))
# 等价于 soup.title.find_all(text=True)
print(soup.title(text=True))
# find用法与find_all用法基本一致，区别如下：
# 1、find返回找到元素的第一个元素，find_all返回所有
# 2、如果没有找到元素，find返回None，find_all返回空集合
print(soup.find("a"))  # <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

a_string = soup.find(text='Lacie')
# 找到a_string元素的父节点是a的所有元素
print(a_string.find_parents("a"))  # [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
# 找到a_string元素的父节点是p的第一个元素
# 结果：
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
# <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>
print(a_string.find_parent("p"))
# 查找a_string元素的父节点是p，class为title的所有元素
print(a_string.find_parents("p", class_="title"))  # []

first_link = soup.a
# 查找第一个a标签的所有是a的兄弟元素
# 结果： [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister"
# href="http://example.com/tillie" id="link3">Tillie</a>]
print(first_link.find_next_siblings("a"))

first_story_paragraph = soup.find("p", "story")
# 查找first_story_paragraph的下一个标签的p的兄弟标签
print(first_story_paragraph.find_next_sibling("p"))  # <p class="story">...</p>

last_link = soup.find("a", id="link3")
# 查找last_link的前一个标签是a的所有兄弟标签
# 结果： [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
print(last_link.find_previous_siblings("a"))
# 查找last_link的前一个标签是a的兄弟标签
print(last_link.find_previous_sibling("a"))  # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>

first_link = soup.a
# 查找first_link之后的所有有字符串的节点
# 结果： ['Elsie', ',\n', 'Lacie', ' and\n', 'Tillie', ';\nand they lived at the bottom of a well.', '\n', '...', '\n']
print(first_link.find_all_next(text=True))
# 查找first_link之后的第一个p标签
print(first_link.find_next("p"))  # <p class="story">...</p>
# 查找first_link之前的所有p标签
# 结果：[<p class="story">Once upon a time there were three little sisters; and their names were
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
# <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>, <p class="title"><b>The Dormouse's story</b></p>]
print(first_link.find_all_previous("p"))
# 查找first_link的前一个title元素
print(first_link.find_previous("title"))  # <title>The Dormouse's story</title>


# CSS 选择器
# 通过css选择器来查找标签为title的元素
print(soup.select("title"))  # [<title>The Dormouse's story</title>]
# 查找是p元素的第三个元素
print(soup.select("p:nth-of-type(3)"))  # [<p class="story">...</p>]
# 逐级查找body下的所有a标签
# 结果： [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister"
# href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie"
# id="link3">Tillie</a>]
print(soup.select("body a"))
# 逐级查找html下的head虾的title元素
print(soup.select("html head title"))  # [<title>The Dormouse's story</title>]
# 查找head元素下的直接子title元素
print(soup.select("head > title"))  # [<title>The Dormouse's story</title>]
# 查找p元素下子元素id为link1的元素
print(soup.select("p > #link1"))  # [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
# 查找body下的子元素为a的元素，不会逐级查找
print(soup.select("body > a"))  # []
# 查找id为link1的所有class为sister的兄弟节点
# 结果：[<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
# <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
print(soup.select("#link1 ~ .sister"))
# 通过css类型sister查找元素
# 结果：[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister"
# href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie"
# id="link3">Tillie</a>]
print(soup.select(".sister"))
# 通过id来查找元素
print(soup.select("#link1"))  # [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
# 查找所有a标签包含href属性的
# 结果：[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister"
# href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie"
# id="link3">Tillie</a>]
print(soup.select("a[href]"))
# 根据a标签的href属性值查找元素
# 结果：[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
print(soup.select('a[href="http://example.com/elsie"]'))
# 根据a标签的href前缀查找元素
# 结果：[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister"
# href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie"
# id="link3">Tillie</a>]
print(soup.select('a[href^="http://example.com"]'))
# 查找所有a标签的href值是以tillie结尾的
# 结果：[<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
print(soup.select('a[href$="tillie"]'))
# 查找所有href的值与表达式相匹配的a标签
print(soup.select('a[href*=".com/el"]'))


# 修改文档树
soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', "html.parser")
tag = soup.b
# 修改标签的name
tag.name = "blockquote"
# 修改标签的class
tag['class'] = "verybold"
# 新增标签的id属性
tag['id'] = 1
print(tag)  # <blockquote class="verybold" id="1">Extremely bold</blockquote>
# 通过.string修改标签的内容
tag.string = "New link text."
print(tag)  # <blockquote class="verybold" id="1">New link text.</blockquote>

soup = BeautifulSoup("<a>Foo</a>", "html.parser")
# 对指定标签增加内容
soup.a.append("Bar")
print(soup.a)  # <a>FooBar</a>
# 通过new_string()方法创建一个字符串对象
new_string = soup.new_string("New content")
soup.a.append(new_string)
print(soup.a)  # <a>FooBarNew content</a>
# 创建一个注释对象
new_comment = soup.new_string("I am comment.", Comment)
soup.a.append(new_comment)
print(soup.a)  # <a>FooBarNew content<!--I am comment.--></a>

soup = BeautifulSoup("<b></b>", "html.parser")
original_tag = soup.b
# 通过new_tag()方法创建一个新的标签
new_tag = soup.new_tag("a", href="http://www.example.com")
original_tag.append(new_tag)
print(original_tag)  # <b><a href="http://www.example.com"></a></b>

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, "html.parser")
tag = soup.a
# 通过insert()方法将制定内容插入对应的下标下
tag.insert(1, "but did not endorse")
print(tag)  # <a href="http://example.com/">I linked to but did not endorse<i>example.com</i></a>

soup = BeautifulSoup("<b>stop</b>", "html.parser")
tag = soup.new_tag("i")
tag.string = "Don't"
# 通过insert_before（）方法在当前tag或者文本节点前插入内容
soup.b.string.insert_before(tag)
print(soup)  # <b><i>Don't</i>stop</b>
# 通过insert_after() 方法在当前tag或文本节点后插入内容
soup.b.i.insert_after(soup.new_string(" no no "))
print(soup)  # <b><i>Don't</i> no no stop</b>

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')
tag = soup.a
# 通过clear() 方法移除当前tag的内容
tag.clear()
print(tag)  # <a href="http://example.com/"></a>

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')
a_tag = soup.a
# 通过extract() 方法将当前tag移除文档树,并作为方法结果返回
i_tag = soup.i.extract()
print(a_tag)  # <a href="http://example.com/">I linked to </a>
print(i_tag)  # <i>example.com</i>

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')
a_tag = soup.a
# 通过decompose() 方法将当前节点移除文档树并完全销毁
i_tag = soup.i.decompose()
print(a_tag)  # <a href="http://example.com/">I linked to </a>
print(i_tag)  # None

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')
a_tag = soup.a
new_tag = soup.new_tag("b")
new_tag.string = "example.net"
# 通过replace_with() 方法移除文档树中的某段内容,并用新tag或文本节点替代它
a_tag.i.replace_with(new_tag)
print(a_tag)  # <a href="http://example.com/">I linked to <b>example.net</b></a>

soup = BeautifulSoup("<p>I wish I was bold.</p>", 'html.parser')
# 通过wrap() 方法可以对指定的tag元素进行包装
soup.p.string.wrap(soup.new_tag("b"))
print(soup)  # <p><b>I wish I was bold.</b></p>

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')
a_tag = soup.a
# unwrap() 方法与 wrap() 方法相反.将移除tag内的所有tag标签,该方法常被用来进行标记的解包
a_tag.i.unwrap()
print(a_tag)  # <a href="http://example.com/">I linked to example.com</a>

markup = '<a href="http://example.com/">\nI linked to <i>example.com</i>\n</a>'
soup = BeautifulSoup(markup, 'html.parser')
# 如果只想得到tag中包含的文本内容,那么可以嗲用 get_text() 方法,这个方法获取到tag中包含的所有文版内容包括子孙tag中的内容,并将结果作为Unicode字符串返回:
print(repr(soup.get_text()))  # '\nI linked to example.com\n'
# 可以通过参数指定tag的文本内容的分隔符
print(repr(soup.get_text("|")))  # '\nI linked to |example.com|\n'
# 还可以去除获得文本内容的前后空白
print(repr(soup.get_text("|", strip=True)))  # 'I linked to|example.com'
