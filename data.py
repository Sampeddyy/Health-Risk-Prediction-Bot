import pandas as pd

# Categories of foods with examples specific to India
categories = {
    "Fruits": [
        "Mango", "Banana", "Guava", "Apple", "Pomegranate", "Papaya", "Chikoo", "Watermelon", "Orange", "Pineapple",
        "Grapes", "Jackfruit", "Lychee", "Custard Apple", "Strawberry", "Plum", "Peach", "Pear", "Fig", "Jamun",
        "Kiwi", "Dragon Fruit", "Mulberry", "Bael", "Ber", "Coconut", "Tamarind", "Dates", "Amla", "Starfruit",
        "Blackberry", "Raspberry", "Red Banana", "Wood Apple", "Kharbuja", "Mosambi", "Passion Fruit", "Rose Apple",
        "Cherries", "Sapota", "Pomelo", "Indian Gooseberry", "Carambola", "Phalsa", "Wild Berries", "Seetaphal",
        "Targola", "Kaith", "Ramdana Fruit", "Alubukhara", "Kokum", "Bakul Fruit", "Surinam Cherry", "Karonda",
        "Grewia", "Peepal", "Manila Tamarind", "Hog Plum", "Indian Almond", "Caper", "Bilimbi", "Monkey Jack",
        "Noni", "Langsat", "Salak", "Longan", "Breadfruit", "Buddha’s Hand", "Wild Mangosteen", "Amra", "Jungli Aam",
        "Lasoda", "Kamranga", "Chironji Fruit", "Pilu", "Banana Flower", "Mahua", "Custard Apple", "Drumstick Fruit",
        "Indian Fig", "Betel Nut", "Pili Nut", "Kewra Fruit", "Malayan Apple", "Burmese Grape", "Ceylon Olive",
        "Indian Jujube", "Indian Mulberry", "Karkati", "Water Chestnut", "Agave Fruit", "Creeping Fig", "Indian Beech",
        "Cucumber Fruit", "Neem Fruit", "Rudraksha Fruit", "Wild Olive", "Indian Bay Leaf", "Indian Capers"
    ],
    "Vegetables": [
        "Potato", "Onion", "Tomato", "Brinjal", "Carrot", "Cauliflower", "Spinach", "Cucumber", "Radish", "Pumpkin", 
        "Bitter Gourd", "Bottle Gourd", "Cabbage", "Capsicum", "Chili", "Cluster Beans", "Colocasia", "Coriander", 
        "Curry Leaves", "Drumstick", "French Beans", "Garlic", "Ginger", "Green Beans", "Green Peas", "Ivy Gourd", 
        "Knol-Khol", "Ladyfinger", "Lettuce", "Methi Leaves", "Mint Leaves", "Mushrooms", "Mustard Greens", "Okra", 
        "Parwal", "Pumpkin Flowers", "Ridge Gourd", "Snake Gourd", "Spring Onion", "Sweet Potato", "Tamarind Leaves", 
        "Turnip", "Yam", "Zucchini", "Ash Gourd", "Amaranth Leaves", "Beetroot", "Broccoli", "Celery", "Chow Chow", 
        "Cress", "Dill Leaves", "Edamame", "Elephant Foot Yam", "Fennel", "Fenugreek", "Kale", "Kohlrabi", "Leek", 
        "Lotus Stem", "Malabar Spinach", "Mint", "Nettles", "Pak Choi", "Parsley", "Radish Leaves", "Sage", "Savory", 
        "Sorrel", "Taro", "Thyme", "Water Spinach", "Wild Spinach", "Ziziphus", "Avarakkai", "Banana Stem", "Banana Flower", 
        "Betel Leaf", "Chayote", "Dondakaya", "Field Beans", "Flat Beans", "Green Chili", "Indian Broad Beans", 
        "Indian Sorrel", "Jackfruit Seeds", "Kantola", "Kovakkai", "Malabar Cucumber", "Neem Leaves", "Peerkangai", 
        "Pointed Gourd", "Pudina", "Sundakkai", "Teasel Gourd", "Tomatillo", "Urad Dal Leaves", "Velvet Bean", 
        "Winged Beans", "Wood Apple Leaves"
    ],
    "Dairy Products": [
        "Milk", "Curd", "Paneer", "Butter", "Ghee", "Cheese", "Khoa", "Chhena", "Cream", "Skimmed Milk", "Buffalo Milk",
        "Cow Milk", "Goat Milk", "Sheep Milk", "Double Cream", "Butter Milk", "Evaporated Milk", "Condensed Milk",
        "Whey Protein", "Milk Powder", "Processed Cheese", "Fresh Cream", "Clotted Cream", "Cultured Butter",
        "Unsalted Butter", "Salted Butter", "Sweetened Condensed Milk", "Yogurt", "Flavored Milk", "Organic Milk",
        "Lactose-Free Milk", "Raw Milk", "UHT Milk", "Probiotic Yogurt", "Milk Solids", "Skimmed Cream", "Hard Cheese",
        "Soft Cheese", "Semi-Hard Cheese", "Cottage Cheese", "Ricotta", "Mascarpone", "Processed Butter", "Whipping Cream",
        "Heavy Cream", "Light Cream", "Double Toned Milk", "Toned Milk", "Full Cream Milk", "Cream Cheese", "Spreadable Butter",
        "Cheddar Cheese", "Parmesan Cheese", "Mozzarella", "Camembert", "Brie", "Feta", "Swiss Cheese", "Emmental", "Blue Cheese",
        "Goat Cheese", "Quark", "Skyr", "Kefir", "Sour Cream", "Butter Fat", "Milk Fat", "Milk Cream Powder", "Butter Oil",
        "Casein", "Milk Protein", "Low-Fat Milk", "Fortified Milk", "Raw Cream", "Artisanal Cheese", "Processed Milk Products",
        "Dahi (Indian Yogurt)", "Malai", "Kulhad Milk", "Homemade Butter", "Lassi (Plain)", "Probiotic Milk", "Milk Derivatives",
        "Curd Cheese", "Natural Butter", "Sweetened Cream", "Full-Fat Yogurt", "Milk Ice", "Unprocessed Cream", "Natural Paneer"
    ],
    "Grains": [
        "Rice", "Wheat", "Barley", "Maize (Corn)", "Ragi (Finger Millet)", "Bajra (Pearl Millet)", "Jowar (Sorghum)", 
        "Foxtail Millet (Kangni)", "Kodo Millet (Kodra)", "Barnyard Millet (Sanwa)", "Proso Millet (Chena)", "Little Millet (Kutki)", 
        "Amaranth (Rajgira)", "Buckwheat (Kuttu)", "Quinoa", "Teff", "Oats", "Rye", "Durum Wheat", "Emmer Wheat (Khapli Gehu)", 
        "Wild Rice", "Basmati Rice", "Red Rice", "Black Rice (Chak Hao)", "Brown Rice", "Sticky Rice (Glutinous Rice)", 
        "Sona Masoori Rice", "Parboiled Rice", "Idli Rice", "Ponni Rice", "Jasmine Rice", "Japonica Rice", "Arborio Rice", 
        "Flattened Rice (Poha)", "Puffed Rice (Murmura)", "Broken Rice", "Polished Rice", "Unpolished Rice", "Husked Rice", 
        "Semi-Husked Rice", "Parched Rice", "Sprouted Grains (Mixed)", "Barley Flour", "Wheat Flour (Atta)", "Refined Wheat Flour (Maida)", 
        "Semolina (Sooji or Rava)", "Gram Flour (Besan)", "Rice Flour", "Cornmeal (Makkai Atta)", "Millet Flour (Mixed)", "Jowar Flour", 
        "Bajra Flour", "Ragi Flour", "Amaranth Flour", "Kodo Millet Flour", "Foxtail Millet Flour", "Barnyard Millet Flour", 
        "Little Millet Flour", "Buckwheat Flour (Kuttu Atta)", "Quinoa Flour", "Oats Flour", "Sprouted Wheat Flour", 
        "Multi-Grain Flour", "Germinated Barley", "Malted Barley", "Whole Wheat", "Cracked Wheat (Dalia)", "Bulgur Wheat", 
        "Couscous", "Freekeh", "Rice Bran", "Wheat Bran", "Corn Bran", "Barley Bran", "Rye Bran", "Red Sorghum (Lal Jowar)", 
        "White Sorghum", "Hulled Barley", "Pearl Barley", "Hulled Oats", "Steel-Cut Oats", "Rolled Oats", "Instant Oats", 
        "Whole Corn", "Sweet Corn Kernels", "Corn Grits", "Popcorn Kernels", "Corn Starch", "Tapioca Pearls (Sabudana)", 
        "Tapioca Starch", "Moth Beans (For Sprouting)", "Sprouted Millets", "Millet Groats", "Barley Groats", "Quinoa Groats", 
        "Sorghum Groats", "Millet Husk", "Rice Husk", "Corn Husk", "Job’s Tears (Adlay Millet)"
    ],
    "Proteins (Meat, Fish, Eggs, Legumes, Nuts)": [
         "Chickpeas (Kabuli Chana)", "Black Chickpeas (Kala Chana)", "Red Lentils (Masoor Dal)", "Yellow Lentils (Moong Dal)", 
        "Green Gram (Whole Moong)", "Pigeon Peas (Toor Dal/Arhar Dal)", "Split Urad Dal (Black Gram Dal)", "Whole Urad Dal", 
        "Horse Gram (Kulthi)", "Moth Beans", "Field Beans (Val Dal)", "Kidney Beans (Rajma)", "Black-Eyed Peas (Lobia)", 
        "Broad Beans", "Bengal Gram (Chana Dal)", "Lentils (Sabut Masoor)", "Matki Dal", "Cowpeas", "Peas (Hara Matar)", 
        "Masoor Whole (Brown Lentils)", "Almonds", "Cashews", "Walnuts", "Pistachios", "Peanuts", "Pine Nuts (Chilgoza)", 
        "Hazelnuts", "Brazil Nuts", "Pumpkin Seeds", "Sunflower Seeds", "Chia Seeds", "Flax Seeds (Alsi)", "Sesame Seeds (Til)", 
        "Hemp Seeds", "Basil Seeds (Sabja)", "Watermelon Seeds", "Cucumber Seeds", "Poppy Seeds (Khus Khus)", "Melon Seeds", 
        "Whey Protein (Powdered or Natural)", "Chicken Eggs", "Duck Eggs", "Quail Eggs", "Chicken", "Mutton (Goat Meat)", 
        "Lamb", "Pork", "Beef (in select regions)", "Buffalo Meat", "Duck Meat", "Turkey", "Rohu (Carp)", "Catla (Indian Carp)", 
        "Hilsa", "Pomfret", "Mackerel (Bangda)", "Sardines (Mathi)", "Tuna", "Kingfish (Surmai)", "Prawns", "Shrimp", "Crab", 
        "Lobster", "Squid", "Octopus", "Anchovies", "Basa", "Salmon (in select markets)", "Tilapia", "Soybeans", "Tofu", 
        "Tempeh", "Soy Milk", "Soy Chunks", "Textured Vegetable Protein (TVP)", "Edamame", "Moringa Leaves", "Drumstick Leaves", 
        "Curry Leaves", "Spinach", "Amaranth Leaves", "Kale", "Mustard Greens", "Fenugreek Leaves (Methi)", "Beet Greens", 
        "Spirulina (Algae-based protein)", "Mushroom (Button, Shiitake, Oyster, etc.)", "Lotus Seeds (Makhana)", "Bamboo Shoots", 
        "Quinoa", "Buckwheat (Kuttu)", "Amaranth (Rajgira)", "Sacha Inchi Seeds", "Sunflower Seed Butter", "Peanut Butter", 
        "Chia Seed Pudding", "Black Sesame", "Hemp Protein Powder", "Alfalfa Sprouts", "Tempeh (Soy Fermented Product)",
    ],
    
    "Fats and Oils":[
    "Mustard Oil", "Groundnut Oil", "Coconut Oil", "Sunflower Oil", "Ghee", "Butter", "Olive Oil", "Sesame Oil", 
    "Palm Oil", "Soybean Oil", "Rice Bran Oil", "Cottonseed Oil", "Safflower Oil", "Avocado Oil", "Canola Oil", 
    "Walnut Oil", "Almond Oil", "Flaxseed Oil", "Hemp Oil", "Neem Oil", "Mango Kernel Oil", "Bitter Almond Oil", 
    "Chili Oil", "Curry Leaf Oil", "Carrot Seed Oil", "Pine Nut Oil", "Peanut Oil", "Jojoba Oil", "Sunflower Seed Oil", 
    "Cucumber Seed Oil", "Pumpkin Seed Oil", "Castor Oil", "Tamarind Seed Oil", "Grapeseed Oil", "Apricot Kernel Oil", 
    "Poppy Seed Oil", "Turmeric Oil", "Ginger Oil", "Clove Oil", "Cinnamon Oil", "Garlic Oil", "Coconut Milk", 
    "Ghee Clarified Butter", "Mustard Seed Oil", "Corn Oil", "Moringa Oil", "Melon Seed Oil", "Mango Oil", "Papaya Seed Oil", 
    "Chia Seed Oil", "Black Cumin Seed Oil", "Sacha Inchi Oil", "Watermelon Seed Oil", "Rosemary Oil", "Lavender Oil", 
    "Sweet Almond Oil", "Cabbage Seed Oil", "Black Seed Oil", "Moringa Seed Oil", "Peach Kernel Oil", "Tomato Seed Oil", 
    "Blackberry Seed Oil", "Olive Pomace Oil", "Rapeseed Oil", "Baobab Oil", "Camelina Oil", "Pistachio Oil", "Grapefruit Seed Oil", 
    "Walnut Seed Oil", "Macadamia Nut Oil", "Sacha Inchi Oil", "Rice Bran Oil", "Cardamom Oil", "Bay Leaf Oil", "Avocado Butter", 
    "Cocoa Butter", "Shea Butter", "Cupuacu Butter", "Coconut Butter", "Mango Butter", "Pumpkin Seed Butter", 
    "Hemp Butter", "Peach Butter", "Tung Oil", "Neem Seed Oil", "Ajwain Oil", "Caraway Oil", "Curry Leaf Essential Oil", 
    "Fennel Seed Oil", "Rosemary Seed Oil", "Sesame Butter", "Honey Oil", "Kalonji Seed Oil", "Basil Seed Oil", "Grapefruit Oil", 
    "Nutritional Yeast Oil", "Tea Tree Oil", "Raspberry Seed Oil", "Jojoba Seed Oil", "Lemongrass Oil", "Carrot Seed Oil", 
    "Basil Oil", "Cilantro Oil", "Parsley Seed Oil", "Peppermint Oil", "Tarragon Oil", "Lemon Oil", "Pineapple Seed Oil", 
    "Paprika Seed Oil", "Litchi Seed Oil", "Cocoa Oil", "Jasmine Oil", "Nectarine Oil"
    ] ,
    "Sweets and Sugars": [
        "Jaggery", "Sugar", "Honey", "Khand", "Palm Sugar", "Mishri", "Barfi", "Laddu", "Halwa", "Gulab Jamun", 
    "Rasgulla", "Gajar Halwa", "Jalebi", "Kheer", "Peda", "Chikki", "Kulfi", "Samosa (Sweet)", "Sandesh", "Lassi",
    "Puran Poli", "Shakarpara", "Gulab Penda", "Motichoor Laddu", "Coconut Burfi", "Chocolate Burfi", "Mysore Pak",
    "Anarsa", "Kaju Katli", "Coconut Ladoo", "Besan Ladoo", "Gulab Jamun with Rabri", "Rava Kesari", "Suji Halwa", 
    "Pineapple Raita", "Fruit Chaat", "Kesar Pista Ladoo", "Bengali Sweets", "Rava Laddu", "Patishapta", "Mishti Doi", 
    "Sivayian", "Khaja", "Milk Cake", "Chumchum", "Badam Halwa", "Sooji Ka Halwa", "Moong Dal Halwa", "Rawa Laddu", 
    "Kokum Sherbet", "Khoya", "Milk Peda", "Carrot Barfi", "Apple Kheer", "Jangri", "Agarbathi", "Rava Khoya Ladoo", 
    "Khatta Meetha", "Jaggery Candy", "Fudge", "Feni", "Petha", "Fruit Chutney", "Papad", "Sakkarai Pongal", 
    "Kalaruchi", "Patra", "Bhapa Doi", "Mithai Pulao", "Khoya Burfi", "Pineapple Barfi", "Cashew Ladoo", "Lassi Kulfi", 
    "Saffron Rice Pudding", "Tiramis", "Shrikhand", "Mango Sandesh", "Rava Pudding", "Sweets with Kesar", "Ragi Ladoo", 
    "Rajbhog", "Srikhand Peda", "Bengal Rasgulla", "Banana Halwa", "Cashew Nuts Halwa", "Jalebi Rabri", "Mawa Ladoo", 
    "Tiranga Ladoo", "Bajra Ladoo", "Cardamom Cake", "Fruit Cake", "Wheat Halwa", "Mango Peda", "Chumchum Peda", 
    "Khajur Kheer", "Baked Sandesh", "Doodh Peda", "Aloo Halwa", "Chana Laddu", "Chivda", "Baked Burfi", 
    "Tamarind Chutney", "Kesar Lassi", "Cheese Peda", "Aloo Tikki Halwa", "Rawa Rasgulla", "Kundru (Sweet)", 
    "Chana Sweets", "Pistachio Barfi", "Chana Chaat", "Coconut Kheer", "Gond Ladoo", "Corn Flour Pudding"
    ],
    "Spices and Condiments": [
        "Turmeric", "Cumin", "Coriander", "Mustard Seeds", "Fenugreek", "Fennel", "Cloves", "Cardamom", "Black Pepper", 
    "Red Chili", "Cinnamon", "Bay Leaves", "Asafoetida (Hing)", "Nutmeg", "Mace", "Ginger", "Garlic", "Kalonji", 
    "Tamarind", "Saffron", "Star Anise", "Kasuri Methi", "Dry Mango Powder (Amchur)", "Curry Leaves", "Curry Powder", 
    "Garam Masala", "Chaat Masala", "Sambar Powder", "Rasam Powder", "Chili Powder", "Turmeric Powder", "Jaggery Powder", 
    "Fennel Seeds", "Mustard Powder", "Cumin Powder", "Coriander Powder", "Clove Powder", "Cardamom Powder", "Cinnamon Powder", 
    "Garlic Powder", "Ginger Powder", "Onion Powder", "Tandoori Masala", "Chili Flakes", "Chili Sauce", "Black Salt", 
    "Hing Powder", "Curry Paste", "Mustard Paste", "Pepper Powder", "Vinegar", "Sweet Chili Sauce", "Soya Sauce", 
    "Tamarind Paste", "Green Chili Paste", "Poppy Seeds", "Sesame Seeds", "White Pepper", "All Spice", "Chili Oil", 
    "Coconut Powder", "Aniseed", "Chili Powder (Kashmiri)", "Cinnamon Stick", "Cloves (Whole)", "Green Cardamom", 
    "Black Cardamom", "Rock Salt", "Raw Mango Powder", "Chili Ginger Sauce", "Salt", "Sea Salt", "Dry Ginger", "Coriander Leaves", 
    "Mint Leaves", "Parsley", "Curry Paste", "Hing", "Kesar (Saffron)", "Szechuan Pepper", "Rose Water", "Ginger Juice", 
    "Lemon Grass", "Ginger Garlic Paste", "Peanut Butter", "Ajwain", "Mustard Oil", "Garlic Oil", "Curry Powder", 
    "Kala Jeera", "Chili Butter", "Mango Pickle", "Garlic Pickle", "Lemon Pickle", "Amla Powder", "Red Chilli Sauce", 
    "Mustard Oil", "Mint Sauce", "Kalonji Seeds", "Curry Sauce", "Paprika", "Rose Petal Jam", "Garlic Chutney", 
    "Mint Chutney", "Tomato Chutney", "Tamarind Chutney", "Mango Chutney", "Green Chili Chutney", "Onion Chutney", 
    "Coconut Chutney", "Lemon Chutney", "Pineapple Chutney", "Date Chut",
    ]
}

# Ensure each category has 100 items
for category in categories:
    categories[category] = (categories[category] * (100 // len(categories[category]) + 1))[:100]

# Create a DataFrame
data = {category: items for category, items in categories.items()}
df = pd.DataFrame.from_dict(data, orient='index').transpose()

# Save to Excel
file_name = "Indian_Food_Categories.xlsx"
df.to_excel(file_name, index=False)

print(f"Excel file '{file_name}' has been created successfully in the current directory.")

