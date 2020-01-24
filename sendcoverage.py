from xml.dom import minidom
root = minidom.parse('coverage.xml')
value = root.getElementsByTagName('coverage')[0].attributes['line-rate'].value
print(round(float(value) * 100))
