from production import IF, THEN, AND

# Classic MIT 6.034 "zookeeper" rules (trimmed but enough to test properly)
zookeeper_rules = [
    IF('(?x) has hair', THEN('(?x) is a mammal')),
    IF('(?x) gives milk', THEN('(?x) is a mammal')),

    IF(AND(['(?x) is a mammal', '(?x) eats meat']), THEN('(?x) is a carnivore')),
    IF(AND(['(?x) is a mammal', '(?x) has pointed teeth', '(?x) has claws', '(?x) has forward-pointing eyes']),
       THEN('(?x) is a carnivore')),

    IF(AND(['(?x) is a mammal', '(?x) has hoofs']), THEN('(?x) is an ungulate')),
    IF(AND(['(?x) is a mammal', '(?x) chews cud']), THEN('(?x) is an ungulate')),

    IF(AND(['(?x) is a carnivore', '(?x) has tawny color', '(?x) has dark spots']),
       THEN('(?x) is a cheetah')),
    IF(AND(['(?x) is a carnivore', '(?x) has tawny color', '(?x) has black stripes']),
       THEN('(?x) is a tiger')),

    IF(AND(['(?x) is an ungulate', '(?x) has long legs', '(?x) has long neck', '(?x) has tawny color', '(?x) has dark spots']),
       THEN('(?x) is a giraffe')),
    IF(AND(['(?x) is an ungulate', '(?x) has black stripes']),
       THEN('(?x) is a zebra')),

    IF(AND(['(?x) is a bird', '(?x) does not fly', '(?x) has long legs', '(?x) has long neck', '(?x) is black and white']),
       THEN('(?x) is an ostrich')),
    IF(AND(['(?x) is a bird', '(?x) does not fly', '(?x) swims', '(?x) is black and white']),
       THEN('(?x) is a penguin')),
    IF(AND(['(?x) is a bird', '(?x) is a good flyer']),
       THEN('(?x) is an albatross')),

    IF('(?x) has feathers', THEN('(?x) is a bird')),
    IF('(?x) flies', THEN('(?x) is a bird')),
    IF(AND(['(?x) lays eggs', '(?x) is a bird']), THEN('(?x) is an egg-layer')),
]