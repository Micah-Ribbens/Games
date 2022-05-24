import random
import pygame

from base.colors import *
from base.dimensions import Dimensions
from base.important_variables import screen_height, screen_length
from base.utility_functions import get_uppercase, get_sublist, remove_index
from base.velocity_calculator import VelocityCalculator
from gui_components.card import Card
from gui_components.grid import Grid
from gui_components.intermediate_screens import IntermediateScreens
from gui_components.text_box import TextBox
from base.utility_functions import string_to_list

from games.minigames.card_games.word_game import WordGame
from utillities.animation import Animation


class Wordle(WordGame):
    """Wordle- the best word game ever"""

    max_guesses = 7
    word_length = 5
    current_guess = 1
    current_index = 0
    round_number = 1
    typed_letters = ""
    words = ['aaron', 'aback', 'abaft', 'abase', 'abash', 'abate', 'abbey', 'abbot', 'abeam', 'abele', 'abets', 'abhor', 'abide', 'abies', 'abler', 'abode', 'abomb', 'abort', 'about', 'above', 'abuse', 'abuzz', 'abyss', 'accra', 'acers', 'ached', 'aches', 'acids', 'acorn', 'acres', 'acrid', 'acted', 'actor', 'acute', 'adage', 'adapt', 'added', 'adder', 'addle', 'adept', 'adhoc', 'adieu', 'adios', 'adlib', 'adman', 'admen', 'admin', 'admit', 'admix', 'adobe', 'adopt', 'adore', 'adorn', 'adult', 'aegis', 'aeons', 'aesop', 'affix', 'afire', 'afoot', 'afros', 'after', 'again', 'agape', 'agave', 'agent', 'agile', 'aging', 'aglow', 'agony', 'agora', 'agree', 'ahead', 'aided', 'aider', 'aides', 'aimed', 'aimer', 'aired', 'aisle', 'alack', 'alarm', 'album', 'alder', 'alert', 'algae', 'algal', 'alias', 'alibi', 'alien', 'align', 'alike', 'aline', 'alive', 'alkyl', 'allay', 'alley', 'allot', 'allow', 'alloy', 'aloes', 'aloft', 'aloha', 'alone', 'along', 'aloof', 'aloud', 'alpha', 'altar', 'alter', 'amass', 'amaze', 'amber', 'ambit', 'amble', 'amend', 'amens', 'amide', 'amigo', 'amine', 'amino', 'amiss', 'amity', 'amman', 'among', 'amour', 'ample', 'amply', 'amuck', 'amuse', 'andes', 'angel', 'anger', 'angle', 'angry', 'angst', 'anion', 'anise', 'ankle', 'annal', 'annex', 'annoy', 'annul', 'anode', 'antic', 'anvil', 'aorta', 'apace', 'apart', 'apery', 'aphid', 'apian', 'aping', 'apish', 'apnea', 'appal', 'apple', 'apply', 'appro', 'april', 'apron', 'apses', 'apsis', 'aptly', 'arabs', 'araks', 'arbor', 'arced', 'areal', 'areas', 'arena', 'arent', 'argon', 'argot', 'argue', 'argus', 'arias', 'arise', 'armed', 'aroma', 'arose', 'array', 'arrow', 'arson', 'ashen', 'ashes', 'asian', 'aside', 'asked', 'askew', 'aspic', 'assay', 'asses', 'asset', 'aster', 'astir', 'aswan', 'atlas', 'atoll', 'atoms', 'atone', 'attic', 'audio', 'audit', 'auger', 'augur', 'aunts', 'aural', 'auras', 'auric', 'avail', 'avens', 'avers', 'avert', 'avian', 'avoid', 'await', 'awake', 'award', 'aware', 'awash', 'awful', 'awoke', 'axial', 'axing', 'axiom', 'axles', 'axons', 'aztec', 'azure', 'babas', 'babel', 'babes', 'backs', 'bacon', 'baddy', 'bader', 'badge', 'badly', 'baggy', 'bails', 'baits', 'baked', 'baker', 'bakes', 'baldy', 'baled', 'bales', 'balls', 'balms', 'balmy', 'balsa', 'banal', 'bands', 'bangs', 'banjo', 'banks', 'banns', 'barbs', 'bards', 'bared', 'barer', 'bares', 'barge', 'barks', 'barky', 'barns', 'baron', 'barre', 'basal', 'based', 'baser', 'bases', 'basic', 'basil', 'basin', 'basis', 'basks', 'baste', 'batch', 'bated', 'bates', 'bathe', 'baths', 'batik', 'baton', 'batty', 'baulk', 'bawdy', 'bawls', 'bayed', 'beach', 'beads', 'beady', 'beaks', 'beams', 'beamy', 'beans', 'beany', 'beard', 'bears', 'beast', 'beats', 'beaus', 'beaux', 'bebop', 'becks', 'beech', 'beefs', 'beefy', 'beeps', 'beers', 'beery', 'beets', 'befit', 'befog', 'began', 'begat', 'beget', 'begin', 'begot', 'begun', 'beige', 'being', 'belay', 'belch', 'belie', 'belle', 'bells', 'belly', 'below', 'belts', 'bench', 'bends', 'beret', 'bergs', 'berry', 'berth', 'beryl', 'beset', 'besot', 'bests', 'betel', 'bevel', 'bevvy', 'bible', 'bided', 'bides', 'bidet', 'bigot', 'bijou', 'biker', 'bikes', 'biles', 'bilge', 'bills', 'billy', 'bimbo', 'binds', 'binge', 'bingo', 'biota', 'biped', 'birch', 'birds', 'birth', 'bison', 'bitch', 'biter', 'bites', 'bitts', 'bitty', 'blabs', 'black', 'blade', 'blame', 'bland', 'blank', 'blare', 'blase', 'blast', 'blaze', 'bleak', 'bleat', 'bleed', 'bleep', 'blend', 'bless', 'blimp', 'blind', 'blink', 'blips', 'bliss', 'blitz', 'bloat', 'blobs', 'block', 'blocs', 'bloke', 'blond', 'blood', 'bloom', 'blots', 'blown', 'blows', 'bluer', 'blues', 'bluff', 'blunt', 'blurb', 'blurs', 'blurt', 'blush', 'board', 'boars', 'boast', 'boats', 'bobby', 'boded', 'bodes', 'boers', 'bogey', 'boggy', 'bogus', 'boils', 'bolts', 'bombs', 'bonds', 'boned', 'bones', 'boney', 'bongs', 'bonny', 'bonus', 'booby', 'booed', 'books', 'booms', 'boons', 'boors', 'boost', 'booth', 'boots', 'booty', 'booze', 'borax', 'bored', 'borer', 'bores', 'borne', 'boron', 'bosom', 'boson', 'bossy', 'bosun', 'botch', 'bothy', 'bough', 'bound', 'bouts', 'bowed', 'bowel', 'bower', 'bowie', 'bowls', 'boxed', 'boxer', 'boxes', 'brace', 'brags', 'braid', 'brail', 'brain', 'brake', 'brand', 'brans', 'brash', 'brass', 'brats', 'brave', 'bravo', 'brawl', 'brawn', 'brays', 'braze', 'bread', 'break', 'bream', 'breed', 'brews', 'briar', 'bribe', 'brick', 'bride', 'brief', 'brims', 'brine', 'bring', 'brink', 'briny', 'brisk', 'broad', 'broil', 'broke', 'brood', 'brook', 'broom', 'broth', 'brown', 'brows', 'brunt', 'brush', 'brute', 'bucks', 'buddy', 'budge', 'buffs', 'buggy', 'bugle', 'build', 'built', 'bulbs', 'bulge', 'bulgy', 'bulks', 'bulky', 'bulls', 'bully', 'bumps', 'bumpy', 'bunch', 'bunks', 'bunny', 'buoys', 'burly', 'burma', 'burns', 'burnt', 'burps', 'burst', 'buses', 'bushy', 'busts', 'busty', 'butts', 'buxom', 'buyer', 'bylaw', 'bytes', 'byway', 'cabal', 'cabby', 'cabin', 'cable', 'cacao', 'cache', 'cacti', 'caddy', 'cadet', 'cadge', 'cafes', 'caged', 'cages', 'cagey', 'cairn', 'cairo', 'caked', 'cakes', 'calif', 'calls', 'calms', 'calve', 'camel', 'cameo', 'camps', 'canal', 'candy', 'caned', 'canes', 'canny', 'canoe', 'canon', 'caped', 'caper', 'capes', 'capri', 'carat', 'cards', 'cared', 'carer', 'cares', 'cargo', 'carol', 'carps', 'carry', 'carts', 'carve', 'cased', 'cases', 'casks', 'caste', 'casts', 'catch', 'cater', 'cause', 'caved', 'caver', 'caves', 'cease', 'cedar', 'ceded', 'celeb', 'cello', 'cells', 'cents', 'ceres', 'chafe', 'chaff', 'chain', 'chair', 'chalk', 'champ', 'chant', 'chaos', 'chaps', 'charm', 'chars', 'chart', 'chary', 'chase', 'chasm', 'chats', 'cheap', 'cheat', 'check', 'cheek', 'cheep', 'cheer', 'chefs', 'chess', 'chest', 'chews', 'chewy', 'chick', 'chide', 'chief', 'child', 'chili', 'chill', 'chime', 'chimp', 'china', 'chink', 'chins', 'chips', 'chirp', 'chits', 'chock', 'choir', 'choke', 'chomp', 'chops', 'chord', 'chore', 'chose', 'chuck', 'chuff', 'chugs', 'chump', 'chums', 'chunk', 'churn', 'chute', 'cider', 'cigar', 'cilia', 'cinch', 'circa', 'cited', 'cites', 'civic', 'civil', 'claim', 'clamp', 'clams', 'clang', 'clank', 'clans', 'claps', 'clash', 'clasp', 'class', 'claws', 'clays', 'clean', 'clear', 'cleat', 'cleft', 'clerk', 'click', 'cliff', 'climb', 'cling', 'clink', 'clips', 'cloak', 'clock', 'clods', 'clogs', 'clone', 'close', 'cloth', 'clots', 'cloud', 'clout', 'clove', 'clown', 'clubs', 'cluck', 'clued', 'clues', 'clump', 'clung', 'coach', 'coals', 'coast', 'coats', 'coble', 'cobra', 'cocks', 'cocky', 'cocoa', 'coded', 'coder', 'codes', 'codex', 'coils', 'coins', 'colas', 'colds', 'colon', 'colts', 'comas', 'combs', 'comer', 'comes', 'comet', 'comfy', 'comic', 'comma', 'coned', 'cones', 'conga', 'congo', 'conic', 'cooed', 'cooks', 'cools', 'coons', 'coops', 'coped', 'copes', 'copra', 'copse', 'coral', 'cords', 'cores', 'corgi', 'corks', 'corky', 'corns', 'corny', 'corps', 'corse', 'costs', 'couch', 'cough', 'could', 'count', 'coupe', 'coups', 'court', 'coven', 'cover', 'coves', 'covet', 'cowed', 'cower', 'coxed', 'coxes', 'coyly', 'crabs', 'crack', 'craft', 'crags', 'cramp', 'crams', 'crane', 'crank', 'crash', 'crass', 'crate', 'crave', 'crawl', 'craws', 'craze', 'crazy', 'creak', 'cream', 'credo', 'creed', 'creek', 'creel', 'creep', 'creme', 'crepe', 'crept', 'cress', 'crest', 'crete', 'crews', 'cribs', 'crick', 'cried', 'crier', 'cries', 'crime', 'crimp', 'crisp', 'croak', 'crock', 'croft', 'crone', 'crony', 'crook', 'croon', 'crops', 'cross', 'croup', 'crowd', 'crown', 'crows', 'crude', 'cruel', 'crumb', 'crush', 'crust', 'crypt', 'cuban', 'cubed', 'cubes', 'cubic', 'cubit', 'cuffs', 'cuing', 'culls', 'cults', 'cupid', 'curbs', 'curds', 'cured', 'curer', 'cures', 'curia', 'curie', 'curio', 'curls', 'curly', 'curry', 'curse', 'curve', 'curvy', 'cusps', 'cycad', 'cycle', 'cynic', 'cysts', 'czars', 'czech', 'dacha', 'daddy', 'daffy', 'dagga', 'daily', 'dairy', 'daisy', 'dakar', 'dales', 'dally', 'dames', 'damns', 'damps', 'dance', 'dandy', 'danes', 'dante', 'dared', 'dares', 'darns', 'darts', 'dated', 'dates', 'datum', 'daunt', 'david', 'dawns', 'dazed', 'deals', 'dealt', 'deans', 'dears', 'deary', 'death', 'debar', 'debit', 'debts', 'debug', 'debut', 'decaf', 'decay', 'decks', 'decor', 'decoy', 'decry', 'deeds', 'deems', 'deeps', 'defer', 'degas', 'deify', 'deism', 'deist', 'deity', 'delay', 'delhi', 'dells', 'delta', 'delve', 'demon', 'demur', 'denim', 'dense', 'dents', 'depot', 'depth', 'derby', 'desks', 'deter', 'detox', 'deuce', 'devil', 'dials', 'diana', 'diary', 'diced', 'dices', 'dicey', 'didnt', 'diets', 'digit', 'dikes', 'dildo', 'dilly', 'dimer', 'dimes', 'dimly', 'dinar', 'dined', 'diner', 'dines', 'dingo', 'dingy', 'dinky', 'dints', 'diode', 'dirge', 'dirts', 'dirty', 'disco', 'discs', 'dishy', 'ditch', 'ditto', 'ditty', 'divan', 'divas', 'dived', 'diver', 'dives', 'divot', 'dizzy', 'docks', 'dodge', 'dodgy', 'doers', 'doges', 'doggy', 'dogma', 'doily', 'doing', 'doled', 'doles', 'dolls', 'dolly', 'domed', 'domes', 'donga', 'donor', 'donut', 'dooms', 'doors', 'doped', 'dopes', 'dopey', 'dosed', 'doses', 'doted', 'dotes', 'dotty', 'doubt', 'dough', 'douse', 'dover', 'doves', 'dowdy', 'dowel', 'downs', 'downy', 'dowry', 'dowse', 'doyen', 'dozed', 'dozen', 'dozes', 'draft', 'drags', 'drain', 'drake', 'drama', 'drank', 'drape', 'drawl', 'drawn', 'draws', 'drays', 'dread', 'dream', 'drear', 'dregs', 'dress', 'dried', 'drier', 'dries', 'drift', 'drill', 'drily', 'drink', 'drips', 'drive', 'droll', 'drone', 'drool', 'droop', 'drops', 'dross', 'drove', 'drown', 'drugs', 'druid', 'drums', 'drunk', 'dryer', 'dryly', 'duals', 'duchy', 'ducks', 'ducts', 'dudes', 'duels', 'duets', 'dukes', 'dulls', 'dully', 'dummy', 'dumps', 'dumpy', 'dunce', 'dunes', 'duomo', 'duped', 'dupes', 'dusky', 'dusts', 'dusty', 'dutch', 'duvet', 'dwarf', 'dwell', 'dwelt', 'dyers', 'dying', 'dykes', 'eager', 'eagle', 'eared', 'earls', 'early', 'earns', 'earth', 'eased', 'easel', 'eases', 'eaten', 'eater', 'eaves', 'ebbed', 'ebony', 'edema', 'edged', 'edges', 'edict', 'edify', 'edits', 'eerie', 'egged', 'egret', 'egypt', 'eider', 'eight', 'eject', 'eking', 'eland', 'elate', 'elbow', 'elder', 'elect', 'elegy', 'elfin', 'elide', 'elite', 'elope', 'elude', 'elven', 'elves', 'email', 'embed', 'ember', 'emery', 'emirs', 'emits', 'empty', 'enact', 'ended', 'endow', 'enema', 'enemy', 'enjoy', 'ennui', 'enrol', 'ensue', 'enter', 'entry', 'envoy', 'eosin', 'ephor', 'epics', 'epoch', 'epoxy', 'equal', 'equip', 'erase', 'erect', 'ergot', 'erica', 'erode', 'erose', 'erred', 'error', 'erupt', 'essay', 'essen', 'ester', 'ether', 'ethic', 'ethos', 'ethyl', 'evade', 'evens', 'event', 'every', 'evict', 'evils', 'evoke', 'exact', 'exalt', 'exams', 'excel', 'exert', 'exile', 'exist', 'exits', 'expel', 'extol', 'extra', 'exude', 'exult', 'fable', 'faced', 'facer', 'faces', 'facet', 'facia', 'facts', 'faded', 'fades', 'fagot', 'fails', 'faint', 'fairs', 'fairy', 'faith', 'faked', 'fakes', 'falls', 'false', 'famed', 'fancy', 'fangs', 'fanny', 'farad', 'farce', 'fared', 'fares', 'farms', 'fasts', 'fatal', 'fated', 'fates', 'fatty', 'fatwa', 'fault', 'fauna', 'fauns', 'faust', 'fawns', 'faxed', 'faxes', 'fears', 'feast', 'feats', 'fedup', 'feeds', 'feels', 'feign', 'feint', 'fells', 'felon', 'femur', 'fence', 'fends', 'feral', 'ferns', 'ferny', 'ferry', 'fetal', 'fetch', 'feted', 'fetes', 'fetid', 'fetus', 'feuds', 'fever', 'fewer', 'fibre', 'fiche', 'ficus', 'fiefs', 'field', 'fiend', 'fiery', 'fifes', 'fifth', 'fifty', 'fight', 'filch', 'filed', 'filer', 'files', 'filet', 'fills', 'filly', 'films', 'filmy', 'filth', 'final', 'finch', 'finds', 'fined', 'finer', 'fines', 'finis', 'fiord', 'fired', 'firer', 'fires', 'firms', 'first', 'firth', 'fishy', 'fists', 'fitly', 'fiver', 'fives', 'fixed', 'fixer', 'fixes', 'fizzy', 'fjord', 'flabs', 'flack', 'flags', 'flair', 'flake', 'flaky', 'flame', 'flank', 'flans', 'flaps', 'flare', 'flash', 'flask', 'flats', 'flaws', 'fleas', 'fleck', 'flees', 'fleet', 'flesh', 'flick', 'flier', 'flies', 'fling', 'flint', 'flips', 'flirt', 'flits', 'float', 'flock', 'flogs', 'flood', 'floor', 'flops', 'flora', 'floss', 'flour', 'flout', 'flown', 'flows', 'flues', 'fluff', 'fluid', 'fluke', 'flung', 'fluor', 'flush', 'flute', 'flyer', 'foals', 'foams', 'foamy', 'focal', 'focus', 'fogey', 'foggy', 'foils', 'foist', 'folds', 'folio', 'folks', 'folly', 'fonts', 'foods', 'fools', 'foots', 'foray', 'force', 'fords', 'forge', 'forgo', 'forks', 'forms', 'forte', 'forth', 'forts', 'forty', 'forum', 'fossa', 'fouls', 'found', 'fount', 'fours', 'fowls', 'foxed', 'foxes', 'foyer', 'frail', 'frame', 'franc', 'frank', 'fraud', 'frays', 'freak', 'freed', 'freer', 'frees', 'freon', 'fresh', 'frets', 'freud', 'freya', 'friar', 'fried', 'fries', 'frill', 'frisk', 'frock', 'frogs', 'frond', 'front', 'frost', 'froth', 'frown', 'froze', 'fruit', 'fryer', 'fudge', 'fuels', 'fugal', 'fugue', 'fully', 'fumed', 'fumes', 'funds', 'fungi', 'funky', 'funny', 'furls', 'furry', 'furze', 'fused', 'fuses', 'fussy', 'fusty', 'futon', 'fuzzy', 'gable', 'gabon', 'gaffe', 'gaily', 'gains', 'gaits', 'galas', 'gales', 'galls', 'galop', 'gamed', 'games', 'gamma', 'gamut', 'gangs', 'gaols', 'gaped', 'gapes', 'garbs', 'gases', 'gasps', 'gassy', 'gated', 'gates', 'gaudy', 'gauge', 'gauls', 'gaunt', 'gauze', 'gavel', 'gawky', 'gazed', 'gazes', 'gears', 'gecko', 'geeks', 'geese', 'genes', 'genie', 'genii', 'genoa', 'genre', 'gents', 'genus', 'germs', 'ghana', 'ghost', 'ghoul', 'giant', 'gibed', 'gibes', 'giddy', 'gifts', 'gilds', 'gills', 'gilts', 'gipsy', 'girls', 'girth', 'given', 'giver', 'gives', 'glace', 'glade', 'gland', 'glans', 'glare', 'glass', 'glaze', 'gleam', 'glean', 'glebe', 'glenn', 'glens', 'glide', 'glint', 'gloat', 'globe', 'gloom', 'glory', 'gloss', 'glove', 'glows', 'glued', 'glues', 'gluey', 'gluon', 'glyph', 'gnarl', 'gnash', 'gnats', 'gnaws', 'gnome', 'goads', 'goals', 'goats', 'godly', 'goers', 'gofer', 'going', 'golds', 'golly', 'gonad', 'gongs', 'goods', 'goody', 'gooey', 'goofs', 'goofy', 'goons', 'goose', 'gored', 'gores', 'gorge', 'gorse', 'goths', 'gouda', 'gouge', 'gourd', 'gowns', 'grabs', 'grace', 'grade', 'graft', 'grail', 'grain', 'grams', 'grand', 'grant', 'grape', 'graph', 'grasp', 'grass', 'grate', 'grave', 'gravy', 'graze', 'great', 'greed', 'greek', 'green', 'greet', 'greys', 'grids', 'grief', 'grill', 'grime', 'grimm', 'grimy', 'grind', 'grins', 'gripe', 'grips', 'grist', 'grits', 'groan', 'groat', 'groin', 'groom', 'grope', 'gross', 'group', 'grout', 'grove', 'growl', 'grown', 'grows', 'grubs', 'gruel', 'gruff', 'grunt', 'guano', 'guard', 'guava', 'guess', 'guest', 'guide', 'guild', 'guile', 'guilt', 'guise', 'gulfs', 'gulls', 'gully', 'gulps', 'guppy', 'gurus', 'gusto', 'gusts', 'gusty', 'gutsy', 'gypsy', 'habit', 'hacks', 'hades', 'hadnt', 'hafts', 'haiku', 'hails', 'hairs', 'hairy', 'haiti', 'hakea', 'hallo', 'halls', 'halon', 'halts', 'halve', 'hands', 'handy', 'hangs', 'hanoi', 'happy', 'hardy', 'hared', 'harem', 'hares', 'harks', 'harms', 'harps', 'harry', 'harsh', 'harts', 'hasnt', 'haste', 'hasty', 'hatch', 'hated', 'hater', 'hates', 'hauls', 'haunt', 'haven', 'haves', 'havoc', 'hawks', 'haydn', 'hazel', 'heads', 'heady', 'heals', 'heaps', 'heard', 'hears', 'heart', 'heath', 'heats', 'heave', 'heavy', 'hedge', 'heeds', 'heels', 'hefty', 'heirs', 'heist', 'helen', 'helix', 'hello', 'hells', 'helms', 'helps', 'heman', 'hemen', 'hence', 'henge', 'henna', 'henry', 'herbs', 'herds', 'herod', 'heron', 'hertz', 'hewed', 'hewer', 'hexed', 'hider', 'hides', 'highs', 'hight', 'hiked', 'hiker', 'hikes', 'hills', 'hilly', 'hilts', 'hindu', 'hinge', 'hinny', 'hints', 'hippo', 'hippy', 'hired', 'hirer', 'hires', 'hitch', 'hived', 'hives', 'hoard', 'hoary', 'hobby', 'hocks', 'hocus', 'hoggs', 'hoist', 'holds', 'holed', 'holes', 'holly', 'homed', 'homes', 'honed', 'hones', 'honey', 'honks', 'hoods', 'hoofs', 'hooks', 'hooky', 'hoops', 'hoots', 'hoped', 'hopes', 'horde', 'horns', 'horny', 'horse', 'hosed', 'hoses', 'hosta', 'hosts', 'hotel', 'hotly', 'hound', 'hours', 'house', 'hovel', 'hover', 'howdy', 'howls', 'hubby', 'huffy', 'hulks', 'hullo', 'hulls', 'human', 'humid', 'humps', 'humus', 'hunch', 'hunks', 'hunts', 'hurls', 'hurry', 'hurts', 'husks', 'husky', 'hussy', 'hutch', 'hydra', 'hydro', 'hyena', 'hymen', 'hymns', 'hyper', 'ibsen', 'icier', 'icily', 'icing', 'icons', 'idaho', 'ideal', 'ideas', 'idiom', 'idiot', 'idled', 'idler', 'idles', 'idols', 'idyll', 'igloo', 'ileum', 'iliad', 'image', 'imago', 'imams', 'imbue', 'impel', 'imply', 'inane', 'incas', 'incur', 'index', 'india', 'inept', 'inert', 'infer', 'infix', 'infra', 'ingot', 'inked', 'inlaw', 'inlay', 'inlet', 'inner', 'input', 'inset', 'inter', 'intro', 'inuit', 'inure', 'ionic', 'iotas', 'iraqi', 'irate', 'irish', 'irked', 'irons', 'irony', 'islam', 'isles', 'islet', 'issue', 'italy', 'itchy', 'items', 'ivies', 'ivory', 'jacks', 'jacob', 'jaded', 'jades', 'jails', 'jambs', 'james', 'janus', 'japan', 'japes', 'jaunt', 'jawed', 'jazzy', 'jeans', 'jeeps', 'jeers', 'jehad', 'jelly', 'jemmy', 'jerks', 'jerky', 'jests', 'jesus', 'jetty', 'jewel', 'jiffy', 'jihad', 'jilts', 'jimmy', 'jingo', 'jinks', 'jived', 'jives', 'joins', 'joint', 'joist', 'joked', 'joker', 'jokes', 'jokey', 'jolly', 'jolts', 'jonah', 'joule', 'joust', 'jowls', 'joyed', 'judas', 'judge', 'juice', 'juicy', 'julep', 'jumbo', 'jumps', 'jumpy', 'junks', 'junta', 'juror', 'kalif', 'karma', 'karst', 'kayak', 'kebab', 'keels', 'keeps', 'kelts', 'kenya', 'kerbs', 'ketch', 'keyed', 'khaki', 'khans', 'kicks', 'kills', 'kilns', 'kilts', 'kinds', 'kings', 'kinks', 'kinky', 'kiosk', 'kites', 'kitty', 'kiwis', 'klick', 'kloof', 'knack', 'knave', 'knead', 'kneed', 'kneel', 'knees', 'knell', 'knelt', 'knife', 'knits', 'knobs', 'knock', 'knoll', 'knots', 'known', 'knows', 'koala', 'kongo', 'koran', 'korea', 'kraal', 'kraft', 'krill', 'kudus', 'label', 'labia', 'laced', 'laces', 'lacks', 'laden', 'ladle', 'lager', 'lagos', 'laird', 'lairs', 'laity', 'lakes', 'lamas', 'lambs', 'lamed', 'lamps', 'lance', 'lands', 'lanes', 'lanky', 'lapel', 'lapse', 'larch', 'lards', 'large', 'largo', 'larks', 'larva', 'laser', 'lasso', 'lasts', 'latch', 'later', 'latex', 'lathe', 'laths', 'latin', 'lauds', 'laugh', 'lavas', 'lawns', 'laxer', 'layby', 'layer', 'lazed', 'leach', 'leads', 'leafy', 'leaks', 'leaky', 'leans', 'leant', 'leaps', 'leapt', 'learn', 'lease', 'leash', 'least', 'leave', 'ledge', 'leech', 'leeds', 'leeks', 'leers', 'lefts', 'lefty', 'legal', 'leggy', 'lemma', 'lemon', 'lemur', 'lends', 'lenin', 'lento', 'leone', 'leper', 'level', 'lever', 'liars', 'libel', 'libya', 'lichi', 'licks', 'liens', 'lifts', 'light', 'liked', 'liken', 'likes', 'lilac', 'limbo', 'limbs', 'limes', 'limit', 'limps', 'lined', 'linen', 'liner', 'lines', 'links', 'lions', 'lipid', 'lisps', 'lists', 'lithe', 'litre', 'lived', 'liven', 'liver', 'lives', 'livid', 'llama', 'loads', 'loafs', 'loams', 'loamy', 'loans', 'loath', 'lobby', 'lobed', 'lobes', 'local', 'lochs', 'locks', 'locus', 'lodge', 'loess', 'lofts', 'lofty', 'logic', 'logos', 'loins', 'loire', 'lolly', 'loner', 'longs', 'looks', 'looms', 'loony', 'loops', 'loopy', 'loose', 'loots', 'loped', 'lopes', 'lords', 'lorry', 'loser', 'loses', 'lotto', 'lotus', 'louis', 'louse', 'lousy', 'louts', 'loved', 'lover', 'loves', 'lower', 'lowly', 'loyal', 'lucid', 'lucky', 'lucre', 'lulls', 'lumen', 'lumps', 'lumpy', 'lunar', 'lunch', 'lunge', 'lungs', 'lupin', 'lurch', 'lured', 'lures', 'lurex', 'lurid', 'lurks', 'lusts', 'lusty', 'lutes', 'luxor', 'lying', 'lymph', 'lynch', 'lyons', 'lyres', 'lyric', 'macaw', 'maces', 'macho', 'macro', 'madam', 'madly', 'mafia', 'magic', 'magma', 'maids', 'mails', 'maims', 'maine', 'mains', 'maize', 'major', 'maker', 'makes', 'malay', 'males', 'malls', 'malta', 'malts', 'malty', 'malva', 'mamas', 'mamba', 'mammy', 'maned', 'manes', 'mange', 'mango', 'mania', 'manic', 'manly', 'manna', 'manor', 'manse', 'maori', 'maple', 'march', 'mares', 'maria', 'marks', 'marls', 'marry', 'marsh', 'maser', 'masks', 'mason', 'masts', 'match', 'mated', 'mater', 'mates', 'maths', 'matte', 'mauls', 'mauve', 'maxim', 'mayas', 'maybe', 'mayor', 'mazes', 'meals', 'mealy', 'means', 'meant', 'meany', 'meats', 'meaty', 'mecca', 'medal', 'media', 'medic', 'meets', 'melee', 'melon', 'melts', 'mends', 'menus', 'meows', 'mercy', 'merge', 'merit', 'merry', 'meson', 'messy', 'metal', 'meted', 'meter', 'metre', 'metro', 'miami', 'micro', 'midas', 'midge', 'midst', 'might', 'mikes', 'milan', 'miler', 'miles', 'milks', 'milky', 'mills', 'mimed', 'mimes', 'mimic', 'mince', 'minds', 'mined', 'miner', 'mines', 'minim', 'minke', 'minks', 'minor', 'mints', 'minty', 'minus', 'mired', 'mires', 'mirth', 'miser', 'missy', 'mists', 'misty', 'mites', 'mitre', 'mitts', 'mixed', 'mixer', 'mixes', 'mixup', 'moans', 'moats', 'mocks', 'modal', 'model', 'modem', 'modes', 'mogul', 'moist', 'molar', 'molds', 'moldy', 'moles', 'molts', 'money', 'monks', 'month', 'moods', 'moody', 'mooed', 'moons', 'moors', 'moose', 'moped', 'mopes', 'moral', 'moray', 'mores', 'morns', 'moron', 'morph', 'morse', 'moses', 'mossy', 'motel', 'motes', 'motet', 'moths', 'motif', 'motor', 'motto', 'mould', 'moult', 'mound', 'mount', 'mourn', 'mouse', 'mousy', 'mouth', 'moved', 'mover', 'moves', 'movie', 'mowed', 'mower', 'mucks', 'mucky', 'mucus', 'muddy', 'muffs', 'mufti', 'muggy', 'mulch', 'mules', 'mummy', 'mumps', 'munch', 'muons', 'mural', 'murky', 'mused', 'muses', 'mushy', 'music', 'musks', 'musky', 'musts', 'musty', 'muted', 'mutes', 'mutts', 'muzak', 'myope', 'myrrh', 'myths', 'nadir', 'naiad', 'nails', 'naive', 'naked', 'named', 'names', 'nanny', 'naomi', 'nappy', 'nasal', 'nasty', 'natal', 'naval', 'navel', 'navvy', 'nazis', 'nears', 'necks', 'needs', 'needy', 'negev', 'neigh', 'nepal', 'nerds', 'nerve', 'nervy', 'nests', 'netts', 'never', 'newer', 'newly', 'newsy', 'newts', 'nguni', 'nicer', 'niche', 'nicks', 'niece', 'nifty', 'niger', 'night', 'nines', 'ninny', 'ninth', 'nixon', 'noble', 'nobly', 'nodal', 'noddy', 'nodes', 'nohow', 'noise', 'noisy', 'nomad', 'nooks', 'noons', 'noose', 'norms', 'north', 'nosed', 'noses', 'nosey', 'notch', 'noted', 'notes', 'nouns', 'novel', 'nudes', 'nudge', 'nulls', 'numbs', 'nurse', 'nutty', 'nyala', 'nylon', 'nymph', 'oaken', 'oakum', 'oases', 'oasis', 'oaths', 'obese', 'obeys', 'oboes', 'occur', 'ocean', 'ochre', 'octal', 'octet', 'odder', 'oddly', 'odium', 'odour', 'offal', 'offer', 'often', 'ogled', 'ogres', 'ohmic', 'oiled', 'oiler', 'oinks', 'okapi', 'okays', 'olden', 'older', 'oldie', 'olive', 'omega', 'omens', 'omits', 'onion', 'onset', 'oozed', 'oozes', 'opals', 'opens', 'opera', 'opine', 'opium', 'opted', 'optic', 'orang', 'orate', 'orbit', 'order', 'organ', 'oscar', 'other', 'otter', 'ought', 'ounce', 'ousts', 'outdo', 'outer', 'outgo', 'ovals', 'ovary', 'ovate', 'ovens', 'overs', 'overt', 'ovoid', 'owing', 'owlet', 'owned', 'owner', 'oxide', 'ozone', 'paced', 'pacer', 'paces', 'pacey', 'packs', 'pacts', 'paddy', 'padre', 'paean', 'pagan', 'paged', 'pager', 'pages', 'pails', 'pains', 'paint', 'pairs', 'paled', 'paler', 'pales', 'palls', 'palms', 'palmy', 'palsy', 'panda', 'paned', 'panel', 'panes', 'panga', 'pangs', 'panic', 'pansy', 'pants', 'papal', 'papas', 'papaw', 'paper', 'pappy', 'papua', 'parch', 'pared', 'pares', 'paris', 'parka', 'parks', 'parry', 'parse', 'parts', 'party', 'passe', 'pasta', 'paste', 'pasts', 'pasty', 'patch', 'paten', 'pater', 'pates', 'paths', 'patio', 'pause', 'paved', 'paves', 'pawed', 'pawns', 'payed', 'payee', 'payer', 'peace', 'peach', 'peaks', 'peaky', 'peals', 'pearl', 'pears', 'peaty', 'pecan', 'pecks', 'pedal', 'peeks', 'peels', 'peeps', 'peers', 'pekan', 'pelts', 'penal', 'pence', 'penny', 'perch', 'peril', 'perks', 'perky', 'perms', 'perry', 'perth', 'pesky', 'pests', 'petal', 'peter', 'petit', 'petty', 'phase', 'phlox', 'phone', 'phony', 'photo', 'phyla', 'piano', 'picks', 'piece', 'piers', 'pieta', 'piety', 'piggy', 'pikes', 'piled', 'piles', 'pills', 'pilot', 'pimps', 'pinch', 'pined', 'pines', 'pings', 'pinks', 'pinky', 'pints', 'pinup', 'pions', 'pious', 'piped', 'piper', 'pipes', 'pipit', 'pique', 'pitch', 'piths', 'pithy', 'piton', 'pivot', 'pixel', 'pixie', 'pizza', 'place', 'plaid', 'plain', 'plait', 'plane', 'plank', 'plans', 'plant', 'plasm', 'plate', 'plato', 'plays', 'plaza', 'plead', 'pleas', 'pleat', 'plebs', 'plied', 'plies', 'plods', 'plops', 'plots', 'ploys', 'pluck', 'plugs', 'plumb', 'plume', 'plump', 'plums', 'plumy', 'plush', 'pluto', 'poach', 'pocks', 'podgy', 'podia', 'poems', 'poets', 'point', 'poise', 'poked', 'poker', 'pokes', 'polar', 'poled', 'poles', 'polio', 'polka', 'polls', 'polyp', 'ponce', 'ponds', 'pooch', 'pools', 'popes', 'poppy', 'popup', 'porch', 'pored', 'pores', 'porky', 'porno', 'porns', 'ports', 'posed', 'poser', 'poses', 'posit', 'posse', 'posts', 'potch', 'potty', 'pouch', 'poult', 'pound', 'pours', 'pouts', 'power', 'prams', 'prang', 'prank', 'prawn', 'prays', 'preen', 'preps', 'press', 'preys', 'price', 'prick', 'pricy', 'pride', 'pried', 'pries', 'prime', 'print', 'prior', 'prise', 'prism', 'privy', 'prize', 'probe', 'prods', 'prone', 'prong', 'proof', 'props', 'prose', 'proud', 'prove', 'prowl', 'prows', 'proxy', 'prude', 'prune', 'psalm', 'pubic', 'puffs', 'puffy', 'pulls', 'pulps', 'pulpy', 'pulse', 'pumas', 'pumps', 'punch', 'punks', 'punky', 'punts', 'pupae', 'pupal', 'pupil', 'puppy', 'puree', 'purer', 'purge', 'purls', 'purrs', 'purse', 'pushy', 'pussy', 'putti', 'putts', 'putty', 'pygmy', 'pylon', 'pyres', 'qatar', 'quack', 'quaff', 'quail', 'quake', 'qualm', 'quark', 'quart', 'quash', 'quasi', 'quays', 'queen', 'queer', 'quell', 'quern', 'query', 'quest', 'queue', 'quick', 'quids', 'quiet', 'quiff', 'quill', 'quilt', 'quips', 'quire', 'quirk', 'quite', 'quits', 'quota', 'quote', 'rabat', 'rabbi', 'rabid', 'raced', 'racer', 'races', 'racks', 'radar', 'radii', 'radio', 'radix', 'radon', 'rafts', 'raged', 'rages', 'raids', 'rails', 'rains', 'rainy', 'raise', 'rajah', 'raked', 'rakes', 'rally', 'ramps', 'ranch', 'rands', 'randy', 'range', 'rangy', 'ranis', 'ranks', 'rants', 'raped', 'rapes', 'rapid', 'rarer', 'rased', 'rasps', 'raspy', 'rated', 'rater', 'rates', 'ratio', 'ratty', 'raved', 'ravel', 'raven', 'raver', 'raves', 'rayed', 'rayon', 'razed', 'razes', 'razor', 'reach', 'react', 'reads', 'ready', 'realm', 'reals', 'reams', 'reaps', 'rearm', 'rears', 'rebel', 'rebus', 'rebut', 'recap', 'recto', 'recur', 'redox', 'reeds', 'reefs', 'reeks', 'reels', 'refer', 'refit', 'regal', 'reich', 'reify', 'reign', 'reins', 'relax', 'relay', 'relic', 'relit', 'remap', 'remit', 'remix', 'remus', 'renal', 'rends', 'renew', 'rents', 'repay', 'repel', 'reply', 'reran', 'rerun', 'resea', 'reset', 'resin', 'resit', 'rests', 'retch', 'retro', 'retry', 'reuse', 'revel', 'revue', 'rhein', 'rhine', 'rhino', 'rhyme', 'rials', 'ricks', 'rider', 'rides', 'ridge', 'riffs', 'rifle', 'rifts', 'right', 'rigid', 'rigor', 'riled', 'riles', 'rills', 'rinds', 'rings', 'rinks', 'rinse', 'riots', 'ripen', 'riper', 'risen', 'riser', 'rises', 'risks', 'risky', 'rites', 'rival', 'riven', 'river', 'rivet', 'roach', 'roads', 'roams', 'roars', 'roast', 'robed', 'robes', 'robin', 'robot', 'rocks', 'rocky', 'rodeo', 'rogue', 'roles', 'rolls', 'roman', 'romps', 'roofs', 'rooks', 'rooms', 'roomy', 'roost', 'roots', 'roped', 'ropes', 'roses', 'rosin', 'rotas', 'rotor', 'rouge', 'rough', 'round', 'rouse', 'route', 'routs', 'roved', 'rover', 'roves', 'rowdy', 'rowed', 'rower', 'royal', 'rucks', 'ruddy', 'ruder', 'ruffs', 'rugby', 'ruins', 'ruled', 'ruler', 'rules', 'rumba', 'rumen', 'rummy', 'rumps', 'runes', 'rungs', 'runny', 'runts', 'rupee', 'rural', 'rusks', 'rusts', 'rusty', 'saber', 'sable', 'sabra', 'sabre', 'sacks', 'sadly', 'safer', 'safes', 'sagas', 'sages', 'sahib', 'sails', 'saint', 'sakes', 'salad', 'salem', 'sales', 'sally', 'salon', 'salsa', 'salts', 'salty', 'salve', 'salvo', 'samba', 'samoa', 'sands', 'sandy', 'saner', 'sarge', 'saris', 'satan', 'sated', 'satin', 'satyr', 'sauce', 'saucy', 'saudi', 'sauna', 'saute', 'saved', 'saver', 'saves', 'savvy', 'sawed', 'saxon', 'scabs', 'scald', 'scale', 'scalp', 'scaly', 'scamp', 'scams', 'scans', 'scant', 'scape', 'scare', 'scarf', 'scarp', 'scars', 'scary', 'scene', 'scent', 'schwa', 'scifi', 'scoff', 'scold', 'scone', 'scoop', 'scoot', 'scope', 'score', 'scorn', 'scots', 'scour', 'scout', 'scowl', 'scram', 'scrap', 'scree', 'screw', 'scrub', 'scrum', 'scuba', 'scuds', 'scuff', 'scull', 'seals', 'seams', 'seamy', 'sears', 'seats', 'sects', 'sedan', 'sedge', 'seeds', 'seedy', 'seeks', 'seems', 'seeps', 'seers', 'seine', 'seize', 'sells', 'semen', 'sends', 'sense', 'seoul', 'sepia', 'serai', 'serfs', 'serge', 'serif', 'serum', 'serve', 'setts', 'setup', 'seven', 'sever', 'sewed', 'sewer', 'sexed', 'sexes', 'shack', 'shade', 'shady', 'shaft', 'shags', 'shahs', 'shake', 'shaky', 'shale', 'shall', 'shame', 'shams', 'shank', 'shape', 'shard', 'share', 'shark', 'sharp', 'shave', 'shawl', 'sheaf', 'shear', 'sheds', 'sheen', 'sheep', 'sheer', 'sheet', 'sheik', 'shelf', 'shell', 'shied', 'shies', 'shift', 'shine', 'shins', 'shiny', 'ships', 'shire', 'shirk', 'shirt', 'shoal', 'shock', 'shoed', 'shoes', 'shone', 'shook', 'shoot', 'shops', 'shore', 'shorn', 'short', 'shots', 'shout', 'shove', 'shown', 'shows', 'showy', 'shred', 'shrew', 'shrub', 'shrug', 'shuns', 'shunt', 'shuts', 'shyer', 'shyly', 'sibyl', 'sided', 'sider', 'sides', 'sidle', 'siege', 'sieve', 'sifts', 'sighs', 'sight', 'sigma', 'signs', 'silks', 'silky', 'silly', 'silts', 'silty', 'sinai', 'since', 'sines', 'sinew', 'singe', 'sings', 'sinks', 'sinus', 'sired', 'siren', 'sires', 'sisal', 'sissy', 'sitar', 'sited', 'sites', 'sixes', 'sixth', 'sixty', 'sized', 'sizes', 'skate', 'skein', 'skews', 'skids', 'skied', 'skier', 'skies', 'skill', 'skimp', 'skims', 'skins', 'skips', 'skirl', 'skirt', 'skits', 'skuas', 'skulk', 'skull', 'skunk', 'slabs', 'slack', 'slags', 'slain', 'slake', 'slams', 'slang', 'slant', 'slaps', 'slash', 'slate', 'slats', 'slave', 'slavs', 'slays', 'sleds', 'sleek', 'sleep', 'sleet', 'slept', 'slice', 'slick', 'slide', 'slily', 'slime', 'slims', 'slimy', 'sling', 'slink', 'slips', 'slits', 'slobs', 'slogs', 'sloop', 'slope', 'slops', 'slosh', 'sloth', 'slots', 'slows', 'slugs', 'slump', 'slums', 'slung', 'slunk', 'slurp', 'slurs', 'slush', 'sluts', 'slyer', 'slyly', 'smack', 'small', 'smart', 'smash', 'smear', 'smell', 'smelt', 'smile', 'smirk', 'smite', 'smith', 'smock', 'smogs', 'smoke', 'smoky', 'smote', 'smuts', 'snack', 'snags', 'snail', 'snake', 'snaky', 'snaps', 'snare', 'snarl', 'sneak', 'sneer', 'snick', 'snide', 'sniff', 'snipe', 'snips', 'snits', 'snobs', 'snoek', 'snoop', 'snore', 'snort', 'snout', 'snows', 'snowy', 'snubs', 'snuff', 'soaks', 'soaps', 'soapy', 'soars', 'sober', 'socks', 'sodas', 'soddy', 'sodom', 'sofas', 'softy', 'soggy', 'soils', 'solar', 'soler', 'soles', 'solfa', 'solid', 'solve', 'somas', 'sonar', 'sones', 'songs', 'sonic', 'sonny', 'soots', 'sooty', 'soppy', 'sores', 'sorry', 'sorts', 'sotho', 'souks', 'souls', 'sound', 'soups', 'soupy', 'sours', 'south', 'sowed', 'sower', 'space', 'spade', 'spain', 'spank', 'spans', 'spare', 'spark', 'spars', 'spasm', 'spate', 'spats', 'spawn', 'spays', 'speak', 'spear', 'speck', 'specs', 'speed', 'spell', 'spelt', 'spend', 'spent', 'spews', 'spice', 'spicy', 'spied', 'spies', 'spike', 'spiky', 'spill', 'spilt', 'spine', 'spins', 'spiny', 'spire', 'spite', 'spits', 'splat', 'split', 'spoil', 'spoke', 'spoof', 'spook', 'spool', 'spoon', 'spoor', 'spore', 'sport', 'spots', 'spout', 'sprat', 'spray', 'spree', 'sprig', 'spume', 'spurn', 'spurs', 'spurt', 'squad', 'squat', 'squaw', 'squib', 'squid', 'stabs', 'stack', 'staff', 'stage', 'stags', 'staid', 'stain', 'stair', 'stake', 'stale', 'stalk', 'stall', 'stamp', 'stand', 'stank', 'stare', 'stark', 'stars', 'start', 'state', 'stave', 'stays', 'stead', 'steak', 'steal', 'steam', 'steed', 'steel', 'steep', 'steer', 'stems', 'steps', 'stern', 'stews', 'stick', 'sties', 'stiff', 'still', 'stilt', 'sting', 'stink', 'stint', 'stirs', 'stoat', 'stock', 'stoep', 'stoic', 'stoke', 'stole', 'stoma', 'stomp', 'stone', 'stony', 'stood', 'stool', 'stoop', 'stops', 'store', 'stork', 'storm', 'story', 'stout', 'stove', 'stows', 'strap', 'straw', 'stray', 'strew', 'strip', 'strop', 'strum', 'strut', 'stubs', 'stuck', 'studs', 'study', 'stuff', 'stump', 'stung', 'stuns', 'stunt', 'style', 'styli', 'suave', 'sucks', 'sudan', 'suede', 'sugar', 'suing', 'suite', 'suits', 'sulks', 'sulky', 'sully', 'summa', 'sumps', 'sunny', 'super', 'surer', 'surfs', 'surge', 'surly', 'sushi', 'swabs', 'swads', 'swags', 'swamp', 'swans', 'swaps', 'sward', 'swarm', 'swats', 'sways', 'swazi', 'swear', 'sweat', 'swede', 'sweep', 'sweet', 'swell', 'swept', 'swift', 'swill', 'swims', 'swine', 'swing', 'swipe', 'swirl', 'swish', 'swiss', 'swoon', 'swoop', 'swops', 'sword', 'swore', 'sworn', 'swots', 'swung', 'sylph', 'synod', 'syria', 'syrup', 'tabby', 'table', 'taboo', 'tacit', 'tacks', 'tacky', 'tails', 'taint', 'taken', 'taker', 'takes', 'tales', 'talks', 'tally', 'talon', 'tamed', 'tamer', 'tames', 'tango', 'tangy', 'tanks', 'tapas', 'taped', 'taper', 'tapes', 'tapir', 'tardy', 'tares', 'tarns', 'tarot', 'tarry', 'tarts', 'tarty', 'tasks', 'taste', 'tasty', 'tatty', 'taunt', 'tawny', 'taxed', 'taxes', 'taxis', 'teach', 'teams', 'tears', 'tease', 'teats', 'teddy', 'teems', 'teens', 'teeny', 'teeth', 'telex', 'tells', 'telly', 'tempi', 'tempo', 'tempt', 'tench', 'tends', 'tenet', 'tenon', 'tenor', 'tense', 'tenth', 'tents', 'tepee', 'tepid', 'terms', 'terns', 'terry', 'terse', 'tests', 'testy', 'tetra', 'texan', 'texas', 'texts', 'thane', 'thank', 'thaws', 'theft', 'their', 'theme', 'there', 'these', 'theta', 'thick', 'thief', 'thigh', 'thine', 'thing', 'think', 'thins', 'third', 'thong', 'thorn', 'those', 'three', 'threw', 'throb', 'throw', 'thrum', 'thuds', 'thugs', 'thumb', 'thump', 'thyme', 'tiara', 'tibia', 'ticks', 'tidal', 'tides', 'tiers', 'tiger', 'tight', 'tikka', 'tilde', 'tiled', 'tiler', 'tiles', 'tills', 'tilts', 'timed', 'timer', 'times', 'timid', 'tinge', 'tinny', 'tints', 'tipsy', 'tired', 'tires', 'titan', 'tithe', 'title', 'titre', 'toads', 'toady', 'toast', 'today', 'toddy', 'toffy', 'togas', 'toils', 'token', 'tokyo', 'tolls', 'tombs', 'tomes', 'tonal', 'toned', 'toner', 'tones', 'tonga', 'tongs', 'tonic', 'tonne', 'tools', 'tooth', 'topaz', 'topic', 'torah', 'torch', 'torso', 'torts', 'torus', 'total', 'totem', 'touch', 'tough', 'tours', 'touts', 'towed', 'towel', 'tower', 'towns', 'toxic', 'toxin', 'toyed', 'trace', 'track', 'tract', 'trade', 'trail', 'train', 'trait', 'tramp', 'trams', 'traps', 'trash', 'trawl', 'trays', 'tread', 'treat', 'trees', 'treks', 'trend', 'tress', 'trews', 'triad', 'trial', 'tribe', 'trice', 'trick', 'tried', 'trier', 'tries', 'trigs', 'trill', 'trims', 'tripe', 'trips', 'trite', 'troll', 'troop', 'trope', 'trots', 'trout', 'trove', 'truce', 'truck', 'truer', 'truly', 'trump', 'trunk', 'truss', 'trust', 'truth', 'tubas', 'tubby', 'tubed', 'tuber', 'tubes', 'tucks', 'tufts', 'tulip', 'tummy', 'tunas', 'tuned', 'tuner', 'tunes', 'tunic', 'tunny', 'turbo', 'turfs', 'turfy', 'turin', 'turks', 'turns', 'tusks', 'tutor', 'twain', 'twang', 'tweak', 'tweed', 'tweet', 'twice', 'twigs', 'twill', 'twine', 'twins', 'twirl', 'twist', 'tying', 'tykes', 'typed', 'types', 'tyres', 'udder', 'ulcer', 'ultra', 'umbra', 'unapt', 'unarm', 'unary', 'unbar', 'uncle', 'uncut', 'under', 'undid', 'undue', 'unfed', 'unfit', 'unfix', 'unify', 'union', 'unite', 'units', 'unity', 'unjam', 'unlit', 'unmet', 'unset', 'untie', 'until', 'unwed', 'unzip', 'upped', 'upper', 'uproo', 'upset', 'urban', 'urged', 'urges', 'urine', 'usage', 'users', 'usher', 'using', 'usual', 'usurp', 'usury', 'uteri', 'utter', 'uvula', 'vacua', 'vaduz', 'vague', 'vales', 'valet', 'valid', 'value', 'valve', 'vamps', 'vaned', 'vanes', 'vapid', 'vases', 'vault', 'veers', 'vegan', 'veils', 'veins', 'velar', 'veldt', 'velum', 'venal', 'vends', 'venom', 'vents', 'venue', 'venus', 'verbs', 'verge', 'verse', 'verve', 'vests', 'vexed', 'vexes', 'vials', 'vibes', 'vicar', 'vices', 'video', 'views', 'vigil', 'viler', 'villa', 'vines', 'vinyl', 'viola', 'viper', 'viral', 'virus', 'visas', 'visit', 'visor', 'vista', 'vital', 'vivid', 'vixen', 'vocal', 'vodka', 'vogue', 'voice', 'voids', 'voile', 'voles', 'volga', 'volts', 'vomit', 'voted', 'voter', 'votes', 'vouch', 'vowed', 'vowel', 'vulva', 'vying', 'wacky', 'waded', 'wader', 'wades', 'wadis', 'wafer', 'wafts', 'waged', 'wager', 'wages', 'wagon', 'waifs', 'wails', 'waist', 'waits', 'waive', 'waked', 'waken', 'wakes', 'wales', 'walks', 'walls', 'waltz', 'wands', 'waned', 'wanes', 'wanly', 'wants', 'wards', 'wares', 'warms', 'warns', 'warps', 'warts', 'warty', 'washy', 'wasps', 'waste', 'watch', 'water', 'watts', 'waved', 'waver', 'waves', 'waxed', 'waxen', 'waxes', 'weans', 'wears', 'weary', 'weave', 'webby', 'wedge', 'weeds', 'weedy', 'weeks', 'weeny', 'weeps', 'weepy', 'weigh', 'weird', 'weirs', 'welds', 'wells', 'welly', 'welsh', 'welts', 'wench', 'wends', 'wetly', 'whack', 'whale', 'wharf', 'wheat', 'wheel', 'whelk', 'whelp', 'where', 'which', 'whiff', 'while', 'whims', 'whine', 'whips', 'whirl', 'whirr', 'whisk', 'whist', 'white', 'whizz', 'whole', 'whoop', 'whore', 'whose', 'wicks', 'widen', 'wider', 'wides', 'widow', 'width', 'wield', 'wilds', 'wiles', 'wills', 'wilts', 'wimpy', 'wince', 'winch', 'winds', 'windy', 'wined', 'wines', 'wings', 'winks', 'wiped', 'wiper', 'wipes', 'wired', 'wirer', 'wires', 'wiser', 'wisps', 'wispy', 'witch', 'witty', 'wives', 'wodan', 'wodge', 'woken', 'wolds', 'woman', 'wombs', 'women', 'woods', 'woody', 'wooed', 'wooer', 'wools', 'wooly', 'words', 'wordy', 'works', 'world', 'worms', 'wormy', 'worry', 'worse', 'worst', 'worth', 'would', 'wound', 'woven', 'wowed', 'wrack', 'wraps', 'wrath', 'wreak', 'wreck', 'wrens', 'wrest', 'wring', 'wrist', 'write', 'writs', 'wrong', 'wrote', 'wrung', 'wryly', 'xenon', 'xhosa', 'xrays', 'yacht', 'yanks', 'yards', 'yarns', 'yawed', 'yawls', 'yawns', 'yearn', 'years', 'yeast', 'yells', 'yelps', 'yemen', 'yetis', 'yield', 'yodel', 'yoked', 'yokel', 'yokes', 'yolks', 'young', 'yours', 'youth', 'yukon', 'yummy', 'zaire', 'zappy', 'zeals', 'zebra', 'zebus', 'zesty', 'zippy', 'zombi', 'zonal', 'zoned', 'zones', 'zooms', 'zulus']
    word = ""
    remaining_height = 0
    remaining_length = 0
    keyboard_components = []
    guesses_components = []
    start_index = 0
    unlocked_cards = []
    locked_cards = []
    is_word_indicators = []
    animation = Animation([.4] * word_length)

    def __init__(self, height_used_up, length_used_up):
        """Initializes the object"""

        super().__init__(height_used_up, length_used_up, 5, IntermediateScreens(height_used_up, length_used_up, 1))
        random.shuffle(self.words)
        self.reset_everything()
        print(len(self.words))

    def set_keyboard_components(self, key_board_height, y_coordinate):
        """Sets the keyboard components for the game that displays what letters are being used"""

        max_length = screen_length - self.length_used_up
        NUMBER_OF_KEYS = 26
        KEYS_IN_TOP_ROW = 10
        KEYS_IN_MIDDLE_ROW = 9
        KEYS_IN_BOTTOM_ROW = 7
        NUMBER_OF_ROWS = 3
        grid = Grid(Dimensions(0, 0, 0, 0), None, 1, True)
        grid.length_buffer, grid.height_buffer = VelocityCalculator.give_measurement(screen_length, .1), VelocityCalculator.give_measurement(screen_length, .1)
        key_length = ( max_length - grid.length_buffer * KEYS_IN_TOP_ROW ) / KEYS_IN_TOP_ROW
        key_height = ( key_board_height - grid.height_buffer * NUMBER_OF_ROWS ) / NUMBER_OF_ROWS

        letters = "qwertyuiopasdfghjklzxcvbnm"

        for x in range(NUMBER_OF_KEYS):
            self.keyboard_components.append(TextBox(letters[x].upper(), 18, False, black, gray))
            self.keyboard_components[x].set_text_is_centered(True)

        top_row_keys = get_sublist(self.keyboard_components, 0, KEYS_IN_TOP_ROW)
        middle_row_keys = get_sublist(self.keyboard_components, KEYS_IN_TOP_ROW, KEYS_IN_MIDDLE_ROW)
        bottom_row_keys = get_sublist(self.keyboard_components, KEYS_IN_TOP_ROW + KEYS_IN_MIDDLE_ROW, KEYS_IN_BOTTOM_ROW)

        # TOP ROW
        grid.dimensions = Dimensions(self.length_used_up, y_coordinate, self.get_keyboard_length(key_length, KEYS_IN_TOP_ROW), key_height)

        grid.turn_into_grid(top_row_keys, key_length, key_height)

        # MIDDLE ROW
        grid.dimensions = Dimensions(self.length_used_up + key_length * .2, grid.dimensions.bottom,
                                     self.get_keyboard_length(key_length, KEYS_IN_MIDDLE_ROW), key_height)

        grid.turn_into_grid(middle_row_keys, key_length, key_height)

        # BOTTOM ROW
        grid.dimensions = Dimensions(self.length_used_up + key_length * 1, grid.dimensions.bottom,
                          self.get_keyboard_length(key_length, KEYS_IN_BOTTOM_ROW), key_height)

        grid.turn_into_grid(bottom_row_keys, key_length, key_height)

    def set_guesses_components(self, guesses_height):
        """Sets the grid that displays the player's guesses and if it is the word indicators"""

        total_components = self.max_guesses * self.word_length
        for x in range(total_components):
            card = Card("", 20, False, black, light_gray)
            card.set_click_action(self.on_card_click)
            self.guesses_components.append(card)
            self.guesses_components[x].set_text_is_centered(True)

        length_buffer = self.remaining_length * .1
        length = self.remaining_length - length_buffer * 2
        grid = Grid(Dimensions(self.length_used_up + length_buffer, self.height_used_up, length, guesses_height),
                    None, self.max_guesses, True)
        grid.turn_into_grid(self.guesses_components[:total_components], None, None)

        for x in range(self.max_guesses):
            self.is_word_indicators.append(TextBox("", 20, False, white, red))
            buffer = VelocityCalculator.give_measurement(screen_length, 2)

            height = grid.get_item_height(self.max_guesses, None)
            y_coordinate = grid.dimensions.y_coordinate + (height * x) + (grid.height_buffer * x)

            self.is_word_indicators[x].number_set_dimensions(grid.dimensions.right_edge + buffer, y_coordinate, length_buffer, height)

    def get_keyboard_length(self, key_length, number_of_keys):
        """returns: double; the length that the row of keyboard should be"""

        return (key_length * number_of_keys) + (Grid.length_buffer * number_of_keys)

    def run(self):
        """Runs all the code necessary for the game to work"""

        self.run_key_events()
        self.set_locked_and_unlocked_cards()
        self.run_intermediate_screens()
        self.animation.run()

        if self.animation.is_done:
            self.change_letters_typed()

        # Resetting the text for all the text boxes
        for card in self.unlocked_cards:
            card.text = ""

        for x in range(len(self.typed_letters)):
            self.unlocked_cards[x].text = self.typed_letters[x].upper()

        is_word_indicator: TextBox = self.is_word_indicators[self.current_index]
        is_word_indicator.set_color(green if self.can_submit() else red)

        if self.can_submit() and pygame.key.get_pressed()[pygame.K_RETURN]:
            self.run_submission()

    def set_locked_and_unlocked_cards(self):
        """Sets the cards that are locked and unlocked"""
        current_cards = get_sublist(self.guesses_components, self.current_index * self.word_length, self.word_length)
        self.unlocked_cards = []
        self.locked_cards = []

        for card in current_cards:
            if card.is_locked:
                self.locked_cards.append(card)

            else:
                self.unlocked_cards.append(card)

    def on_card_click(self, card):
        """Runs the code that should be run when a card is clicked"""
        current_cards = get_sublist(self.guesses_components, self.current_index * self.word_length, self.word_length)

        if card.is_locked and current_cards.__contains__(card):
            self.locked_cards.remove(card)

        elif current_cards.__contains__(card):
            self.unlocked_cards.remove(card)
            self.locked_cards.append(card)
            self.typed_letters = remove_index(self.typed_letters, current_cards.index(card))

        if current_cards.__contains__(card):
            card.is_locked = not card.is_locked

    def change_letters_typed(self):
        """Gets all the letters typed and modifies the attribute 'letters_typed'"""

        self.typed_letters += self.get_letters_typed()
        if pygame.key.get_pressed()[pygame.K_BACKSPACE] and not self.backspace_event.happened_last_cycle():
            # Removes the last letter
            self.typed_letters = self.typed_letters[:-1]

        max_letters = len(self.unlocked_cards)

        if len(self.typed_letters) >= max_letters:
            self.typed_letters = self.typed_letters[:max_letters]

        self.typed_letters = get_uppercase(self.typed_letters)

    def get_components(self):
        """returns: List of Component; the components that should be rendered"""

        screens_components = self.keyboard_components + [self.is_word_indicators[self.current_index]] + self.guesses_components
        return self.intermediate_screens.get_components() if not self.intermediate_screens.is_done() else screens_components

    def run_submission(self):
        """Runs all the logic for submitting a guess"""

        self.run_submission_guess()

        if get_uppercase(self.word) == get_uppercase(self.typed_letters):
            print("YOU GOT IT")
            self.intermediate_screens.display(["Congratulations"], [1.5])

        elif self.current_guess > self.max_guesses:
            self.intermediate_screens.display([f"The Word Was {self.word}"], [1.5])

        if get_uppercase(self.word) == get_uppercase(self.typed_letters) or self.current_guess >= self.max_guesses:
            self.round_number += 1
            self.reset_everything()

    def get_keyboard_letter(self, letter):
        """returns: TextBox; the keyboard key associated with that letter"""

        return_value = None
        for key in self.keyboard_components:
            if key.text.upper() == letter.upper():
                return_value = key
                break

        return return_value

    def reset_everything(self):
        """Resets everything to the start of the game"""

        self.keyboard_components, self.guesses_components = [], []
        self.is_word_indicators = []
        self.remaining_height = screen_height - self.height_used_up
        self.remaining_length = screen_length - self.length_used_up

        key_board_height = self.remaining_height * .3
        guesses_height = self.remaining_height - key_board_height
        self.set_keyboard_components(key_board_height, screen_height - key_board_height)
        self.set_guesses_components(guesses_height)
        self.word = self.words[self.round_number]
        self.word = get_uppercase(self.word)
        self.current_guess = 1
        self.current_index = 0
        self.typed_letters = ""

    def run_submission_guess(self):
        """Runs all the code for displaying what letters are good and what letters aren't; not used if the player has
           guessed correctly or if they had too many guesses"""

        typed_letters = self.get_all_letters()
        word = string_to_list(self.word)

        green_letters = []
        current_components = get_sublist(self.guesses_components, self.current_index * self.word_length, self.word_length)
        colors = [None] * len(typed_letters)
        for x in range(len(typed_letters)):
            if word[x] == typed_letters[x]:
                component = current_components[x]
                green_letters.append(component)
                colors[x] = green
                self.get_keyboard_letter(typed_letters[x]).set_color(green)

        for green_letter in green_letters:
            word.remove(green_letter.text)

        for x in range(len(typed_letters)):
            component = current_components[x]
            if word.__contains__(typed_letters[x]) and not green_letters.__contains__(component):
                colors[x] = yellow
                self.get_keyboard_letter(typed_letters[x]).set_color(yellow)
                word.remove(typed_letters[x])

            elif not green_letters.__contains__(component):
                try:
                    colors[x] = dark_gray
                except:
                    print("BAD")
                self.get_keyboard_letter(typed_letters[x]).set_color(dark_gray)

        for component in self.get_current_components():
            component.is_locked = False

        if not get_uppercase(self.word) == get_uppercase(self.typed_letters) and not self.current_guess >= self.max_guesses:
            self.current_guess += 1
            self.current_index += 1
            self.typed_letters = ""

        print(colors)
        self.animation.run_animation(current_components, colors, self.set_component_color)

    def set_component_color(self, component, color):
        """Sets the components color to the color specified"""

        component.set_color(color)

    def reset_cards(self):
        """Resets the cards after a submission has been run: the locked and unlocked cards"""

        for card in self.locked_cards:
            card.is_locked = False

        self.locked_cards = []
        self.unlocked_cards = []

    def can_submit(self):
        """returns: boolean; if the player can submit their guess"""

        return WordGame.can_submit(self, self.get_all_letters(), self.word_length)

    def get_current_components(self):
        """returns: List of Card; the current cards that the player is modifying"""

        return get_sublist(self.guesses_components, self.current_index * self.word_length, self.word_length)

    def get_all_letters(self):
        """returns: String; all the letters"""
        all_letters = ""

        for component in self.get_current_components():
            all_letters += component.text

        return all_letters







