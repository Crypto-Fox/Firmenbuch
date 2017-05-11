from pattern.graph import Graph
import webbrowser

g = Graph()
n1 = "asdasd"
n2 = "two"
n3 = "three"
n4 = "four"
n5 = "five"

g.add_node(n1)
g.add_node(n2)
g.add_node(n3)
g.add_node(n4)
g.add_node(n5)

g.add_edge(n2, n3)
g.add_edge(n3, n4)
g.add_edge(n4, n5)


"""for n1, n2 in (
   ('cat', 'tail'), ('cat', 'purr'), ('purr', 'sound'),
   ('dog', 'tail'), ('dog', 'bark'), ('bark', 'sound')):
     g.add_node(n1)
     g.add_node(n2)
     g.add_edge(n1, n2, weight=0.0, type='is-related-to')"""

g.export('sound')

webbrowser.open(u"file:///Users/tobiasfuma/Desktop/FirmenbuchCrawler/sound/index.html")
