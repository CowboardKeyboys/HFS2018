import json

class Job:

	def __init__(self, sourceData):
		#self.id = sourceData
		s = json.loads(sourceData)
		self.id = s["PLATSNUMMER"]
		self.name = s["PLATSRUBRIK"]
		self.vacancies = s["ANTAL_AKT_PLATSER"]
		self.title = s["PLATSRUBRIK"]
		self.region_code = s["KOMMUN_KOD"]
		self.job_id = s["YRKE_ID"]
		self.duration = s["VARAKTIGHET"]
		self.working_hours = s["ARBETSTID"]
		self.working_operation = s["ARBETSDRIFT"]
		self.employer_name = s["AG_NAMN"]
		self.country = s["ADRESSLAND"]
		self.location = s["POSTORT"]
		self.location_desc = s["PLATSBESKRIVNING"]
		self.working_operation_desc = s["BESKR_ARBETSDRIFT"]
		self.access = s["TILLTRADE"]
		self.score = None



	def to_json(self):
		return json.dumps(self.__dict__)





def test():
	j = JobListing('{"PLATSNUMMER": "0017-653836", "ANTAL_AKT_PLATSER": "1"}')
	#j = job_listing("hej")
	print(j.to_json())
	print("exit")

if __name__ == "__main__":
	test()
