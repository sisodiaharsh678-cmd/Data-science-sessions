class sample:
    like = 0 
    score = 10 

    @staticmethod
    def addcount(self , count):
        self.score = self.score + count
        print(self.score)

obj1 = sample()
obj1.like += 1 
print(obj1.like)   

obj1.like += 1 
print(obj1.like) 
print("--------")

obj2 = sample()
obj2.like += 1 
print(obj2.like) 

sample.addcount(sample , 10 )
sample.addcount(sample,80)


    
        