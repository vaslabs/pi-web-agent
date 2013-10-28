# HTML.py tutorial - P. Lagadec

# see also http://www.decalage.info/en/python/html for more details and
# updates.


import HTML

# open an HTML file to show output in a browser
HTMLFILE = 'HTML_tutorial_output.html'
f = open(HTMLFILE, 'w')


#=== TABLES ===================================================================

# 1) a simple HTML table may be built from a list of lists:

table_data = [
        ['Last name',   'First name',   'Age'],
        ['Smith',       'John',         30],
        ['Carpenter',   'Jack',         47],
        ['Johnson',     'Paul',         62],
    ]

htmlcode = HTML.table(table_data)
print htmlcode
f.write(htmlcode)
f.write('<p>')
print '-'*79

#-------------------------------------------------------------------------------

# 2) a header row may be specified: it will appear in bold in browsers

table_data = [
        ['Smith',       'John',         30],
        ['Carpenter',   'Jack',         47],
        ['Johnson',     'Paul',         62],
    ]

htmlcode = HTML.table(table_data,
    header_row=['Last name',   'First name',   'Age'])
print htmlcode
f.write(htmlcode)
f.write('<p>')
print '-'*79


#-------------------------------------------------------------------------------

# 3) you may also create a Table object and add rows one by one:

t = HTML.Table(header_row=['x', 'square(x)', 'cube(x)'])
for x in range(1,10):
    t.rows.append([x, x*x, x*x*x])
htmlcode = str(t)
print htmlcode
f.write(htmlcode)
f.write('<p>')
print '-'*79


#-------------------------------------------------------------------------------

# 4) rows may be any iterable (list, tuple, ...) including a generator:
#    (this is useful to save memory when generating a large table)

def gen_rows(i):
    'rows generator'
    for x in range(1,i):
        yield [x, x*x, x*x*x]

htmlcode = HTML.table(gen_rows(10), header_row=['x', 'square(x)', 'cube(x)'])
print htmlcode
f.write(htmlcode)
f.write('<p>')
print '-'*79


#-------------------------------------------------------------------------------

# 5) to choose a specific background color for a cell, use a TableCell
#    object:

HTML_COLORS = ['Black', 'Green', 'Silver', 'Lime', 'Gray', 'Olive', 'White',
    'Maroon', 'Navy', 'Red', 'Blue', 'Purple', 'Teal', 'Fuchsia', 'Aqua']

t = HTML.Table(header_row=['Name', 'Color'])
for colorname in HTML_COLORS:
    colored_cell = HTML.TableCell(' ', bgcolor=colorname)
    t.rows.append([colorname, colored_cell])
htmlcode = str(t)
print htmlcode
f.write(htmlcode)
f.write('<p>')
print '-'*79


#-------------------------------------------------------------------------------

# 6) A simple way to generate a test report:

# dictionary of test results, indexed by test id:
test_results = {
        'test 1': 'success',
        'test 2': 'failure',
        'test 3': 'success',
        'test 4': 'error',
    }

# dict of colors for each result:
result_colors = {
        'success':      'lime',
        'failure':      'red',
        'error':        'yellow',
    }

t = HTML.Table(header_row=['Test', 'Result'])
for test_id in sorted(test_results):
    # create the colored cell:
    color = result_colors[test_results[test_id]]
    colored_result = HTML.TableCell(test_results[test_id], bgcolor=color)
    # append the row with two cells:
    t.rows.append([test_id, colored_result])
htmlcode = str(t)
print htmlcode
f.write(htmlcode)
f.write('<p>')
print '-'*79

#-------------------------------------------------------------------------------

# 7) sample table with column attributes and styles:
table_data = [
        ['Smith',       'John',         30,    4.5],
        ['Carpenter',   'Jack',         47,    7],
        ['Johnson',     'Paul',         62,    10.55],
    ]
htmlcode = HTML.table(table_data,
    header_row = ['Last name',   'First name',   'Age', 'Score'],
    col_width=['', '20%', '10%', '10%'],
    col_align=['left', 'center', 'right', 'char'],
    col_styles=['font-size: large', '', 'font-size: small', 'background-color:yellow'])
f.write(htmlcode + '<p>\n')
print htmlcode
print '-'*79



#=== LISTS ===================================================================

# 1) a HTML list (with bullets) may be built from a Python list of strings:

a_list = ['john', 'paul', 'jack']
htmlcode = HTML.list(a_list)
print htmlcode
f.write(htmlcode)
f.write('<p>')
print '-'*79


# 2) it is easy to change it into a numbered (ordered) list:

htmlcode = HTML.list(a_list, ordered=True)
print htmlcode
f.write(htmlcode)
f.write('<p>')
print '-'*79


# 3) Lines of a list may also be added one by one, when using the List class:

html_list = HTML.List()
for i in range(1,10):
    html_list.lines.append('square(%d) = %d' % (i, i*i))
htmlcode = str(html_list)
print htmlcode
f.write(htmlcode)
f.write('<p>')
print '-'*79


# 4) To save memory, a large list may be built from a generator:

def gen_lines(i):
    'lines generator'
    for x in range(1,i):
        yield 'square(%d) = %d' % (x, x*x)
htmlcode = HTML.list(gen_lines(10))
print htmlcode
f.write(htmlcode)
f.write('<p>')
print '-'*79


#=== LINKS ===================================================================

# How to create a link:

htmlcode = HTML.link('Decalage website', 'http://www.decalage.info')
print htmlcode
f.write(htmlcode)
f.write('<p>')
print '-'*79


f.close()
print '\nOpen the file %s in a browser to see the result.' % HTMLFILE
