import pickle

class Company(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

# with open('company_data.pkl', 'wb') as outp:
#     company1 = Company('banana', 40)
#     pickle.dump(company1, outp, pickle.HIGHEST_PROTOCOL)

#     company2 = Company('spam', 42)
#     pickle.dump(company2, outp, pickle.HIGHEST_PROTOCOL)

# del company1
# del company2

with open('company_data.pkl', 'rb') as inp:
    print("Here I am")
    company1 = pickle.load(inp)
    print(company1.name)  # -> banana
    print(company1.value)  # -> 40

    company2 = pickle.load(inp)
    print(company2.name) # -> spam
    print(company2.value)  # -> 42