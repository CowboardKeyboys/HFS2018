import json

class job_listing:

	def __init__(self, sourceData):
		#self.id = sourceData
		s = json.loads(sourceData)
		self.id = s["PLATSNUMMER"]
		self.name = s["PLATSRUBRIK"]
		self.vacancies = s["ANTAL_AKT_PLATSER"]
		self.title = s["PLATSRUBRIK"]
		self.region_code = s["KOMMUN_KOD"]
		self.job_id = s["YRKE_ID"]

		
	def to_json(self):
		return json.dumps(self.__dict__)





def test():
	j = job_listing('{"PLATSNUMMER": "0017-653836", "ANTAL_AKT_PLATSER": "1"}')
	#j = job_listing("hej")
	print j.to_json()
	print "exit"
	
if __name__ == "__main__":
	test()
	