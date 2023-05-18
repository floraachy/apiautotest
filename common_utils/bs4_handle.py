# -*- coding: utf-8 -*-
# @Time    : 2023/5/10 14:11
# @Author  : chenyinhua
# @File    : bs4_handle.py
# @Software: PyCharm
# @Desc: bs4（BeautifulSoup4）是Python中的第三方库。可以从HTML或XML文件中提取数据的Python库。


from bs4 import BeautifulSoup  # pip install beautifulsoup4


class SoupAPI:
    def __init__(self, html_file):
        self.html_file = html_file
        self.soup = self.get_soup()

    def get_soup(self):
        with open(self.html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        return soup

    def get_element_text(self, element):
        """
        获取元素的文本内容
        *************************
        在使用 BeautifulSoup 库解析 HTML 文件时，element.text 和 element.get_text() 都可以用来获取元素的文本内容。它们的区别在于：
            element.text 返回的是元素及其子元素的文本内容，但是会将所有的换行符转换为空格。换言之，它可以将文本内容整合成一段连续的字符串，并去掉其中的换行符。
            element.get_text() 返回的也是元素及其子元素的文本内容，但是可以通过指定分隔符来保留换行符或者其他字符。
            如果不指定分隔符，默认情况下会将所有的空白字符（包括换行符、制表符等）都替换成一个空格。
        因此，如果你想保留换行符并且不需要在文本内容中保留其他空白字符，可以使用element.get_text('\n') 来指定换行符为分隔符。如果你只是想将文本内容整合为一行字符串，可以使用 element.text。
        *************************
        """
        return element.get_text()

    def get_element_by_id(self, element_id):
        """
        获取指定ID的元素
        """
        element = self.soup.find(id=element_id)
        return element

    def get_elements_by_class(self, class_name):
        """
        获取指定Class的所有元素
        """
        elements = self.soup.find_all(class_=class_name)
        return elements

    def get_elements_by_tag(self, tag_name):
        """
        获取指定标签的所有元素
        例如：self.soup.find_all('p')， 获取所有的p标签
        """
        elements = self.soup.find_all(tag_name)
        return elements

    def select_element(self, selector):
        """
        使用select筛选（select使用CSS选择规则）
        soup.select(‘标签名'),代表根据标签来筛选出指定标签。
        soup.select(‘[属性名="属性值"]'),代表根据指定属性进行筛选；
        CSS中#xxx代表筛选id，soup.select(‘#xxx')代表根据id筛选出指定标签,返回值是一个列表。
        CSS中.###代表筛选class，soup.select('.xxx')代表根据class筛选出指定标签,返回值是一个列表。
        嵌套select: soup.select(“#xxx .xxxx”)，如(“#id2 .news”)就是id=”id2”标签下class=”news的标签，返回值是一个列表。
        """
        return self.soup.select(selector)

    def get_elements_by_attr(self, attr_name, attr_value=True):
        """
        通过属性获取标签
        如果是查找具体某个属性名称=属性值的标签，可以通过attr_name和attr_value来指定；
        如果仅想查找具备某个属性名称的标签，而不关心属性值是什么，就可以使用 True 来表示属性存在
        """
        return self.soup.find_all(attrs={f'{attr_name}': attr_value})

    def get_element_parent(self, element):
        """
        查找指定元素的父元素；
        """
        return element.parent

    def get_element_parents(self, element):
        """
        查找指定元素的所有祖先元素；
        """
        return element.parents

    def get_element_next_sibling(self, element):
        """
        查找指定元素的下一个兄弟元素；
        """
        return element.next_sibling

    def get_element_next_siblings(self, element):
        """
        查找指定元素的下一个所有的兄弟元素；
        """
        return element.next_siblings

    def get_element_previous_sibling(self, element):
        """
        查找指定元素的上一个兄弟元素；
        """
        return element.previous_sibling

    def get_element_previous_siblings(self, element):
        """
        查找指定元素的上一个所有兄弟元素；
        """
        return element.previous_siblings

    def get_element_children(self, element):
        """
        查找指定元素的所有子元素；
        """
        return element.children

    def get_element_descendants(self, element):
        """
        查找指定元素的所有子孙元素。
        """
        return element.descendants
