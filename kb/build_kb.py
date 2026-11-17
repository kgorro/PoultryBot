"""Builds kb/kb.json, the verified poultry knowledge base used by every PoultryBot component.

Scope: small and medium poultry farming in the Philippines (broilers, layers, native and free-range chickens,
ducks, quail), covering housing, brooding, feeding, health and biosecurity, incubation, food safety, and
farm business.

Safety rules for content:
  - Never give drug or vaccine doses. Point to the product label and a licensed veterinarian.
  - Treat Newcastle disease and avian influenza as reportable: advise isolation and reporting.
  - Figures are typical ranges for guidance, not prescriptions; strain guides and suppliers come first.

Edit entries here (or add a markdown pack in kb/sources/), run `python kb/build_kb.py`, and all components pick up the change.
"""
import json
from pathlib import Path

VERIFIED = "2026-10"
E = []


def add(id, group, cat, title, keywords, questions, answer):
    E.append(dict(id=id, group=group, category=cat, title=title, keywords=keywords,
                  questions=questions, answer=answer.strip()))


VET = "For diagnosis and treatment, consult a licensed veterinarian or your municipal or provincial veterinary office."

# ---------------------------------------------------------------- GENERAL
add("greet", "general", "Basics", "Greeting",
    ["hello", "hi", "good morning", "maayong", "kumusta", "start", "help"],
    ["Hi", "Hello, what can you do?"],
    """
Hello! I'm JuanGPT, a helper for poultry raisers.
Ask me about broilers, layers, native chickens, ducks, quail, brooding chicks, feeding, housing, vaccination, common diseases, incubation, or the business side of poultry.
For sick birds, I can help you recognize signs, but a veterinarian should confirm the diagnosis and treatment.
""")

add("fallback", "general", "Basics", "Fallback", [], [], """
I'm not sure about that one. I can help with chickens, ducks, and quail: brooding, feeding, housing, vaccination, common diseases, egg production, incubation, and farm business.
For a sick flock, contact a licensed veterinarian or your municipal agriculture office.
""")

add("start-backyard", "general", "Getting started", "Starting a backyard flock",
    ["start", "begin", "beginner", "backyard", "small", "flock", "raise", "first", "how many", "starting"],
    ["How do I start raising chickens?", "What do I need to start a small poultry farm?"],
    """
To start a small flock:
- Decide the purpose first: meat (broilers or native chickens), eggs (layers), or both (native or dual-purpose breeds).
- Start small, for example 20 to 50 birds, to learn before expanding.
- Prepare a clean, well-ventilated coop that keeps out rain, rats, dogs, and snakes.
- Buy healthy, vaccinated chicks from a reputable hatchery or supplier.
- Set up brooding with heat, feeders, and drinkers before the chicks arrive.
- Plan for feed, vaccines, and a record book from day one.
- Check with your barangay or municipal office about local rules on raising animals near homes.
""")

add("record-keeping", "business", "Business", "Farm records",
    ["record", "records", "logbook", "book", "track", "data", "monitor", "write"],
    ["What records should I keep for my poultry?", "How do I track my flock?"],
    """
Keep simple daily records for each batch or flock:
- Number of birds placed, deaths and culls each day, and the cause if known.
- Feed delivered and feed used, so you can compute feed conversion.
- Eggs collected per day (for layers) and body weights each week (for broilers).
- Vaccinations and medications given, with date, product, batch number, and withdrawal period.
- Costs and sales.
Records show problems early, such as a drop in eggs or feed intake, and they are needed to compute profit.
""")

# ---------------------------------------------------------------- BROILERS
add("broiler-overview", "broiler", "Broilers", "Raising broilers",
    ["broiler", "broilers", "meat", "raise", "grow", "fattening", "batch", "cycle", "harvest", "harvested", "market age", "days", "sell", "how long"],
    ["How do I raise broilers?", "How long does it take to grow broilers?"],
    """
Broilers are fast-growing meat chickens (commercial strains such as Cobb and Ross).
Typical cycle in the Philippines:
- Day 0 to 14: brooding with extra heat.
- Market age: about 30 to 40 days, at about 1.5 to 2.0 kg live weight, depending on strain, feed, and weather.
- Feed: booster or pre-starter, then starter, then finisher.
- Normal mortality for a well-managed batch is about 3 to 5%.
After each batch, clean and disinfect the house and leave it empty for 1 to 2 weeks before the next batch.
""")

add("broiler-feeding", "broiler", "Broilers", "Broiler feeding program",
    ["broiler", "feed", "feeding", "booster", "starter", "finisher", "pre-starter", "how much", "kilo", "consume", "protein"],
    ["What feed do broilers need?", "How much feed does a broiler eat until harvest?"],
    """
A common broiler feeding program:
- Booster or pre-starter (about day 1 to 10): highest protein, roughly 22 to 23%.
- Starter (about day 11 to 21): roughly 21% protein.
- Finisher (about day 22 to market): roughly 19% protein.
One broiler eats about 3 to 3.5 kg of feed to reach about 1.8 to 2 kg live weight, a feed conversion ratio (FCR) of about 1.6 to 1.8.
Give feed and clean water at all times. Follow your feed supplier's program, since products differ.
""")

add("broiler-fcr", "broiler", "Broilers", "Feed conversion ratio (FCR)",
    ["fcr", "feed conversion", "ratio", "efficiency", "compute", "formula", "calculate"],
    ["How do I compute FCR?", "What is a good feed conversion ratio?"],
    """
Feed conversion ratio (FCR) = total feed used (kg) / total live weight produced (kg).
Example: 300 kg of feed used for 100 birds weighing 180 kg in total gives FCR = 300 / 180 = 1.67.
Lower is better. Good broiler batches reach about 1.6 to 1.8. A high FCR points to feed wastage, heat stress, disease, poor chick quality, or keeping birds too long.
""")

add("broiler-lighting", "broiler", "Broilers", "Lighting for broilers",
    ["light", "lighting", "bulb", "hours", "dark", "night", "lamp"],
    ["How many hours of light do broilers need?", "Should I keep the lights on at night?"],
    """
- First 2 to 3 days: about 23 hours of light so chicks find feed and water.
- After that: about 18 to 20 hours of light with a dark period of 4 to 6 hours. Some darkness helps leg health and lowers stress.
Use dim, even light. In hot weather, light during cool night hours encourages birds to eat when it is less hot.
""")

add("stocking-density", "housing", "Housing", "Space per bird",
    ["space", "density", "stocking", "per square meter", "how many birds", "overcrowding", "crowded", "area", "sqm"],
    ["How many chickens per square meter?", "How much space do broilers need?"],
    """
Typical floor space in open-sided houses in a hot climate:
- Broilers: about 8 to 10 birds per square meter at market age.
- Layers or native hens on litter: about 4 to 5 birds per square meter.
- Chicks during brooding start closer together and are given more space every few days.
Crowding raises heat stress, wet litter, and disease. Closed, tunnel-ventilated houses can hold more birds.
""")

# ---------------------------------------------------------------- BROODING
add("brooding", "brooding", "Brooding", "Brooding chicks",
    ["brooding", "brooder", "chick", "chicks", "day-old", "newly", "new", "arrival", "arrive", "prepare", "brooder guard"],
    ["How do I brood day-old chicks?", "How do I take care of chicks in the first week?"],
    """
Brooding is the first 2 to 3 weeks, when chicks cannot yet keep themselves warm.
- Prepare 1 to 2 days early: clean house, dry litter (rice hull) about 5 to 8 cm deep, heater on, feed and water ready.
- Use a brooder guard (a ring of cardboard or plywood) to keep chicks near heat, feed, and water.
- Give clean water first, then feed on paper or trays so chicks find it easily.
- After 24 hours, gently feel the crops: most chicks should have full, soft crops.
- Watch the chicks' behavior to adjust heat (ask me about brooding temperature).
""")

add("brooding-temp", "brooding", "Brooding", "Brooding temperature",
    ["temperature", "temp", "heat", "degrees", "celsius", "warm", "cold", "huddle", "huddling", "crowding under", "bulb", "chick", "chicks", "brooder", "week old"],
    ["What temperature should chicks be kept at?", "Why are my chicks huddling?"],
    """
Typical temperature at chick level:
- Week 1: about 32 to 35 °C.
- Then lower by about 2 to 3 °C per week, to about 24 °C by week 4.
Read the chicks:
- Huddled under the heater and noisy: too cold.
- Panting, wings spread, far from the heater: too hot.
- Evenly spread and active: just right.
- All on one side: draft from the other side.
In warm lowland weather, broilers may need heat only for the first 7 to 14 days, mainly at night.
""")

add("chick-mortality", "brooding", "Brooding", "Chicks dying in the first week",
    ["chick", "chicks", "dying", "dead", "death", "mortality", "weak", "navel", "navels", "day old", "day-old", "first week"],
    ["Why are my chicks dying?", "What causes deaths in the first week?"],
    """
Common causes of early chick deaths:
- Poor chick quality from the hatchery, such as navel infection (wet, swollen navel).
- Chilling or overheating during transport or brooding.
- Chicks not finding water or feed (check crop fill after 24 hours).
- Dehydration from long transport.
- Dirty water, wet litter, or ammonia.
Up to about 1% loss in the first week can be normal. Higher losses: keep dead chicks, record the numbers, inform the hatchery, and ask a veterinarian to examine them.
""")

# ---------------------------------------------------------------- LAYERS
add("layer-overview", "layer", "Layers", "Raising layers",
    ["layer", "layers", "raise layers", "pullet", "pullets", "start laying", "point of lay", "age", "weeks", "peak", "hybrid", "when"],
    ["How do I raise layers?", "When do chickens start laying eggs?"],
    """
Commercial layer hybrids (for example Hy-Line, Lohmann, Dekalb) start laying at about 18 to 20 weeks and peak at about 25 to 30 weeks, when a good flock lays an egg from more than 90% of hens daily.
Phases:
- Chick (0 to 6 weeks), grower (6 to 16 weeks), pre-lay, then laying.
- Keep body weight on the strain's target during rearing. Underweight pullets lay small eggs and fewer of them.
Production slowly declines after the peak, and flocks are usually replaced at about 72 to 80 weeks of age.
""")

add("layer-feeding", "layer", "Layers", "Feeding laying hens",
    ["layer", "feed", "feeding", "layer mash", "how much", "grams", "calcium", "shell", "protein", "hen", "eat"],
    ["How much feed does a laying hen eat?", "What should I feed laying hens?"],
    """
- A laying hen eats about 110 to 120 g of layer feed per day, more in cool weather and less in heat.
- Layer feed has about 16 to 18% protein and 3.5 to 4.5% calcium for strong shells.
- Switch from grower to pre-lay or layer feed just before laying starts, as your strain guide or supplier advises.
- Coarse limestone or crushed shells can be offered in the afternoon, since shells form at night.
Give clean water at all times. Hens drink about twice as much water as feed.
""")

add("layer-lighting", "layer", "Layers", "Lighting for laying hens",
    ["light", "lighting", "hours", "egg", "lay", "laying", "stimulate", "day length", "bulb"],
    ["How many hours of light do laying hens need?", "Does light affect egg production?"],
    """
Day length strongly affects laying.
- Laying hens: about 16 hours of light per day, kept constant. Add early-morning light so the total reaches 16 hours.
- Never reduce light hours during lay, or production will drop.
- Growing pullets: keep light short and constant, then increase it gradually at the start of lay to bring them into production.
""")

add("low-egg", "layer", "Layers", "Low or dropping egg production",
    ["low", "drop", "decrease", "fewer", "less", "production", "stopped", "not laying", "stopped laying", "not", "egg production"],
    ["Why did my hens stop laying?", "Why is egg production dropping?"],
    """
Common reasons for low egg production:
- Age: production falls naturally after the peak; old hens lay less.
- Light: fewer than 16 hours or irregular lighting.
- Feed and water: wrong feed, low calcium or protein, or water running out even for a few hours.
- Heat stress, crowding, or sudden changes and stress.
- Molting or broodiness.
- Disease: Newcastle disease, infectious bronchitis, egg drop syndrome, and others can cause sudden drops, often with thin or misshapen shells.
- Parasites: mites, lice, and worms.
A sudden drop with sick or dying birds needs a veterinarian quickly.
""")

add("egg-shell", "layer", "Layers", "Soft or thin eggshells",
    ["soft", "thin", "shell", "shells", "shell-less", "weak", "cracked", "broken", "eggshell"],
    ["Why are my eggs soft-shelled?", "What causes thin eggshells?"],
    """
Thin or soft shells usually come from:
- Low calcium or vitamin D3 in the feed, or hens not eating enough in hot weather.
- Heat stress.
- Older hens, whose shells get thinner.
- Diseases such as infectious bronchitis or egg drop syndrome.
Use a proper layer feed, offer coarse limestone or shell grit, keep hens cool, and ask a veterinarian if many hens are affected suddenly.
""")

add("egg-eating", "layer", "Layers", "Hens eating eggs",
    ["eating", "eat", "egg", "eggs", "peck", "pecking", "broken", "cannibalism", "feather"],
    ["Why are my hens eating their eggs?", "How do I stop feather pecking?"],
    """
Egg eating and pecking usually start from boredom, crowding, bright nests, or a lack of protein or calcium.
- Collect eggs 2 to 3 times a day and remove broken eggs quickly.
- Provide dark, padded nest boxes, about one per 4 to 5 hens.
- Check feed calcium and protein.
- Reduce crowding and very bright light.
- Separate injured birds until healed, since blood attracts pecking.
""")

add("molting", "layer", "Layers", "Molting",
    ["molt", "molting", "moult", "feathers", "losing", "falling", "bald"],
    ["Why are my hens losing feathers?", "What is molting?"],
    """
Molting is the natural shedding and regrowth of feathers. Hens usually stop laying during the molt, which can last several weeks.
- Older hens molt about once a year. Stress, short days, or a feed or water interruption can trigger it early.
- Give good feed with enough protein during the molt to help feathers regrow.
Patchy feather loss with itching or red skin can mean mites or lice instead.
""")

add("broody", "layer", "Layers", "Broody hens",
    ["broody", "brooding", "sitting", "nest", "hen", "won't leave", "incubate", "setting"],
    ["My hen keeps sitting on the nest, what do I do?", "How do I stop a broody hen?"],
    """
A broody hen sits on eggs to hatch them and stops laying.
- To hatch chicks: give her fertile eggs in a quiet nest with feed and water nearby. Chicken eggs hatch in about 21 days.
- To stop broodiness: remove her from the nest and keep her for a few days in a bright, airy pen without nesting material.
Native hens go broody often. Commercial layer hybrids rarely do.
""")

add("culling", "layer", "Layers", "Culling non-productive hens",
    ["cull", "culling", "remove", "non-laying", "non layer", "unproductive", "identify", "tell", "laying hen", "old hens"],
    ["How do I know which hens are not laying?", "When should I cull hens?"],
    """
Signs of a laying hen: red, moist comb; large, moist vent; wide gap between the pelvic bones (about three fingers); soft abdomen.
Signs of a non-laying hen: pale, shrunken comb; small, dry vent; narrow pelvic bones (one or two fingers); yellow beak and shanks returning.
Cull non-layers, sick birds, and very old hens to save feed. Many farms replace layer flocks at about 72 to 80 weeks of age.
""")

# ---------------------------------------------------------------- NATIVE AND FREE-RANGE
add("native-chicken", "native", "Native and free-range", "Philippine native chickens",
    ["native", "darag", "banaba", "paraoakan", "joloano", "bolinao", "camarines", "strains", "upgraded", "philippine"],
    ["What are the Philippine native chicken breeds?", "Is raising native chicken profitable?"],
    """
Philippine native chickens are hardy, tolerate heat and disease better than commercial strains, and fetch higher prices per kilo.
Recognized strains include Darag (Western Visayas), Banaba (Batangas), Paraoakan (Palawan), Camarines, Bolinao, and Joloano.
Under backyard conditions they grow slowly (about 4 to 6 months to market) and lay about 40 to 60 eggs a year, but improved feeding, housing, and selection can raise both.
Upgraded or colored breeds (for example Sasso or Kabir) grow faster while keeping a native-like look and taste.
""")

add("free-range", "native", "Native and free-range", "Free-range and range-fed systems",
    ["free range", "free-range", "range", "pasture", "forage", "roam", "organic", "natural", "outdoor"],
    ["How do I raise free-range chickens?", "What is the difference between free-range and organic?"],
    """
In a free-range system, birds have a house for night, laying, and shelter, plus fenced outdoor range by day.
- Provide shade, shelter from rain, and protection from predators.
- Range gives grass, insects, and exercise, but birds still need supplemental feed for good growth and laying.
- Rotate the range area to reduce parasites, and deworm as your veterinarian advises.
"Organic" products sold as such must follow organic standards and certification under Philippine law, which covers feed, medicines, and records.
""")

add("local-feeds", "feed", "Feeds", "Alternative and local feed ingredients",
    ["alternative", "local", "cheap", "homemade", "rice bran", "darak", "copra", "azolla", "insects", "larvae", "bsf", "kangkong", "ipil-ipil", "trichanthera", "madre de agua", "reduce feed cost"],
    ["What cheap local feeds can I give chickens?", "Can I make my own chicken feed?"],
    """
Local ingredients can lower feed cost, especially for native and free-range chickens:
- Energy: corn, rice bran (darak or tahop), cassava (dried, in moderation).
- Protein: soybean meal, fish meal, black soldier fly larvae, earthworms.
- Leaf meals and greens: azolla, kangkong, madre de agua (trichanthera), malunggay. Ipil-ipil leaves only in small amounts, because they contain mimosine.
- Copra meal in moderate amounts.
A home-mixed ration must still be balanced for protein, energy, calcium, and phosphorus. Fast-growing broilers and commercial layers perform poorly on unbalanced mixes, so compare costs per kilo of meat or per egg, not per sack.
""")

add("feed-storage", "feed", "Feeds", "Storing feed and avoiding mold",
    ["store", "storage", "stored", "mold", "moldy", "aflatoxin", "sack", "expire", "old feed", "damp", "spoiled", "shelf life", "how long"],
    ["How do I store chicken feed?", "Can I give moldy feed to chickens?"],
    """
- Store sacks off the floor on pallets, away from walls, in a dry, shaded, rat-proof room.
- Use feed within about a month of the manufacturing date and use old stock first.
- Never feed moldy, caked, or sour-smelling feed. Molds can produce aflatoxins that cause poor growth, liver damage, low egg production, and deaths.
- Keep feeders and drinkers clean, and do not let feed get wet in the feeders.
""")

add("water", "feed", "Feeds", "Water needs",
    ["water", "drink", "drinker", "drinking", "how much water", "nipple", "clean"],
    ["How much water do chickens drink?", "How do I keep drinking water clean?"],
    """
Chickens drink about twice as much water as the feed they eat, and up to three or four times as much in hot weather.
- Water must never run out. Even a few hours without water lowers growth and egg production.
- Clean drinkers daily and keep water cool and shaded.
- Use clean, safe water. Have well water tested if birds do poorly.
- A sudden drop in water intake is often the first sign of disease.
""")

# ---------------------------------------------------------------- HOUSING
add("housing", "housing", "Housing", "Poultry house design",
    ["house", "housing", "coop", "building", "design", "construct", "orientation", "roof", "cage", "shed", "pen"],
    ["How should I build a chicken house?", "What is the best design for a poultry house?"],
    """
Basics for open-sided houses in the tropics:
- Orient the long axis east to west, so the sun does not shine directly into the house.
- Raise the floor or site above flood level, with good drainage.
- Use a high roof with overhangs and, ideally, a ridge vent to release hot air.
- Wire mesh sides for airflow, with curtains to block rain and wind.
- Keep out rats, snakes, dogs, and wild birds, which carry disease.
- Leave space between houses and keep them away from homes and water sources.
""")

add("litter", "housing", "Housing", "Litter and wet litter",
    ["litter", "bedding", "rice hull", "wet", "wet litter", "ammonia", "smell", "floor", "sawdust", "fix"],
    ["What bedding should I use for chickens?", "How do I control ammonia smell?"],
    """
- Common litter: rice hull (about 5 to 8 cm deep), wood shavings, or sawdust.
- Wet, caked litter causes ammonia, footpad sores, breast blisters, and coccidiosis.
Keep litter dry by fixing leaking drinkers, improving ventilation, not overcrowding, and turning or replacing wet spots.
A strong ammonia smell at bird level means ventilation is not enough and harms the birds' lungs and eyes.
""")

add("heat-stress", "health", "Health", "Heat stress",
    ["heat", "hot", "heat stress", "panting", "summer", "temperature", "dying from heat", "cool", "weather", "prevent"],
    ["How do I protect chickens from heat?", "Why are my chickens panting?"],
    """
Signs: panting with open beak, wings held out, less eating, more drinking, lower egg production, and deaths in hot afternoons, often the heaviest birds first.
What to do:
- Improve airflow with fans, open sides, and shade around the house. Wet the roof or use sprinklers on the roof in extreme heat.
- Give cool, clean water and add more drinkers.
- Feed during cooler hours (early morning and night) and avoid handling birds at midday.
- Electrolytes and vitamin C in the water can help during hot spells.
- Reduce stocking density.
""")

# ---------------------------------------------------------------- HEALTH AND BIOSECURITY
add("biosecurity", "health", "Health", "Biosecurity",
    ["biosecurity", "prevent", "prevention", "disease", "diseases", "visitors", "footbath", "disinfect", "protect", "spread", "keep out"],
    ["How do I prevent diseases in my farm?", "What is biosecurity?"],
    """
Biosecurity means keeping diseases out of the farm and stopping them from spreading:
- Limit visitors. Use a footbath and clean boots or footwear for each house.
- Buy chicks only from trusted, vaccinated sources. Keep new or returning birds separate for 2 to 3 weeks.
- Keep wild birds, rats, dogs, and cats away from birds and feed.
- Do not mix ages or species, such as ducks with chickens.
- All-in, all-out: clean, disinfect, and rest the house between batches.
- Dispose of dead birds properly and quickly.
Biosecurity is cheaper than any treatment.
""")

add("vaccination", "health", "Health", "Vaccination program",
    ["vaccine", "vaccination", "vaccinate", "schedule", "program", "when", "newcastle", "gumboro", "ib", "pox", "marek"],
    ["What is the vaccination schedule for chickens?", "When should I vaccinate my broilers?"],
    """
Vaccination programs depend on the local disease situation, so follow your veterinarian, hatchery, or vaccine supplier. A common example:
- Day 1 (hatchery): Marek's disease, mainly for layers and breeders.
- Day 7 to 10: Newcastle disease and infectious bronchitis (eye or nose drop, or drinking water).
- Day 12 to 16: infectious bursal disease (Gumboro).
- Day 18 to 28: Newcastle disease booster.
- Layers and native chickens: fowl pox (wing web) at about 6 to 8 weeks, plus further Newcastle and other boosters before lay.
Store vaccines cold, use them within the time on the label, vaccinate only healthy birds, and keep records.
""")

add("vaccine-handling", "health", "Health", "Giving vaccines properly",
    ["vaccine", "drinking water", "eye drop", "mix vaccine", "chlorine", "skim milk", "storage", "cold", "failure", "failed", "fail", "vaccination failed"],
    ["How do I give vaccine through drinking water?", "Why did my vaccine not work?"],
    """
- Keep vaccines in the refrigerator (2 to 8 °C) and carry them in an ice box.
- For drinking-water vaccines: use clean water without chlorine, withhold water for about 1 to 2 hours first so birds are thirsty, add a vaccine stabilizer or skim milk as the label directs, and make sure all birds drink within about 1 to 2 hours.
- For eye or nose drops: one drop per bird, and wait until it is absorbed.
- Mix only what you will use immediately and discard leftovers properly.
Vaccines fail when they get warm, are mixed with chlorinated water, are given to sick birds, or do not reach every bird. Follow the product label exactly.
""")

add("newcastle", "health", "Diseases", "Newcastle disease",
    ["newcastle", "nd", "twisted neck", "torticollis", "green", "diarrhea", "paralysis", "sudden death", "outbreak", "neck", "twisted"],
    ["What are the signs of Newcastle disease?", "My chickens have twisted necks, what is it?"],
    """
Newcastle disease (often called "peste" by farmers) is a severe viral disease.
Signs: sudden deaths, gasping and coughing, greenish watery droppings, twisted neck, paralysis, swollen face, and a sharp drop in eggs.
There is no cure. Prevention is vaccination plus biosecurity.
If you suspect it:
- Isolate the flock, stop all bird movement and sales, and limit visitors.
- Report to your municipal agriculturist or provincial veterinarian right away. It is a reportable disease.
""" + VET)

add("avian-flu", "health", "Diseases", "Avian influenza (bird flu)",
    ["bird flu", "avian influenza", "influenza", "ai", "h5n1", "swollen head", "purple comb", "high mortality", "report"],
    ["What are the signs of bird flu?", "What do I do if I suspect bird flu?"],
    """
Highly pathogenic avian influenza (bird flu) is a notifiable disease that can kill most of a flock in days and can, rarely, infect people.
Signs: sudden high deaths, swollen head, comb, and wattles, purple or blue comb and legs, bleeding spots on the legs, a sharp drop in eggs, and nervous signs.
If you suspect it:
- Do not move, sell, eat, or give away birds or eggs from the farm.
- Keep people out and wear gloves and a mask when handling birds.
- Report immediately to your municipal agriculturist, provincial veterinarian, or the Bureau of Animal Industry.
""" + VET)

add("coccidiosis", "health", "Diseases", "Coccidiosis (bloody droppings)",
    ["coccidiosis", "cocci", "bloody", "blood", "droppings", "poop", "stool", "diarrhea", "wet litter"],
    ["Why are my chickens passing bloody droppings?", "How do I prevent coccidiosis?"],
    """
Coccidiosis is caused by parasites in the gut and is common in birds on litter, usually from about 3 to 6 weeks of age.
Signs: bloody or mucous droppings, ruffled feathers, hunched birds, poor growth, and deaths.
Prevention:
- Keep litter dry and drinkers from leaking.
- Use feed with an anticoccidial or a coccidiosis vaccine, as your supplier or veterinarian advises.
Treatment uses anticoccidial drugs in the drinking water. Ask a veterinarian for the right product and dose, and observe the withdrawal period.
""")

add("coryza", "health", "Diseases", "Infectious coryza (swollen face)",
    ["coryza", "swollen face", "swollen eyes", "nasal discharge", "bad smell", "colds", "runny nose", "face", "wattles", "swollen"],
    ["Why are my chickens' faces swollen?", "My chickens have colds and a smelly discharge"],
    """
Infectious coryza is a bacterial disease of the respiratory tract.
Signs: swollen face and eyes, sticky, foul-smelling discharge from the nose, sneezing, lower feed intake, and a drop in eggs.
- Separate sick birds and improve ventilation.
- Treatment with antibiotics needs a veterinarian's prescription. Recovered birds can remain carriers, so do not mix them with new birds.
- Vaccines exist for farms with repeated outbreaks. Practice all-in, all-out to break the cycle.
""")

add("respiratory", "health", "Diseases", "Coughing and breathing problems",
    ["cough", "coughing", "sneezing", "breathing", "respiratory", "gasping", "rattling", "crd", "mycoplasma", "bronchitis", "colds"],
    ["Why are my chickens coughing?", "My chickens are sneezing and have rattling breath"],
    """
Coughing, sneezing, rattling, or gasping can come from several causes:
- Infections: Newcastle disease, infectious bronchitis, chronic respiratory disease (mycoplasma), coryza, and others.
- Environment: ammonia from wet litter, dust, and poor ventilation make all of these worse.
Improve ventilation and litter first, and isolate sick birds. A diagnosis needs a veterinarian, often with laboratory tests, because the right action differs by disease. If many birds die suddenly, treat it as possible Newcastle disease or bird flu and report it.
""")

add("gumboro", "health", "Diseases", "Gumboro (infectious bursal disease)",
    ["gumboro", "ibd", "bursal", "bursa", "watery", "white diarrhea", "3 to 6 weeks", "immune"],
    ["What is Gumboro disease?", "Why are my 4-week-old broilers dying with watery droppings?"],
    """
Infectious bursal disease (Gumboro) is a viral disease of young chickens, usually 3 to 6 weeks old.
Signs: sudden illness, whitish watery droppings, ruffled feathers, trembling, pecking at the vent, and deaths that peak and then fall within about a week.
It also weakens the immune system, so other vaccines and treatments work less well afterward.
There is no cure. Prevention is vaccination at the right age, plus thorough cleaning between batches.
""" + VET)

add("fowl-pox", "health", "Diseases", "Fowl pox",
    ["pox", "fowl pox", "scabs", "warts", "comb", "wattles", "lesions", "mosquito", "bumps"],
    ["What are the scabs on my chicken's comb?", "How do I prevent fowl pox?"],
    """
Fowl pox is a viral disease spread mainly by mosquitoes and contact.
Signs: wart-like scabs on the comb, wattles, face, and legs (dry form), or yellow patches in the mouth and throat that make eating and breathing hard (wet form).
- Prevention: wing-web vaccination of layers and native chickens, plus mosquito control.
- There is no cure. Isolate affected birds and give them soft feed and water. Most birds with the dry form recover in a few weeks.
""")

add("worms", "health", "Diseases", "Worms and deworming",
    ["worms", "worm", "deworm", "deworming", "dewormer", "roundworm", "tapeworm", "parasites", "internal", "often", "purga", "purge"],
    ["How often should I deworm chickens?", "Do my chickens have worms?"],
    """
Signs of worms: weight loss, poor growth, pale combs, lower egg production, and sometimes worms seen in droppings.
Free-range and native chickens on soil are most at risk. Broilers kept on fresh litter for a short cycle rarely need deworming.
- Deworm on a schedule your veterinarian recommends, often every 2 to 3 months for range birds.
- Use a dewormer labeled for poultry, follow the label dose, and observe the egg and meat withdrawal period.
- Rotate the range and keep the area dry.
""")

add("mites-lice", "health", "Diseases", "Mites and lice",
    ["mites", "lice", "red mites", "external parasites", "itching", "scratching", "pale comb", "bugs", "fleas", "tiny", "get rid", "treat"],
    ["How do I get rid of mites on chickens?", "My chickens have lice"],
    """
Signs: restlessness, feather damage, scabby skin, pale combs from blood loss, and lower egg production. Red mites hide in cracks and bite at night.
- Inspect under the wings and around the vent, and check perches and nests at night.
- Clean and treat the house, nests, and perches, not just the birds.
- Use a product labeled for poultry and follow the label, including egg and meat withdrawal periods. Repeat as the label directs to kill newly hatched parasites.
- A dust bath area with dry soil helps birds keep themselves clean.
""")

add("sudden-death", "health", "Diseases", "Many birds dying suddenly",
    ["sudden", "dying", "many", "dead", "deaths", "mortality", "die", "overnight", "high mortality", "emergency"],
    ["Many of my chickens died overnight, what should I do?", "What causes sudden deaths in chickens?"],
    """
Sudden deaths of many birds are an emergency.
Possible causes include Newcastle disease, avian influenza, heat stroke, poisoning (moldy feed, chemicals), suffocation from piling, and predators.
What to do now:
- Stop moving, selling, or eating birds and eggs from the farm.
- Keep visitors out and isolate the affected house.
- Record the number of deaths, ages, and signs. Keep a few fresh dead birds chilled (not frozen) for examination.
- Call your municipal agriculturist or provincial veterinarian immediately.
""")

add("medication", "health", "Health", "Antibiotics and medicines",
    ["antibiotic", "antibiotics", "medicine", "medication", "drug", "treatment", "dose", "dosage", "cure"],
    ["What antibiotic should I give my chickens?", "What medicine is good for sick chickens?"],
    """
I can't recommend a specific drug or dose, because the right treatment depends on a correct diagnosis.
- Use antibiotics only when a veterinarian confirms a bacterial infection. They do not cure viral diseases like Newcastle disease, bird flu, or Gumboro.
- Follow the label dose and the full treatment period.
- Observe the withdrawal period before selling or eating meat and eggs.
- Misusing antibiotics creates resistant bacteria that harm both animals and people.
""" + VET)

add("withdrawal", "health", "Health", "Withdrawal period for meat and eggs",
    ["withdrawal", "residue", "safe to eat", "after treatment", "eat eggs", "on antibiotics", "treated", "medicated", "how long"],
    ["Can I sell eggs while my hens are on medicine?", "How long before I can eat treated chickens?"],
    """
The withdrawal period is the time after the last dose of a drug before meat or eggs are safe to eat or sell, because drug residues remain in the body.
- Each product has its own withdrawal period printed on its label. Some products must not be used in laying hens at all.
- Do not sell or eat meat or eggs during this period.
- Write down the product, date of last dose, and the date the withdrawal ends in your records.
""")

add("dead-birds", "health", "Health", "Disposing of dead birds",
    ["dispose", "disposal", "dead", "bury", "burial", "carcass", "mortality", "throw", "burn"],
    ["How do I dispose of dead chickens?", "Where should I bury dead birds?"],
    """
- Remove dead birds every day.
- Bury them in a pit at least about 1 meter deep, covered with lime and soil, away from wells, rivers, and houses. Incineration or composting are other options.
- Never throw carcasses into rivers or fields, feed them to other animals, or sell them.
- If many birds die suddenly, do not dispose of them yet. Call the veterinary office first, since samples may be needed.
""")

add("vet-help", "health", "Health", "When and where to get veterinary help",
    ["veterinarian", "vet", "doctor", "help", "office", "agriculturist", "where", "who", "contact", "bai", "laboratory", "diagnosis", "sick", "check", "report"],
    ["Where can I get help for my sick chickens?", "Who do I call if my chickens are sick?"],
    """
Get help early when you see sudden deaths, a sharp drop in eggs or feed intake, many sick birds, or signs you cannot explain.
Where to go:
- Your municipal agriculture office (municipal agriculturist).
- The provincial veterinary office.
- Regional animal disease diagnostic laboratories of the Department of Agriculture for tests.
- The Bureau of Animal Industry for reportable diseases such as avian influenza.
- Private poultry veterinarians and feed or vaccine company technical staff.
Bring your records and, if asked, fresh dead or sick birds for examination.
""")

# ---------------------------------------------------------------- INCUBATION
add("incubation", "incubation", "Incubation", "Incubating and hatching eggs",
    ["incubate", "incubation", "incubator", "hatch", "hatching", "temperature", "humidity", "turn", "turning", "days", "fertile"],
    ["How do I incubate chicken eggs?", "What temperature and humidity for an incubator?"],
    """
Typical settings for chicken eggs in a forced-air incubator:
- Temperature: about 37.5 to 37.8 °C.
- Humidity: about 50 to 55% for days 1 to 18, then about 65 to 70% for hatching.
- Turning: at least 3 to 5 times a day (an odd number) until day 18, then stop.
- Chicken eggs hatch in about 21 days.
Use clean, fertile eggs no more than about 7 days old, stored cool and pointed end down. Follow your incubator's manual, since still-air models need a slightly higher temperature.
""")

add("hatch-days", "incubation", "Incubation", "Hatching times by species",
    ["how many days", "days", "day", "hatch", "duck", "quail", "turkey", "muscovy", "goose", "chicken", "incubation period", "itik", "pato", "pugo"],
    ["How many days do duck eggs take to hatch?", "How long do quail eggs take to hatch?"],
    """
Approximate incubation periods:
- Chicken: 21 days
- Quail: 17 to 18 days
- Duck (Pateros and most ducks): 28 days
- Muscovy duck (pato): about 35 days
- Turkey: 28 days
- Goose: about 28 to 32 days
""")

add("candling", "incubation", "Incubation", "Candling eggs",
    ["candling", "candle", "check", "fertile", "infertile", "clear", "veins", "embryo", "light", "alive"],
    ["How do I candle eggs?", "How do I know if an egg is fertile?"],
    """
Candling means shining a bright light through the egg in a dark room.
- Around day 7: a fertile egg shows a dark spot with spidery blood vessels. A clear egg is infertile and can be removed.
- A blood ring or dark, cloudy egg means an early dead embryo; remove it before it spoils.
- Around day 18: most of the egg is dark and the air cell is larger.
Candle quickly and gently so eggs do not cool down.
""")

add("poor-hatch", "incubation", "Incubation", "Poor hatching results",
    ["poor hatch", "low hatch", "didn't hatch", "not hatching", "dead in shell", "failed", "hatchability", "pipped", "inside the shell", "hatch", "not"],
    ["Why did my eggs not hatch?", "Why are chicks dying in the shell?"],
    """
Common causes of poor hatching:
- Infertile eggs: too few roosters, old roosters, or eggs stored too long or too warm.
- Wrong temperature: even a small error over many days kills embryos. Check with a second thermometer.
- Wrong humidity: too low makes chicks stick to the shell; too high makes weak, wet chicks.
- Not turning eggs, or turning after day 18.
- Dirty or cracked eggs, and power interruptions.
Open unhatched eggs to see at which stage embryos died, which points to the cause.
""")

# ---------------------------------------------------------------- DUCKS AND QUAIL
add("ducks", "other-birds", "Ducks and quail", "Raising ducks",
    ["duck", "ducks", "itik", "pato", "pateros", "muscovy", "mallard", "balut", "penoy", "salted"],
    ["How do I raise ducks?", "What is the difference between itik and pato?"],
    """
- Itik (Philippine mallard, including the Pateros type) are raised mainly for eggs used for balut, penoy, and salted eggs. Good layers can produce about 200 or more eggs a year with proper feeding.
- Pato (Muscovy duck) is raised mainly for meat and is hardy and good at foraging.
Ducks need clean drinking water deep enough to dip their heads, but they do not need a swimming pond. Keep their housing dry, since wet bedding causes disease. Keep ducks separate from chickens.
""")

add("balut", "other-birds", "Ducks and quail", "Balut and penoy production",
    ["balut", "penoy", "duck egg", "incubate", "days", "fertile", "process", "make"],
    ["How many days to make balut?", "What is the difference between balut and penoy?"],
    """
- Balut is a fertile duck egg incubated for about 16 to 18 days and then boiled.
- Penoy is an egg that turned out infertile or did not develop (found by candling), boiled and sold separately.
Producers incubate fertile itik eggs, candle them to sort out the infertile ones for penoy, and boil the developing eggs at the target age. Clean handling and quick sale are important for food safety.
""")

add("quail", "other-birds", "Ducks and quail", "Raising quail",
    ["quail", "pugo", "quail eggs", "cage", "raise", "how many eggs"],
    ["How do I raise quail?", "How many eggs does a quail lay?"],
    """
Quail (pugo) need little space and start laying at about 6 to 7 weeks of age.
- A good laying quail can produce about 250 to 300 eggs a year.
- They are usually kept in tiered cages, with layer-type feed high in protein (about 20 to 24%).
- They need about 14 to 16 hours of light a day to keep laying.
- Quail eggs hatch in about 17 to 18 days.
Keep the house well ventilated and clean, and protect quail from rats and snakes.
""")

# ---------------------------------------------------------------- BREEDS
add("breeds", "general", "Getting started", "Choosing a breed",
    ["breed", "breeds", "best", "which", "choose", "kind", "type", "strain", "rhode island", "australorp", "sasso", "kabir", "cobb", "ross", "most eggs"],
    ["What is the best chicken breed to raise?", "Which breed lays the most eggs?"],
    """
Choose by purpose and system:
- Fast meat in confinement: commercial broilers (Cobb, Ross, and similar), about 30 to 40 days.
- Most eggs in confinement: commercial layer hybrids (Hy-Line, Lohmann, Dekalb, and similar).
- Free-range meat with higher prices: Philippine native strains or colored, slower-growing breeds such as Sasso or Kabir.
- Dual-purpose for backyards: Rhode Island Red, Black Australorp, and crosses with native chickens.
Commercial hybrids need good feed and housing to perform; native and dual-purpose birds tolerate simpler conditions.
""")

# ---------------------------------------------------------------- FOOD SAFETY AND PRODUCTS
add("egg-handling", "food-safety", "Food safety", "Handling and storing eggs",
    ["egg", "eggs", "store", "storage", "wash", "washing", "clean", "dirty", "fresh", "shelf life", "refrigerate", "fridge", "last", "room temperature", "how long"],
    ["Should I wash eggs?", "How long can eggs be stored?"],
    """
- Collect eggs at least twice a day and keep nests clean to reduce dirty eggs.
- Do not wash eggs that will be stored, unless they are dirty. If you must wash, use water warmer than the egg and dry them at once. Cold water can pull bacteria through the shell.
- Store eggs pointed end down in a cool place. At room temperature in a hot climate, use or sell within about 1 to 2 weeks; refrigerated eggs keep several weeks.
- Do not sell cracked or very dirty eggs as table eggs.
""")

add("egg-grading", "food-safety", "Food safety", "Egg sizes and quality",
    ["size", "sizes", "grade", "grading", "small", "large", "jumbo", "peewee", "weight", "double yolk", "blood spot", "quality"],
    ["Why are my eggs small?", "What causes blood spots in eggs?"],
    """
- Egg size increases with hen age: young hens lay small (pullet) eggs, and size rises over the first months of lay. Underweight pullets and low-protein feed also give small eggs.
- Eggs are sold by weight class, from small to jumbo.
- Double yolks are common in young hens starting to lay.
- Small blood or meat spots are harmless and come from tiny bleeds during egg formation; candling removes them for sale.
""")

add("slaughter", "food-safety", "Food safety", "Dressing and selling chicken meat",
    ["slaughter", "dress", "dressing", "butcher", "kill", "sell meat", "dressed chicken", "nmis", "meat", "processing"],
    ["How do I dress chickens for sale?", "Do I need a permit to sell dressed chicken?"],
    """
- Remove feed about 8 to 10 hours before slaughter (keep water available) so the gut is empty and the carcass stays clean.
- Slaughter and dress in a clean area with clean water, chill the carcass quickly, and keep it cold until sale.
- Never slaughter birds that are sick or still within a drug withdrawal period.
- Meat sold commercially in the Philippines generally must come from an accredited slaughterhouse or dressing plant under the National Meat Inspection Service (NMIS). Check with NMIS or your local government for the rules that apply to your scale.
""")

add("manure", "business", "Business", "Using chicken manure",
    ["manure", "dung", "droppings", "fertilizer", "compost", "waste", "smell", "flies"],
    ["Can I use chicken manure as fertilizer?", "How do I manage chicken manure?"],
    """
Chicken manure is a valuable fertilizer, rich in nitrogen and phosphorus, and can be sold as an extra income source.
- Compost it before use: piled and turned, it heats up, which kills many germs and weed seeds and reduces smell.
- Fresh manure can burn plants and carry disease.
- Keep manure dry and covered to control flies and smell, and away from water sources and neighbors.
""")

# ---------------------------------------------------------------- BUSINESS
add("cost-profit", "business", "Business", "Costs and profit of a broiler batch",
    ["cost", "costs", "profit", "income", "capital", "budget", "expenses", "return", "profitable", "how much money"],
    ["How much capital do I need for 100 broilers?", "Is broiler raising profitable?"],
    """
Main costs per batch:
- Feed: usually the largest cost, often 60 to 70% of the total.
- Chicks, vaccines and medicines, brooding fuel or electricity, litter, labor, and house depreciation.
To estimate profit:
- Income = birds sold × average live weight × price per kg.
- Profit = income minus all costs.
- Example method: if 100 chicks are placed and 96 are sold at 1.8 kg, 172.8 kg are sold; multiply by the local price per kg.
Prices for chicks, feed, and live birds change often, so check current local prices before planning. Mortality, FCR, and selling price decide whether a batch makes money.
""")

add("contract-growing", "business", "Business", "Contract growing with integrators",
    ["contract", "contract growing", "integrator", "grower", "partner", "san miguel", "company", "growers fee", "tie-up"],
    ["What is contract growing for broilers?", "How do I partner with a poultry company?"],
    """
In contract growing, an integrator company supplies chicks, feed, vaccines, and technical support, while the grower provides the house, equipment, labor, utilities, and management.
- The grower is paid a fee per bird or per kilo, often with bonuses or deductions based on mortality and feed conversion.
- Integrators usually require a minimum house size and specific equipment, sometimes closed tunnel-ventilated houses.
- Read the contract carefully: who carries the risk of disease losses, payment terms, and the minimum number of batches.
""")

add("permits", "business", "Business", "Permits and registration",
    ["permit", "permits", "license", "registration", "register", "legal", "business permit", "ecc", "requirements", "bai", "lgu"],
    ["What permits do I need for a poultry farm?", "Do I need to register my poultry farm?"],
    """
Requirements depend on farm size and location. Commonly:
- Barangay clearance and a mayor's or business permit from the local government.
- Compliance with local zoning and distance rules from homes and water sources.
- Registration of the farm with the Bureau of Animal Industry, especially for commercial farms.
- Larger farms may need an Environmental Compliance Certificate from the DENR Environmental Management Bureau.
- Business name registration with DTI and tax registration with BIR when operating as a business.
Ask your municipal agriculture office and LGU for the exact list for your scale.
""")

add("marketing", "business", "Business", "Selling eggs and chickens",
    ["sell", "selling", "market", "marketing", "buyers", "customers", "price", "where to sell"],
    ["Where can I sell my eggs?", "How do I find buyers for my chickens?"],
    """
Options for selling poultry products:
- Direct to households, sari-sari stores, carinderias, bakeries, and restaurants.
- Public market vendors and egg or chicken traders.
- Online selling through community groups.
- Cooperatives and farmers' associations that pool products for bigger buyers.
- Contract growing or supply agreements for steady volume.
Consistent supply, clean and graded products, and reliable delivery keep buyers. Native and free-range chicken and eggs can command higher prices when their origin is explained.
""")

add("feed-cost-reduce", "feed", "Feeds", "Reducing feed cost and waste",
    ["reduce", "lower", "save", "feed cost", "wastage", "waste", "expensive feed", "cheaper", "efficient"],
    ["How can I reduce feed costs?", "How do I stop feed wastage?"],
    """
Ways to lower feed cost without hurting performance:
- Stop wastage: fill feeders only about one-third full and keep the feeder lip at the height of the birds' backs.
- Keep birds healthy and comfortable, since sick or heat-stressed birds convert feed poorly.
- Sell broilers at the right age; keeping them longer raises the FCR.
- Cull non-laying hens.
- Store feed properly to prevent spoilage and rats.
- For native and free-range birds, add forage and local ingredients (ask me about local feeds).
""")

add("predators", "housing", "Housing", "Protecting chickens from predators",
    ["predator", "predators", "rat", "rats", "snake", "snakes", "dog", "cat", "hawk", "missing", "stolen", "civet", "eaten", "eating", "killed", "killing", "getting into", "chick", "chicks"],
    ["How do I protect chickens from rats and snakes?", "Something is killing my chickens at night"],
    """
- Rats eat feed, kill chicks, and spread disease: use rat-proof storage, close holes, keep grass short around the house, and set traps or bait stations out of reach of chickens and pets.
- Snakes and civets: close gaps larger than about 2 cm with fine wire mesh, especially in brooders, and lock birds in at night.
- Dogs: use solid fencing.
- Hawks: provide cover or netting over runs.
Count birds every evening so losses are noticed early.
""")

# ---------------------------------------------------------------- LOCAL RESEARCH (markdown packs)
import sys  # noqa: E402
sys.path.insert(0, str(Path(__file__).parent))
from ingest_md import load_all  # noqa: E402

PACKS, MD_ENTRIES = load_all()
E += MD_ENTRIES
dupes = {e["id"] for e in E if sum(x["id"] == e["id"] for x in E) > 1}
assert not dupes, f"duplicate entry ids: {dupes}"

kb = dict(name="PoultryBot KB", verified=VERIFIED, sources=[{k: v for k, v in p.items()} for p in PACKS], entries=E)
out = Path(__file__).parent / "kb.json"
out.write_text(json.dumps(kb, ensure_ascii=False, indent=1), encoding="utf-8")
if __name__ == "__main__":
    from collections import Counter
    print(len(E), "entries", dict(Counter(e["group"] for e in E)))
