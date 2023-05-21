class Bird:
    def __init__(self, bird_ru="", bird_en="", desc_en="", desc_ru="", place_ru="", place_en="", size_ru="", size_en=""):
        self.bird_ru = "Название:" + str(bird_ru)
        self.bird_en = "Name:" + str(bird_en)
        self.desc_en = "Description:" + str(desc_en)
        self.desc_ru = "Общая информация:" + str(desc_ru)
        self.place_ru = "Среда обитания:" + str(place_ru)
        self.place_en = "Habitat:" + str(place_en)
        self.size_ru = "Внешний вид:" + str(size_ru)
        self.size_en = "Appearence:" + str(size_en)

    def getRusssian(self):
        return (self.bird_ru, self.desc_ru, self.place_ru, self.size_ru, self.bird_en)
    
    def getEnglish(self):
        return (self.bird_en, self.desc_en, self.place_en, self.size_en, self.bird_en)
