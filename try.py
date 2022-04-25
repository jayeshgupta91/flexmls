l = ['Beds/Baths: 5.2 / 3.5', 'Bedrooms Plus: 7', 'Approx SqFt: 2,702 / County Assessor', 'Price/SqFt: $212.81', 'Year Built: 2014', 'Pool: Private Only', 'Encoded Features: 53.5RDPO2G2S', 'Exterior Stories: 2', '# of Interior Levels: 2', 'Dwelling Type: Single Family - Detached', 'Dwelling Styles: Detached']


sqft = l[2]
print(sqft.find(":"))

sqft = sqft[sqft.find(":")+1:sqft.find("/")]
print(sqft)

s = l[0].rfind("/")
bedsBaths = l[0]
print(bedsBaths[bedsBaths.find(":")+2:s])
print(bedsBaths[s+2:])


