"""Catalogue seed data.

Row format:  name|height_cm|weight|lifespan_years|tags
Weight unit depends on the category (see UNITS). Tags are single letters
(see TAG_LABELS). All figures are typical ranges for demo purposes.
"""

CATEGORIES = [
    ("Dogs", "dog", "\U0001F415"),
    ("Cats", "cat", "\U0001F408"),
    ("Rabbits", "rabbit", "\U0001F407"),
    ("Guinea pigs", "guinea-pig", "\U0001F439"),
    ("Hamsters", "hamster", "\U0001F439"),
    ("Birds", "bird", "\U0001F426"),
    ("Fish", "fish", "\U0001F41F"),
    ("Tortoises", "tortoise", "\U0001F422"),
    ("Pet rats", "pet-rat", "\U0001F400"),
    ("Chinchillas", "chinchilla", "\U0001F42D"),
]

TAG_LABELS = {
    "g": "Guard dog",
    "m": "Military & police work",
    "s": "Search & rescue",
    "v": "Service & therapy",
    "h": "Herding",
    "f": "Family pet",
    "a": "Apartment living",
    "b": "First-time owners",
    "u": "Hunting & retrieving",
    "c": "Hot-climate friendly",
    "x": "Talks & mimics",
    "e": "Experienced keepers",
    "k": "Community tank",
}

TRAITS = {
    "g": "protective and alert",
    "m": "highly trainable and driven",
    "s": "strong scenting or rescue ability",
    "v": "calm and gentle with people",
    "h": "intelligent and energetic",
    "f": "affectionate with family",
    "b": "easy to handle",
    "u": "energetic and eager to work",
    "x": "social and able to mimic sounds",
    "k": "peaceful with tankmates",
}

SINGULAR = {
    "Dogs": "dog", "Cats": "cat", "Rabbits": "rabbit",
    "Guinea pigs": "guinea pig", "Hamsters": "hamster", "Birds": "bird",
    "Fish": "fish", "Tortoises": "tortoise", "Pet rats": "pet rat",
    "Chinchillas": "chinchilla",
}

UNITS = {  # (height unit, weight unit)
    "Dogs": ("cm", "kg"), "Cats": ("cm", "kg"), "Rabbits": ("cm", "kg"),
    "Guinea pigs": ("cm", "g"), "Hamsters": ("cm", "g"), "Birds": ("cm", "g"),
    "Fish": ("cm", ""), "Tortoises": ("cm", "kg"), "Pet rats": ("cm", "g"),
    "Chinchillas": ("cm", "g"),
}

HEIGHT_SUFFIX = {
    "Dogs": " at shoulder", "Cats": " at shoulder", "Rabbits": " body length",
    "Guinea pigs": " body length", "Hamsters": " body length", "Birds": " long",
    "Fish": " long", "Tortoises": " shell length", "Pet rats": " body length",
    "Chinchillas": " body length",
}

ADULT_AGE = {
    "Dogs": {"Small": "10-12 months", "Medium": "12-18 months",
             "Large": "18-24 months", "Giant": "24-36 months"},
    "Cats": {"Small": "12 months", "Medium": "12-18 months", "Large": "2-4 years"},
    "Rabbits": {"Small": "6-8 months", "Medium": "8-10 months", "Large": "12-18 months"},
    "Guinea pigs": "4-6 months",
    "Hamsters": "2-3 months",
    "Birds": {"Small": "6-12 months", "Medium": "1-3 years", "Large": "3-5 years"},
    "Fish": {"Small": "3-6 months", "Medium": "6-12 months", "Large": "1-3 years"},
    "Tortoises": "Many years (slow growth)",
    "Pet rats": "5-6 months",
    "Chinchillas": "8-12 months",
}

INDIAN_PROTECTED = {
    "Indian Star Tortoise", "Elongated Tortoise", "Burmese Star Tortoise",
    "Indian Ringneck Parakeet", "Alexandrine Parakeet", "Plum-headed Parakeet",
}
EXOTIC_BIRD_WORDS = ("Macaw", "Cockatoo", "Amazon", "Grey", "Eclectus")

CARE = {
    "Dogs": {
        "purpose": "Companion; working roles vary by breed",
        "activity_level": "Varies by breed; daily exercise required",
        "diet": "Complete, balanced dog food appropriate to age and health; provide fresh water.",
        "grooming": "Brush according to coat type; check ears, nails, skin and teeth.",
        "exercise_needs": "Daily walks, play, training and mental enrichment.",
        "housing_needs": "Safe accommodation, comfortable resting space and protection from extreme weather.",
        "social_needs": "Positive human interaction, reward-based training and gradual socialisation.",
        "care_needs": "Preventive veterinary care, vaccinations as advised and parasite prevention.",
        "care_difficulty": "Varies by breed and individual",
        "health_considerations": "Health risks vary by breed; discuss screening with a veterinarian.",
        "enrichment": "Sniffing walks, food puzzles, training, play and suitable chew toys.",
    },
    "Cats": {
        "purpose": "Companion",
        "activity_level": "Daily play, climbing and exploration",
        "diet": "Complete cat food appropriate to life stage; provide fresh water.",
        "grooming": "Brush according to coat length; check nails, ears and teeth.",
        "exercise_needs": "Interactive play and safe opportunities to climb and chase toys.",
        "housing_needs": "Safe environment, hiding places, scratching surfaces and clean litter trays.",
        "social_needs": "Respect individual preferences for contact and personal space.",
        "care_needs": "Routine veterinary examinations and preventive care.",
        "care_difficulty": "Moderate; coat and health needs vary",
        "health_considerations": "Health risks vary by breed and individual.",
        "enrichment": "Interactive toys, food puzzles, scratching posts and climbing structures.",
    },
    "Rabbits": {
        "purpose": "Companion",
        "activity_level": "Daily exercise and exploration",
        "diet": "Unlimited suitable grass hay, fresh water, leafy greens and appropriate pellets.",
        "grooming": "Brush regularly, especially during shedding.",
        "exercise_needs": "Daily access to a large, secure exercise area.",
        "housing_needs": "Spacious housing with hides, solid flooring and room to hop.",
        "social_needs": "Compatible rabbit companionship is often beneficial.",
        "care_needs": "Use rabbit-experienced veterinary care. Not eating can be an emergency.",
        "care_difficulty": "Specialist care required",
        "health_considerations": "Dental disease and digestive problems are important concerns.",
        "enrichment": "Tunnels, hideouts, digging and hay-based foraging.",
    },
    "Guinea pigs": {
        "purpose": "Companion",
        "activity_level": "Daily floor time and exploration",
        "diet": "Grass hay, fresh water, suitable vegetables and guinea-pig food containing vitamin C.",
        "grooming": "Brush according to coat type; check nails and teeth.",
        "exercise_needs": "Daily safe floor time.",
        "housing_needs": "Spacious, ventilated housing with solid flooring and hiding places.",
        "social_needs": "Compatible guinea pig companions are generally beneficial.",
        "care_needs": "Monitor eating, droppings, teeth and weight.",
        "care_difficulty": "Moderate; daily specialist care",
        "health_considerations": "Vitamin C deficiency and dental problems require attention.",
        "enrichment": "Tunnels, hay foraging, hideouts and safe chew items.",
    },
    "Hamsters": {
        "purpose": "Companion",
        "activity_level": "Primarily active during evenings and nights",
        "diet": "Balanced hamster food, suitable vegetables and fresh water.",
        "grooming": "Provide suitable substrate and species-appropriate sand bathing.",
        "exercise_needs": "Suitable solid-surface wheel, deep substrate and foraging.",
        "housing_needs": "Spacious, secure enclosure with deep bedding and hiding places.",
        "social_needs": "Respect sleeping hours; many pet hamsters must live alone.",
        "care_needs": "Monitor weight, teeth, skin and activity.",
        "care_difficulty": "Moderate; nocturnal needs must be respected",
        "health_considerations": "Dental, skin and respiratory problems can occur.",
        "enrichment": "Deep bedding, tunnels, scatter feeding and a suitable wheel.",
    },
    "Birds": {
        "purpose": "Companion; requirements vary by species",
        "activity_level": "Daily movement and mental enrichment",
        "diet": "Species-appropriate balanced food and fresh water.",
        "grooming": "Provide bathing opportunities; monitor beak, nails and feathers.",
        "exercise_needs": "Daily movement and safe supervised activity.",
        "housing_needs": "Roomy, secure enclosure with suitable bar spacing and perches.",
        "social_needs": "Provide species-appropriate interaction without forcing contact.",
        "care_needs": "Use an avian veterinarian for preventive care and illness.",
        "care_difficulty": "Moderate to high; species dependent",
        "health_considerations": "Dietary deficiencies and respiratory hazards require attention.",
        "enrichment": "Foraging, safe toys, varied perches and training.",
    },
    "Fish": {
        "purpose": "Aquarium keeping",
        "activity_level": "Species-specific swimming space",
        "diet": "Species-appropriate food in suitable quantities; avoid overfeeding.",
        "grooming": "Maintain water quality and observe fish behaviour.",
        "exercise_needs": "Provide appropriate swimming space and habitat structure.",
        "housing_needs": "Properly sized, cycled aquarium with filtration and suitable water conditions.",
        "social_needs": "Research schooling, territorial and tankmate requirements.",
        "care_needs": "Test water, maintain filtration and perform suitable water changes.",
        "care_difficulty": "Depends on species and aquarium requirements",
        "health_considerations": "Poor water quality is a major risk.",
        "enrichment": "Suitable plants, hiding places and naturalistic habitat.",
    },
    "Tortoises": {
        "purpose": "Specialist reptile keeping",
        "activity_level": "Species-appropriate roaming space",
        "diet": "Diet depends on species; do not assume one diet suits all tortoises.",
        "grooming": "Monitor shell, skin, eyes, beak and nails.",
        "exercise_needs": "Secure roaming and grazing opportunities where appropriate.",
        "housing_needs": "Species-appropriate temperature, lighting, UVB and humidity.",
        "social_needs": "Assess species-specific behaviour and avoid overcrowding.",
        "care_needs": "Use a reptile-experienced veterinarian and check applicable wildlife laws.",
        "care_difficulty": "High; long-term specialist commitment",
        "health_considerations": "Incorrect diet, temperature or UVB can cause serious problems.",
        "enrichment": "Suitable terrain, hides and safe exploration.",
    },
    "Pet rats": {
        "purpose": "Companion",
        "activity_level": "Active and curious; daily exploration",
        "diet": "Balanced rat-specific food, suitable fresh foods and clean water.",
        "grooming": "Inspect coat, skin, nails and teeth.",
        "exercise_needs": "Supervised exploration and a safe play area.",
        "housing_needs": "Spacious, ventilated housing with climbing structures and hides.",
        "social_needs": "Positive interaction and compatible rat companions.",
        "care_needs": "Monitor breathing, lumps, appetite and activity.",
        "care_difficulty": "Moderate; social and health needs",
        "health_considerations": "Respiratory disease and tumours are concerns.",
        "enrichment": "Foraging, climbing, tunnels and nesting material.",
    },
    "Chinchillas": {
        "purpose": "Specialist companion",
        "activity_level": "Active and agile; safe jumping and exploration",
        "diet": "Suitable grass hay, fresh water and chinchilla pellets.",
        "grooming": "Provide appropriate dust baths; avoid water bathing unless directed by a veterinarian.",
        "exercise_needs": "Safe supervised exercise and climbing.",
        "housing_needs": "Spacious, ventilated housing with platforms; protect from overheating.",
        "social_needs": "Social needs vary; introduce companions carefully.",
        "care_needs": "Monitor teeth, digestion and heat tolerance.",
        "care_difficulty": "High; specialist temperature and dental needs",
        "health_considerations": "Dental disease, digestive problems and heat stress are concerns.",
        "enrichment": "Safe ledges, tunnels, chew materials and foraging.",
    },
}

# Known facts (size and lifespan come from the rows instead)
BREED_FACTS = {
    ("Dogs", "Labrador Retriever"): {
        "origin": "Newfoundland, Canada; developed further in the United Kingdom",
        "purpose": "Retrieving and working companion",
        "temperament": "Often friendly, outgoing and eager to work", "activity_level": "High",
    },
    ("Dogs", "German Shepherd"): {
        "origin": "Germany", "purpose": "Herding, service and working dog",
        "temperament": "Often intelligent, alert and loyal", "activity_level": "High",
    },
    ("Dogs", "Golden Retriever"): {
        "origin": "Scotland", "purpose": "Retrieving and companion",
        "temperament": "Often friendly, sociable and trainable", "activity_level": "High",
    },
    ("Cats", "Abyssinian"): {
        "origin": "Breed history associated with Britain; exact origin is debated",
        "purpose": "Companion",
        "temperament": "Often active, curious and people-oriented", "activity_level": "High",
    },
    ("Cats", "Persian"): {
        "origin": "Persia, historically associated with modern Iran", "purpose": "Companion",
        "temperament": "Often calm and gentle", "activity_level": "Low to moderate",
    },
    ("Cats", "Siamese"): {
        "origin": "Thailand, historically Siam", "purpose": "Companion",
        "temperament": "Often vocal, social and active", "activity_level": "High",
    },
    ("Birds", "Budgerigar"): {
        "origin": "Australia", "purpose": "Companion bird",
        "temperament": "Often social, active and vocal", "activity_level": "High",
    },
    ("Birds", "African Grey Parrot"): {
        "origin": "Central and West Africa", "purpose": "Companion parrot",
        "temperament": "Highly intelligent; social and mentally demanding",
        "activity_level": "High", "experience_level": "Experienced bird keeper recommended",
        "care_difficulty": "High; substantial long-term enrichment and social needs",
    },
    ("Rabbits", "Holland Lop"): {
        "origin": "Netherlands", "purpose": "Companion",
        "temperament": "Varies by individual; gentle handling is important",
    },
    ("Guinea pigs", "Abyssinian"): {
        "origin": "Domestic guinea pig breed developed through selective breeding",
        "purpose": "Companion",
    },
    ("Hamsters", "Syrian"): {
        "origin": "Syria and surrounding region", "purpose": "Companion",
        "temperament": "Usually solitary; individuals vary in handling tolerance",
        "social_needs": "Generally house alone; provide enrichment and gentle handling.",
    },
    ("Fish", "Betta"): {
        "origin": "Southeast Asia", "purpose": "Freshwater aquarium fish",
        "temperament": "Males are often territorial",
        "housing_needs": "Use a heated, filtered, cycled aquarium with adequate space and gentle flow.",
    },
    ("Tortoises", "Indian Star Tortoise"): {
        "origin": "India and Sri Lanka",
        "purpose": "Specialist reptile; protected wildlife considerations apply",
        "experience_level": "Specialist experience and legal checks required",
        "care_difficulty": "High; check local wildlife laws before considering ownership",
    },
}

DATA = {
    "Dogs": """
Labrador Retriever|55-62|25-36|10-12|fvsbu
German Shepherd|55-65|22-40|9-13|gmsvf
Golden Retriever|51-61|25-34|10-12|fvbu
Poodle|45-60|20-32|12-15|fvab
Bulldog|31-40|18-25|8-10|fa
Beagle|33-41|9-11|12-15|fa
Rottweiler|56-69|35-60|8-10|gm
Dachshund|20-27|7-14|12-16|fa
Siberian Husky|51-60|16-27|12-14|f
Shih Tzu|20-28|4-7|10-16|fab
Pomeranian|18-24|2-3|12-16|ab
Boxer|53-63|25-32|10-12|gf
Doberman Pinscher|63-72|27-45|10-12|gm
Great Dane|71-86|45-90|7-10|gf
Border Collie|46-56|14-20|12-15|h
Indian Pariah Dog|50-63|20-30|12-16|gfcb
Cocker Spaniel|34-41|12-15|12-15|fau
Pug|25-33|6-9|12-15|fab
Chihuahua|15-23|1.5-3|14-18|ab
Rajapalayam|65-75|22-25|10-12|gc
Mudhol Hound|62-72|20-28|10-13|uc
Kombai|46-56|20-30|10-14|gc
Chippiparai|60-76|16-22|10-13|uc
Indian Spitz|23-30|5-6|12-15|abfc
Kanni|60-65|16-20|12-14|uc
Himalayan Sheepdog|60-70|35-50|10-12|g
Gaddi Kutta|65-75|35-50|10-12|g
Bakharwal Dog|65-75|35-45|10-12|g
Caravan Hound|66-76|18-30|10-14|uc
Rampur Greyhound|60-76|22-32|10-12|uc
Jonangi|38-50|12-18|10-12|c
Belgian Malinois|56-66|25-34|12-14|gms
Dutch Shepherd|55-62|23-32|11-14|gm
Bloodhound|58-69|36-50|7-10|s
Cane Corso|60-68|40-50|9-12|g
Giant Schnauzer|60-70|25-48|10-12|gm
Bullmastiff|61-69|41-59|8-10|g
Mastiff|70-76|54-100|6-10|g
Presa Canario|55-66|40-60|9-11|g
Dogo Argentino|60-68|35-45|9-12|g
Black Russian Terrier|64-77|36-68|10-12|g
Kangal|71-86|41-64|11-15|g
Caucasian Shepherd|64-75|45-100|10-12|g
Tibetan Mastiff|61-71|45-72|10-12|g
Anatolian Shepherd|71-81|41-64|11-13|g
Great Pyrenees|63-81|36-54|10-12|g
Neapolitan Mastiff|60-77|50-70|7-9|g
Fila Brasileiro|60-75|40-50|9-11|g
Boerboel|58-70|50-90|9-11|g
Rhodesian Ridgeback|61-69|29-41|10-12|gu
Akita|61-71|32-59|10-13|g
Alaskan Malamute|58-71|34-45|10-14|
Belgian Tervuren|58-66|20-34|12-14|hm
Belgian Sheepdog|56-66|20-34|12-14|h
Beauceron|61-70|30-45|10-12|gmh
Australian Shepherd|46-58|16-32|12-15|h
Australian Cattle Dog|43-51|14-22|12-16|h
Old English Sheepdog|53-61|27-41|10-12|h
Shetland Sheepdog|33-41|6-12|12-14|hf
Rough Collie|51-61|18-30|12-14|hf
Briard|56-69|27-40|10-12|hg
Bouvier des Flandres|59-70|27-40|10-12|hg
Pembroke Welsh Corgi|25-30|10-14|12-14|hfa
Cardigan Welsh Corgi|27-32|11-17|12-15|hf
Bergamasco|54-62|26-38|13-15|h
Polish Lowland Sheepdog|42-50|14-23|12-14|h
Icelandic Sheepdog|41-46|9-14|12-15|hf
Swedish Vallhund|31-35|11-16|12-15|h
Entlebucher Mountain Dog|40-50|20-30|11-13|h
Picardy Sheepdog|55-65|23-32|12-14|h
Bernese Mountain Dog|58-70|32-52|7-10|f
Saint Bernard|65-90|55-82|8-10|s
Newfoundland|63-74|45-70|9-10|s
Leonberger|65-80|40-77|8-9|f
Samoyed|46-60|16-30|12-14|f
Chow Chow|46-56|20-32|8-12|g
Shar Pei|44-51|16-29|8-12|g
Weimaraner|56-70|25-40|10-13|u
Vizsla|53-64|20-30|12-14|fu
German Shorthaired Pointer|53-64|20-32|10-12|fu
German Wirehaired Pointer|55-67|23-32|12-14|u
English Pointer|58-69|20-34|12-15|u
English Setter|61-69|20-36|10-12|fu
Irish Setter|58-70|24-32|12-15|fu
Gordon Setter|62-69|25-36|10-12|u
Brittany|43-52|14-18|12-14|u
English Springer Spaniel|46-56|18-25|12-14|fu
Welsh Springer Spaniel|46-48|16-20|12-15|fu
Field Spaniel|43-46|18-25|11-13|u
Clumber Spaniel|43-51|25-36|10-12|u
Spinone Italiano|59-70|29-39|10-12|u
Wirehaired Pointing Griffon|50-60|18-30|12-15|u
Flat-Coated Retriever|56-61|25-36|8-10|fu
Chesapeake Bay Retriever|53-66|25-36|10-13|u
Nova Scotia Duck Tolling Retriever|45-51|17-23|12-14|u
Portuguese Water Dog|43-57|16-27|10-14|fu
Lagotto Romagnolo|41-48|11-16|15-17|u
Irish Wolfhound|71-86|40-55|6-8|f
Scottish Deerhound|71-76|34-50|8-11|u
Greyhound|68-76|27-40|10-14|fc
Whippet|44-51|9-18|12-15|fa
Saluki|58-71|16-29|10-14|uc
Afghan Hound|63-74|23-27|12-14|
Borzoi|68-82|27-48|9-14|
Basenji|40-43|9-12|12-14|ac
Ibizan Hound|56-74|20-29|11-14|uc
Pharaoh Hound|53-64|18-27|12-14|uc
Azawakh|57-74|15-25|12-15|c
Sloughi|61-72|18-27|12-16|c
Canaan Dog|48-61|18-25|12-15|gc
Carolina Dog|43-61|15-25|12-15|c
Italian Greyhound|33-38|3-5|14-15|a
Basset Hound|33-38|20-29|10-12|f
Black and Tan Coonhound|58-69|23-34|10-12|u
Redbone Coonhound|53-69|20-32|12-15|u
English Foxhound|58-64|29-34|10-13|u
Harrier|48-53|18-27|12-15|u
Norwegian Elkhound|49-52|20-23|12-15|u
Finnish Spitz|39-50|9-16|12-15|
Jack Russell Terrier|25-38|5-8|13-16|fa
Parson Russell Terrier|31-38|6-8|13-15|fa
Yorkshire Terrier|18-23|2-3|11-15|ab
West Highland White Terrier|25-28|7-10|13-15|fa
Scottish Terrier|25-28|8-10|11-13|a
Cairn Terrier|23-33|6-8|13-15|fa
Airedale Terrier|56-61|18-29|11-14|g
Staffordshire Bull Terrier|36-41|11-17|12-14|f
American Staffordshire Terrier|43-48|18-29|12-16|g
Bull Terrier|53-56|23-32|11-14|
Miniature Schnauzer|30-36|5-9|12-15|fa
Standard Schnauzer|45-51|14-20|13-16|g
Wire Fox Terrier|36-39|7-8|12-15|a
Border Terrier|25-28|5-7|12-15|fa
Irish Terrier|45-48|11-12|12-15|
Kerry Blue Terrier|44-50|15-18|12-15|
Bedlington Terrier|38-43|8-10|12-14|
Manchester Terrier|38-41|5-10|14-16|a
Rat Terrier|25-45|4-11|15-18|fa
Maltese|20-25|2-4|12-15|ab
Bichon Frise|23-30|5-8|14-15|fab
Havanese|23-28|4-7|14-16|fab
Lhasa Apso|25-28|5-8|12-15|a
Papillon|20-28|3-5|14-16|a
Cavalier King Charles Spaniel|30-33|5-8|12-15|fab
Miniature Pinscher|25-32|4-6|12-16|a
Pekingese|15-23|3-6|12-14|a
Japanese Chin|20-27|2-5|10-12|a
Boston Terrier|38-43|5-11|11-13|fa
French Bulldog|27-35|8-14|10-12|a
Shiba Inu|33-43|8-11|13-16|a
Japanese Spitz|30-36|5-10|10-16|fa
American Eskimo Dog|23-48|3-18|13-15|f
Keeshond|43-46|14-18|12-15|f
Schipperke|25-33|5-9|13-15|g
Coton de Tulear|22-30|3-6|14-16|fa
Toy Poodle|24-28|2-4|12-18|ab
Miniature Poodle|28-38|5-9|12-15|fa
American Cocker Spaniel|34-39|7-14|12-15|fa
Tibetan Spaniel|24-28|4-7|12-15|a
Tibetan Terrier|35-41|8-14|12-15|f
Silky Terrier|23-26|3-5|12-15|a
Chinese Crested|23-33|2-5|13-18|a
Lowchen|25-33|4-8|13-15|a
Affenpinscher|24-28|3-4|12-14|a
Brussels Griffon|18-20|3-5|12-15|a
English Toy Spaniel|25-28|3-6|10-12|a
Labradoodle|53-61|23-29|12-14|f
Goldendoodle|51-61|20-34|10-15|f
Cockapoo|25-39|5-12|14-16|fa
Maltipoo|20-35|2-9|12-15|ab
Puggle|25-38|7-14|10-15|f
Kuvasz|66-76|30-52|10-12|g
Komondor|65-80|36-59|10-12|g
Sarplaninac|56-62|30-45|11-13|g
Hovawart|58-70|25-40|10-14|g
Great Swiss Mountain Dog|60-72|38-63|8-11|f
Dalmatian|54-61|20-32|11-13|f
Xoloitzcuintli|25-60|4-14|13-18|c
Australian Terrier|23-28|5-7|12-15|a
Curly-Coated Retriever|63-69|27-36|10-12|u
Miniature Bull Terrier|25-36|9-14|11-14|
Norfolk Terrier|24-26|5-6|12-16|a
Norwich Terrier|24-26|5-6|12-15|a
Soft Coated Wheaten Terrier|43-49|14-18|12-14|f
Welsh Terrier|39|9-10|12-15|
""",
    "Cats": """
Abyssinian|23-28|3-5|9-15|fa
Persian|25-38|3-6|12-17|fa
Siamese|20-25|3-5|12-20|fab
Maine Coon|25-41|5-8|12-15|f
Ragdoll|23-28|4-9|12-17|fa
Bengal|20-25|3-7|12-16|f
British Shorthair|30-33|4-8|12-17|fa
Sphynx|20-25|3-5|8-14|a
Birman|20-25|3-6|12-16|fa
Scottish Fold|20-25|3-6|11-14|fa
Russian Blue|23-25|3-5|15-20|ab
Norwegian Forest Cat|23-32|3-9|14-16|f
American Shorthair|20-25|4-7|15-20|fb
Indian Desi Cat|23-28|3-5|12-15|fabc
Exotic Shorthair|20-25|3-6|12-15|fa
European Shorthair|23-28|3-6|12-15|fa
Burmese|20-25|3-6|10-17|fa
Oriental Shorthair|20-25|2-5|12-20|a
Devon Rex|20-25|2-4|9-15|a
Cornish Rex|20-25|2-4|11-15|a
Tonkinese|20-25|3-5|10-16|fa
Turkish Angora|23-28|2-5|12-18|a
Turkish Van|25-35|4-8|12-17|f
Egyptian Mau|20-30|3-5|12-15|a
Ocicat|23-28|3-7|12-18|f
Chartreux|23-25|3-7|12-15|f
Korat|23-25|2-4|10-15|a
Manx|23-28|3-6|8-14|f
Cymric|23-28|3-6|8-14|f
American Curl|23-25|2-5|12-16|fa
Balinese|20-25|2-5|10-20|a
Siberian|23-30|4-9|11-15|f
Somali|23-28|3-5|11-16|a
Singapura|20-23|2-4|11-15|a
Snowshoe|20-28|2-5|14-19|fa
Selkirk Rex|23-28|3-7|10-15|f
LaPerm|20-25|2-5|10-15|a
Munchkin|13-18|2-4|12-15|a
Himalayan|23-25|3-6|9-15|fa
Nebelung|25-28|3-6|15-18|a
Havana Brown|23-28|2-4|10-15|a
Japanese Bobtail|20-25|3-4|9-15|fa
Pixie-bob|23-28|4-8|13-15|f
Toyger|20-25|3-5|12-15|
Bombay|23-28|3-5|12-16|fa
American Bobtail|23-28|3-7|13-15|f
Burmilla|20-25|3-6|10-15|
Lykoi|20-25|2-4|11-15|a
Peterbald|20-25|3-5|12-15|a
Ragamuffin|23-28|5-9|12-16|f
Sokoke|23-28|3-5|12-15|
Khao Manee|23-28|3-5|10-15|a
Savannah|35-43|5-9|12-20|e
Chausie|35-40|5-11|12-14|e
American Wirehair|20-25|3-6|7-14|f
Australian Mist|20-25|3-6|12-18|fa
Bengal Longhair|20-25|3-7|12-16|f
Brazilian Shorthair|23-28|3-6|12-15|fa
California Spangled|35-40|6-9|12-16|e
Chantilly-Tiffany|23-28|3-6|14-16|fa
Colorpoint Shorthair|20-25|3-5|12-15|a
European Burmese|20-25|3-6|10-17|fa
German Rex|20-25|2-4|11-15|a
Kurilian Bobtail|23-28|3-7|15-20|f
Oriental Longhair|20-25|2-5|12-20|a
Scottish Straight|20-25|3-6|11-14|fa
Serengeti|35-40|5-8|9-15|e
""",
    "Rabbits": """
Holland Lop|20-25|1.5-2|7-12|ab
Netherland Dwarf|20-25|0.5-1.1|10-12|a
Mini Rex|25-30|1.5-2|7-10|ab
Lionhead|25-30|1.2-1.7|7-10|a
Dutch Rabbit|25-30|1.5-2.5|5-10|ab
Flemish Giant|35-45|6-10|5-8|f
English Angora|25-30|2.3-3.4|7-12|
English Lop|30-40|4-5|5-7|
Rex Rabbit|35-40|3-4.5|5-8|f
Mini Lop|25-30|1.8-2.7|6-10|ab
Polish Rabbit|20-25|1-1.5|5-8|a
Himalayan Rabbit|25-30|1.8-2.5|5-8|b
Californian Rabbit|35-40|3.5-4.5|5-10|b
New Zealand White|40-45|4-5.5|5-8|b
Harlequin Rabbit|35-40|2.7-3.6|5-8|f
Silver Marten|30-35|2.7-3.6|5-8|f
Checkered Giant|45-55|4-5.5|5-8|
French Lop|35-45|4.5-6|5-8|f
Jersey Wooly|20-25|1-1.5|7-10|a
Mini Satin|25-30|2-2.5|6-10|b
Britannia Petite|20-25|0.7-1|6-8|a
Belgian Hare|45-55|2.7-4|6-10|
American Fuzzy Lop|20-25|1.4-1.8|7-10|a
Cinnamon Rabbit|30-35|3-4.5|5-8|
Tan Rabbit|25-30|1.8-2.5|6-9|
Champagne d'Argent|35-45|3.2-4.5|5-8|
French Angora|30-35|3-4|7-12|
Silver Fox Rabbit|35-40|3-5|5-8|
""",
    "Guinea pigs": """
Abyssinian|20-25|700-1200|5-8|f
American|20-25|700-1200|5-8|fb
Peruvian|20-25|700-1200|5-8|f
Silkie|20-25|700-1200|5-8|f
Teddy|20-25|700-1200|5-8|fb
Texel|20-25|700-1200|5-8|f
Coronet|20-25|700-1200|5-8|f
White Crested|20-25|700-1200|5-8|fb
Skinny Pig|20-25|600-1000|5-7|
Baldwin|20-25|600-1000|5-7|
Alpaca Guinea Pig|20-25|700-1200|5-8|f
Rex Guinea Pig|20-25|700-1200|5-8|f
American Satin|20-25|700-1200|5-8|f
English Crested|20-25|700-1200|5-8|f
Lunkarya|20-25|700-1200|5-8|f
Merino|20-25|700-1200|5-8|f
Sheba Mini Yak|20-25|700-1200|5-8|f
""",
    "Hamsters": """
Syrian|13-18|100-200|2-3|
Roborovski|4-5|20-30|3-3.5|
Winter White Dwarf|8-10|30-40|1.5-2|
Campbell's Dwarf|8-10|30-50|1.5-2|
Chinese Hamster|9-12|30-50|2-3|
Long-haired Syrian|13-18|100-200|2-3|
Banded Syrian|13-18|100-200|2-3|
Black Bear Syrian|13-18|100-200|2-3|
Hybrid Dwarf Hamster|8-10|30-50|1.5-2|
Pearl Winter White|8-10|30-40|1.5-2|
Sapphire Winter White|8-10|30-40|1.5-2|
""",
    "Birds": """
Budgerigar|18|30-40|5-10|bxa
African Grey Parrot|33|400-500|40-60|xe
Cockatiel|30|80-100|15-25|ba
Lovebird|15|40-60|10-15|ba
Canary|13|15-30|10-15|ab
Finch|11|10-15|5-9|ab
Green-cheeked Conure|25|60-80|15-25|a
Sun Conure|30|100-130|20-30|
Eclectus Parrot|35|400-600|30-40|xe
Indian Ringneck Parakeet|40|100-140|20-30|cx
Alexandrine Parakeet|58|200-300|25-30|cx
Plum-headed Parakeet|33|60-90|15-20|c
Blue-and-gold Macaw|85|900-1300|30-50|e
Scarlet Macaw|85|900-1100|40-50|e
Green-winged Macaw|90|1100-1700|40-60|e
Hahn's Macaw|30|140-170|20-30|
Severe Macaw|45|300-400|20-30|x
Yellow-naped Amazon|38|450-600|40-60|xe
Blue-fronted Amazon|37|400-500|40-60|xe
Orange-winged Amazon|33|340-400|40-60|x
Senegal Parrot|23|120-170|20-30|
Meyer's Parrot|21|100-130|20-30|
Quaker Parrot|29|90-120|15-25|x
Black-headed Caique|23|140-170|25-40|
Blue-headed Pionus|28|230-270|25-40|
Goffin's Cockatoo|32|300-350|30-40|
Umbrella Cockatoo|46|550-800|40-60|e
Sulphur-crested Cockatoo|50|810-975|40-70|e
Moluccan Cockatoo|50|850-1100|40-60|e
Bourke's Parakeet|19|40-50|10-15|ba
Eastern Rosella|30|90-120|15-25|
Gouldian Finch|12|13-18|5-7|a
Society Finch|11|10-14|6-8|ba
Java Sparrow|15|23-30|7-10|a
Diamond Dove|20|30-40|8-15|ba
Ringneck Dove|28|130-180|12-20|b
Fancy Pigeon|33|300-500|10-15|
Fischer's Lovebird|14|40-55|10-15|ba
Peach-faced Lovebird|15|50-60|10-15|ba
Yellow-collared Lovebird|14|40-50|10-15|a
Red-bellied Parrot|25|130-160|25-30|
Jardine's Parrot|28|140-200|25-35|
Timneh African Grey|30|275-400|40-60|xe
Rainbow Lorikeet|30|120-150|15-25|
Lineolated Parakeet|16|40-50|10-15|ba
Pacific Parrotlet|12|25-35|15-20|a
Gloster Canary|11|15-25|10-12|a
Yorkshire Canary|17|20-30|10-12|a
Blue-crowned Conure|37|230-260|20-30|
Jenday Conure|30|110-130|20-30|
Nanday Conure|30|130-150|20-30|
Dusky Conure|25|90-120|20-30|
Hyacinth Macaw|100|1400-1700|50-60|e
Masked Lovebird|14|40-50|10-15|a
Pineapple Green-cheeked Conure|25|60-80|15-25|a
Princess Parrot|40|90-130|15-25|
""",
    "Fish": """
Betta|6-7||2-5|b
Goldfish|10-30||10-20|b
Guppy|3-6||1-3|bk
Neon Tetra|3-4||5-8|bk
Molly|7-10||3-5|bk
Platy|4-7||3-5|bk
Angelfish|10-15||8-10|k
Zebra Danio|4-5||3-5|bk
Discus|15-20||10-15|e
Swordtail|8-12||3-5|bk
Cardinal Tetra|4-5||4-5|k
Black Skirt Tetra|6-7||4-5|bk
Serpae Tetra|4||3-5|k
Rummy-nose Tetra|5||4-6|k
Harlequin Rasbora|4-5||5-8|bk
Cherry Barb|5||4-6|bk
Tiger Barb|6-7||5-7|
Rosy Barb|10||5-6|k
Tinfoil Barb|35||8-10|e
Dwarf Gourami|5-8||4-6|k
Pearl Gourami|10-12||4-8|k
Honey Gourami|5||4-8|k
Three-spot Gourami|10-15||4-6|
Kissing Gourami|20-30||7-8|
Paradise Fish|10||5-8|
Bronze Corydoras|6-7||5-10|bk
Panda Corydoras|5||5-8|k
Common Pleco|35-50||10-15|e
Bristlenose Pleco|10-15||5-10|k
Otocinclus|4-5||3-5|k
Siamese Algae Eater|12-15||8-10|k
Kuhli Loach|8-10||10-14|k
Clown Loach|20-30||10-15|
Yoyo Loach|10||5-8|
Weather Loach|20-25||10-15|
Oscar|25-35||10-15|e
Convict Cichlid|10-15||8-10|
Jack Dempsey|20-25||8-10|e
Green Terror|25-30||8-10|e
Firemouth Cichlid|12-15||8-10|
Yellow Lab Cichlid|10||6-10|
Peacock Cichlid|13-20||8-10|
German Blue Ram|5-7||2-4|e
Apistogramma|5-8||3-5|
Kribensis|8-10||5-8|k
Severum|20-25||10-15|
Flowerhorn|30-40||10-12|e
Silver Arowana|90-120||10-20|e
Boesemani Rainbowfish|10-12||5-8|k
Celestial Pearl Danio|2-3||3-5|
White Cloud Mountain Minnow|4-5||3-5|bk
Endler's Livebearer|3||2-3|bk
Koi|60-90||25-35|e
Oranda|15-20||10-15|b
Redtail Shark|15-18||5-8|
Rainbow Shark|15||5-8|
Sailfin Molly|12-15||3-5|
Bala Shark|30||8-10|e
Glass Catfish|10||6-8|k
Blood Parrot Cichlid|15-20||10-15|
Clownfish|8-11||3-10|
Blue Tang|25-30||8-20|e
Yellow Tang|20||10-30|e
Firefish Goby|8||3-5|
Banggai Cardinalfish|8||4-5|
Royal Gramma|8||5-6|
Mandarinfish|6-8||2-4|e
""",
    "Tortoises": """
Indian Star Tortoise|15-30|1.5-6|35-80|e
Russian Tortoise|15-20|0.5-1.5|40-50|
Greek Tortoise|18-20|1-2|50-100|
Hermann's Tortoise|15-20|1-2|50-75|
Sulcata Tortoise|60-80|40-100|50-100|e
Red-footed Tortoise|30-35|5-8|40-50|
Yellow-footed Tortoise|35-45|8-12|50-60|
Leopard Tortoise|35-45|10-20|50-100|e
Marginated Tortoise|25-30|3-5|50-100|
Egyptian Tortoise|10-13|0.2-0.4|40-50|
Pancake Tortoise|15-17|0.5-0.6|25-35|e
Radiated Tortoise|30-40|10-15|50-100|e
Elongated Tortoise|25-35|2-4|50-70|e
Burmese Star Tortoise|20-25|2-3|50-80|e
Red-eared Slider|20-30|1-2|20-30|
Eastern Box Turtle|12-15|0.4-0.5|30-50|e
Aldabra Giant Tortoise|90-120|150-250|100-150|e
""",
    "Pet rats": """
Standard Rat|15-25|300-600|2-3|a
Dumbo Rat|15-25|300-600|2-3|a
Rex Rat|15-25|300-600|2-3|a
Hairless Rat|15-25|300-600|2-3|a
Satin Rat|15-25|300-600|2-3|a
Hooded Rat|15-25|300-600|2-3|a
Manx Rat|15-25|300-600|2-3|a
Siamese Rat|15-25|300-600|2-3|a
Berkshire Rat|15-25|300-600|2-3|a
Blue Rat|15-25|300-600|2-3|a
""",
    "Chinchillas": """
Standard Grey Chinchilla|22-38|400-600|10-20|e
White Chinchilla|22-38|400-600|10-20|e
Beige Chinchilla|22-38|400-600|10-20|e
Black Velvet Chinchilla|22-38|400-600|10-20|e
Violet Chinchilla|22-38|400-600|10-20|e
Charcoal Chinchilla|22-38|400-600|10-20|e
Sapphire Chinchilla|22-38|400-600|10-20|e
Brown Velvet|22-38|400-600|10-20|e
Ebony|22-38|400-600|10-20|e
Pearl|22-38|400-600|10-20|e
""",
}

# Old duplicate entries (same animal under another name). seed_catalogue deletes them.
REMOVE = [
    ("Guinea pigs", "Alpaca"), ("Guinea pigs", "Rex"),
    ("Chinchillas", "Beige"), ("Chinchillas", "Black Velvet"), ("Chinchillas", "Charcoal"),
    ("Chinchillas", "Sapphire"), ("Chinchillas", "Standard Grey"),
    ("Chinchillas", "Violet"), ("Chinchillas", "White"),
    ("Hamsters", "Djungarian"), ("Hamsters", "Golden Syrian"),
    ("Hamsters", "Short-haired Syrian"), ("Hamsters", "Teddy Bear Syrian"),
    ("Hamsters", "European Hamster"),
    ("Birds", "Cockatoo"), ("Birds", "Parrotlet"), ("Birds", "Pionus Parrot"),
    ("Birds", "Rose-ringed Parakeet"), ("Birds", "Zebra Finch"),
    ("Dogs", "Fox Terrier"), ("Rabbits", "New Zealand Rabbit"), ("Cats", "Pixiebob"),
    ("Fish", "Corydoras Catfish"),
    ("Fish", "Mikrogeophagus ramirezi (Ram Cichlid)"),
]


# ----------------------------------------------------------------- helpers
def iter_rows(category):
    for line in DATA[category].strip().splitlines():
        line = line.strip()
        if not line:
            continue
        name, height, weight, life, tags = [p.strip() for p in line.split("|")]
        yield name, height, weight, life, tags


def _max(value):
    try:
        return float(str(value).replace(" ", "").split("-")[-1])
    except ValueError:
        return 0.0


def size_for(category, height, weight):
    w, h = _max(weight), _max(height)
    if category == "Dogs":
        return "Small" if w <= 10 else "Medium" if w <= 25 else "Large" if w <= 45 else "Giant"
    if category == "Cats":
        return "Small" if w <= 4 else "Medium" if w <= 6 else "Large"
    if category == "Rabbits":
        return "Small" if w <= 2 else "Medium" if w <= 4 else "Large"
    if category == "Birds":
        return "Small" if w <= 60 else "Medium" if w <= 400 else "Large"
    if category == "Fish":
        return "Small" if h <= 8 else "Medium" if h <= 20 else "Large"
    if category == "Tortoises":
        return "Small" if w <= 2 else "Medium" if w <= 15 else "Large"
    return "Small"


def _lookup(table, category, size):
    value = table.get(category)
    if isinstance(value, dict):
        return value.get(size) or next(iter(value.values()))
    return value


def legal_note(name, category):
    if name in INDIAN_PROTECTED:
        return ("Native Indian wildlife protected under the Wildlife Protection Act, 1972. "
                "Keeping or trading may be illegal - do not buy; check with the Forest Department.")
    if name == "Red-eared Slider":
        return "Invasive species - never release into the wild. Check local rules before buying."
    if category == "Tortoises":
        return "Confirm legal source and wildlife rules (CITES papers) before buying."
    if category == "Birds" and any(w in name for w in EXOTIC_BIRD_WORDS):
        return "Exotic species: buy only with legal origin papers; check current Indian rules."
    return ""


def build_profile(name, category, height, weight, life, tags):
    size = size_for(category, height, weight)
    unit_w = UNITS[category][1]
    labels = [TAG_LABELS[t] for t in tags if t in TAG_LABELS]
    suitable = ", ".join(labels) if labels else "Companion"

    profile = {
        "origin": "", "purpose": "", "size": "", "weight_range": "",
        "height_range": "", "lifespan": "", "temperament": "",
        "activity_level": "", "experience_level": "",
        "child_compatibility": "Supervise interactions and teach safe handling.",
        "pet_compatibility": "Compatibility depends on species and individual temperament.",
        "purpose_tags": "companion", "diet": "", "grooming": "",
        "exercise_needs": "", "housing_needs": "", "social_needs": "",
        "care_needs": "", "care_difficulty": "",
        "health_considerations": "", "enrichment": "",
    }
    profile.update(CARE.get(category, {}))

    roles = [TAG_LABELS[t] for t in tags if t in "gmsvhu"]
    if roles:
        profile["purpose"] = "Working roles: " + ", ".join(roles)

    traits = [TRAITS[t] for t in tags if t in TRAITS]
    profile["temperament"] = ("Often " + ", ".join(traits)) if traits else "Varies by individual"

    if "e" in tags or (category == "Dogs" and "g" in tags):
        profile["experience_level"] = "Experienced owner recommended"
    elif "b" in tags:
        profile["experience_level"] = "Suitable for beginners"
    else:
        profile["experience_level"] = "Some experience helpful"

    if "f" in tags:
        profile["child_compatibility"] = "Generally good with children when supervised."

    facts = BREED_FACTS.get((category, name), {})
    profile.update({k: v for k, v in facts.items() if k not in ("size", "lifespan")})

    height_text = f"{height} cm{HEIGHT_SUFFIX[category]}" if height else ""
    weight_text = f"{weight} {unit_w}" if weight and unit_w else ""
    life_text = f"{life} years" if life else ""
    singular = SINGULAR[category]

    size_bits = [b for b in (height_text, weight_text) if b]
    description = (
        f"{name} is a {size.lower()} {singular}"
        + (f", usually {' and '.join(size_bits)}" if size_bits else "")
        + (f", living about {life_text}" if life_text else "")
        + f". Suitable for: {suitable}. "
        "Individual needs vary - confirm details with a qualified veterinarian."
    )

    profile.update({
        "description": description,
        "size": size,
        "height_range": height_text,
        "weight_range": weight_text,
        "lifespan": life_text,
        "adult_age": _lookup(ADULT_AGE, category, size),
        "suitable_for": suitable,
        "purpose_tags": suitable,
        "legal_note": legal_note(name, category),
        "is_active": True,
    })
    return profile