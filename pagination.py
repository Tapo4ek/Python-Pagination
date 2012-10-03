#!/usr/bin/env python

__author__      = "Tapo4ek"
__license__     = "GPL"

from math import ceil

class Pagination:
    """
    This class for pagination if iterable objects
    usage:  paginator = Pagination(some_list, entries_per_page, current_page, pageset_range, changeset_range)
    """
    def __init__(self, array=list(), entries_per_page=10, current_page=1, pageset_range=5, changeset_range=10):
        """
        array = iterable object
        entries_per_page = How many elements you want to show on the page (int)
        current_page = Your current page (int)
        pageset_range = How many pages you will see left and right from the current page (int)
        changeset_range = If you want to jump pages for example +10 or -10 (int)
        """
        self.entries_per_page = abs(entries_per_page)
        self.total_entries = len(array)
        self.last_page = ceil(self.total_entries/self.entries_per_page) # if you are using python lower then version 3.0 use: ceil(float(self.total_entries)/self.entries_per_page)
        self.changeset_range = changeset_range
        self.array = array
        self.pageset_range = abs(pageset_range)
        self.current_page = abs(current_page)
        self.first_page = 1

    def previous_page(self):
        """
        Will return previous page
        if it does not exists will return current page
        """
        if self.current_page > 1:
            return self.current_page - 1
        return self.current_page

    def next_page(self):
        """
        Will return next page
        if it does not exists will return current page
        """
        if self.current_page < self.last_page:
            return self.current_page + 1
        return self.current_page

    def pages_range(self):
        """
        Will return iterable object of all pages
        if you are using python less then 3.0 use xrange instead of range
        """
        return range(self.first_page, self.last_page+1)

    def entries_pages(self):
        """
        Will return iterable object of pages in range current page minus pageset_range
        and plus pageset_range. for example if you have 200 pages your current page is 130,
        and pageset_range is 5 your pages will be 125 126 127 128 129 130 131 132 133 134 135
        if pageset_range is 2 your pages will be 128 129 130 131 132
        this method will return iterator
        if you are using python less then 3.0 use xrange instead of range
        """
        if (self.current_page > self.pageset_range) and (self.current_page + self.pageset_range <= self.last_page):
            return range(self.current_page - self.pageset_range, self.current_page + self.pageset_range + 1)
        if (self.current_page <= self.pageset_range) and (self.current_page + self.pageset_range <= self.last_page):
            return range(self.first_page , self.current_page + self.pageset_range + 1)
        if (self.current_page > self.pageset_range) and (self.current_page + self.pageset_range > self.last_page):
            return range(self.current_page - self.pageset_range, self.last_page + 1)
        if (self.current_page <= self.pageset_range) and (self.current_page + self.pageset_range > self.last_page):
            return range(self.first_page , self.last_page + 1)

    def array_at_page(self):
        """
        I am using jinja2
        so my code looks like:
        {% for i in pager.array_at_page() %}
            <tr>
                <td>{{ i.id }}</td>
                <td>{{ i.amount }} {{ i.currency }}</td>
                <td>{{ i.status }}</td>
            </tr>
        {% endfor %}



        <form>
            <a href="{{ request.path }}?page={{ pager.first_page }}"> First page </a>
            {% if pager.first_page + pager.changeset_range <= page %}
                <a href="{{ request.path }}?page={{ pager.minus_range() }}">
                    -{{ pager.changeset_range }}
                </a>
            {% endif %}
            {% for page_number in pager.entries_pages() %}
                <a href="{{ request.path }}?page={{ page_number }}">
                    {% if page == page_number %}<span style="color: #daa520;"> {{ page_number }} </span> {% else %}{{ page_number }}{% endif  %}
                </a>
            {% endfor %}
            {% if page + pager.changeset_range <= pager.last_page %}
                <a href="{{ request.path }}?page={{ pager.plus_range() }}">
                    +{{ pager.changeset_range }}
                </a>
            {% endif %}
            <a href="{{ request.path }}?page={{ pager.last_page }}"> Last page </a>
        </form>
        <form>
            <input type="number" min="{{ pager.first_page }}" max="{{ pager.last_page }}" name="page" class="span1">
            <input type="submit" value="go">
        </form>

        """
        return self.array[self.entries_per_page * (self.current_page-1):][:self.entries_per_page]

    def plus_range(self):
        """
        Will return current page plus changeset_range
        for example: if current page is 5 and changeset_range is 10
        this function will return 15
        if page does not exists, function will return current page
        """
        if self.current_page + self.changeset_range <= self.last_page:
            return self.current_page + self.changeset_range
        return self.current_page

    def minus_range(self):
        """
        Will return current page minus changeset_range
        for example: if current page is 15 and changeset_range is 10
        this function will return 5
        if page does not exists, function will return current page
        """
        if self.current_page - self.changeset_range >= self.first_page:
            return self.current_page - self.changeset_range
        return self.current_page

    def goto_page(self, value):
        """
        This function returns page number
        if you want to go to page 13
        paginator = Pagination(some_list, entries_per_page, current_page, pageset_range, changeset_range)
        paginator.goto_page(13)
        function will return an integer
        """
        try:
            value = int(value)
        except:
            value = self.current_page
        if self.first_page <= value <= self.last_page:
            return value
        return self.current_page

