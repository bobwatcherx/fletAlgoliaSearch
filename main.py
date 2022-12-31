from flet import *
from algoliasearch.search_client import SearchClient
myAppId = "08OHMDKV8Y"
myKEYID = "e98de167199968c82c9cd047ad448deb"

client = SearchClient.create(myAppId,myKEYID)
index = client.init_index("YouFUck")


mydata = [
{"objectID":1,"name":"dogs"},
{"objectID":2,"name":"bear"},
{"objectID":3,"name":"tiger"},
{"objectID":4,"name":"penguin"},
{"objectID":5,"name":"koala"},
{"objectID":6,"name":"digymon"},

]

# PUSH MYDATA TO ALGOLIA
index.save_objects(mydata)

class Myclass(UserControl):
	def __init__(self):
		super().__init__()
		# IF NOT FOUND SEARCH 
		self.isEmpty = Text("YOU EMPTY SEARCH....",size=30)
		self.mysearch = TextField(label="Search",
			on_change=self.searchChange
			)
		self.data = Column()
		# PUSH MYDATA TO COLUMN
		for x in mydata:
			self.data.controls.append(
			Column([
				Text(x['name'],size=20)
				])
			)
		# SET DEFAULT EMPTY IS FALSE
		self.isEmpty.visible = False


	def build(self):
		return Column([
		self.mysearch,
		self.data,
		self.isEmpty

			])
	# SEARCH  INPUT PROSES
	def searchChange(self,e):
		# IF YOU TEXTINPUT IS ""
		if e.control.value == "":
			self.data.controls.clear()
			# PUSH MYDATA TO COLUMN
			for x in mydata:
				self.data.controls.append(
					Column([
				Text(x['name'],size=20)
				])
			)
			print("YOU INPUT IS BLANK GUYS...")
		objects = index.search(self.mysearch.value)
		# IF NOT FOUND SEARCH
		if not objects['hits']:
			self.data.visible = False
			self.isEmpty.visible = True
			self.update()
			print("YOU EMPTY GUYS....")
		else:
			self.data.visible = True
			self.isEmpty.visible = False
			self.youRenderIFFound(objects)
			self.update()

	def youRenderIFFound(self,x):
		self.data.controls.clear()
		# IF DATA  FOUND QUERY OR QUERY IS ""
		if not x['query'] == "":
			print("no result here guys..")
			for r in x['hits']:
				self.data.controls.append(
					Column([
				Text(r['name'],size=20)
				])
			)
				self.update()
		# IF NOT FOUND
		if x['query'] == "":
			for r in mydata:
				self.data.controls.append(
					Column([
				Text(r['name'],size=20)
				])
			)
				self.update()




def main(page:Page):
	page.update()
	myclass = Myclass()
	page.add(myclass)

flet.app(target=main)
