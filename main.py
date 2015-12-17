# -*- encoding: utf-8 -*-                                                                                                                                    

import json,gzip,re,itertools,sys
import cabocha

# 絵文字の正規表現  新しい絵文字をどんどん追加しよう
# twitterで使われる絵文字一覧： http://jp.piliapp.com/emoji/list/

# ツイートのイテレータ
file_path = sys.argv[1]
file_name = file_path.split("/")[-1]
print file_name

def tweet_iter():
    with gzip.open(file_path) as f:
        for line in f:
            j = json.loads(line.strip())
            yield  j[u"text"]    

#  絵文字のリスト
emoji_list = [u'😀',u'😛',u'😸',u'👷',u'💋',u'😁',u'😜',u'😹',u'👸',u'👅',u'😂',u'😝',u'😺',u'💂',u'💅'
                      ,u'😃',u'😞',u'😻',u'👼',u'👋',u'😄',u'😟',u'😼',u'🎅',u'👍',u'😅',u'😠',u'😽',u'👻',u'👎'
                      ,u'😆',u'😡',u'😾',u'👹',u'😇',u'😢',u'😿',u'👺',u'👆',u'😈',u'😣',u'🙀',u'💩',u'👇',u'👿'
                      ,u'😤',u'👣',u'💀',u'👈',u'😉',u'😥',u'👤',u'👽',u'👉',u'😊',u'😦',u'👥',u'👾',u'👌',u'😧'
                      ,u'👦',u'🙇',u'😋',u'😨',u'👧',u'💁',u'👊',u'😌',u'😩',u'👨',u'🙅',u'✊',u'😍',u'😪',u'👩'
                      ,u'🙆',u'✋',u'😎',u'😫',u'👪',u'🙋',u'💪',u'😏',u'😬',u'👫',u'🙎',u'👐',u'😐',u'😭',u'👬'
                      ,u'🙍',u'🙏',u'😑',u'😮',u'👭',u'💆',u'😒',u'😯',u'👮',u'💇',u'😓',u'😰',u'👯',u'💑',u'😔'
                      ,u'😱',u'👰',u'💏',u'😕',u'😲',u'👱',u'🙌',u'😖',u'😳',u'👲',u'👏',u'😗',u'😴',u'👳',u'👂'
                      ,u'😘',u'😵',u'👴',u'👀',u'😙',u'😶',u'👵',u'👃',u'😚',u'😷',u'👶',u'👄',u'🌱',u'🌲',u'🌳'
                      ,u'🌴',u'🌵',u'🌷',u'🌸',u'🌹',u'🌺',u'🌻',u'🌼',u'💐',u'🌾',u'🌿',u'🍀',u'🍁',u'🍂',u'🍃'
                      ,u'🍄',u'🌰',u'🐀',u'🐁',u'🐭',u'🐹',u'🐂',u'🐃',u'🐄',u'🐮',u'🐅',u'🐆',u'🐯',u'🐇',u'🐰'
                      ,u'🐈',u'🐱',u'🐎',u'🐴',u'🐏',u'🐑',u'🐐',u'🐓',u'🐔',u'🐤',u'🐣',u'🐥',u'🐦',u'🐧',u'🐘'
                      ,u'🐪',u'🐫',u'🐗',u'🐖',u'🐷',u'🐽',u'🐕',u'🐩',u'🐶',u'🐺',u'🐻',u'🐨',u'🐼',u'🐵',u'🙈'
                      ,u'🙉',u'🙊',u'🐒',u'🐉',u'🐲',u'🐊',u'🐍',u'🐢',u'🐸',u'🐋',u'🐳',u'🐬',u'🐙',u'🐟',u'🐠'
                      ,u'🐡',u'🐚',u'🐌',u'🐛',u'🐜',u'🐝',u'🐞',u'🐾',u'⚡️',u'🔥',u'🌙',u'☀️',u'⛅',u'☁️',u'💧'
                      ,u'💦',u'☔',u'💨',u'🌟',u'⭐',u'🌠',u'🌄',u'🌅',u'🌈',u'🌊',u'🌋',u'🌌',u'🗻',u'🗾',u'🌐'
                      ,u'🌍',u'🌎',u'🌏',u'🌑',u'🌒',u'🌓',u'🌔',u'🌕',u'🌖',u'🌗',u'🌘',u'🌚',u'🌝',u'🌛',u'🌜'
                      ,u'🌞',u'🍅',u'🍆',u'🌽',u'🍠',u'🍇',u'🍈',u'🍉',u'🍊',u'🍋',u'🍌',u'🍍',u'🍎',u'🍏',u'🍐'
                      ,u'🍑',u'🍓',u'🍒',u'🍔',u'🍕',u'🍖',u'🍗',u'🍘',u'🍙',u'🍚',u'🍛',u'🍜',u'🍝',u'🍞',u'🍟'
                      ,u'🍡',u'🍢',u'🍣',u'🍤',u'🍥',u'🍦',u'🍧',u'🍨',u'🍩',u'🍪',u'🍫',u'🍬',u'🍭',u'🍮',u'🍯'
                      ,u'🍰',u'🍱',u'🍲',u'🍳',u'🍴',u'🍵',u'☕',u'🍶',u'🍷',u'🍸',u'🍹',u'🍺',u'🍻',u'🍼',u'🎂'
                      ,u'🎃',u'🎄',u'🎋',u'🎍',u'🎑',u'🎆',u'🎇',u'🎉',u'🎊',u'🎈',u'💫',u'✨',u'💥',u'🎓',u'👑'
                      ,u'🎎',u'🎏',u'🎐',u'🎌',u'🏮',u'💍',u'💔',u'💌',u'💕',u'💞',u'💓',u'💗',u'💖',u'💘',u'💝'
                      ,u'💟',u'💜',u'💛',u'💚',u'💙',u'🏃',u'🚶',u'💃',u'🚣',u'🏊',u'🏄',u'🛀',u'🏂',u'🎿',u'⛄'
                      ,u'🚴',u'🚵',u'🏇',u'⛺',u'🎣',u'⚽',u'🏀',u'🏈',u'⚾️',u'🎾',u'🏉',u'⛳',u'🏆',u'🎽',u'🏁'
                      ,u'🎹',u'🎸',u'🎻',u'🎷',u'🎺',u'🎵',u'🎶',u'🎼',u'🎧',u'🎤',u'🎭',u'🎫',u'🎩',u'🎪',u'🎬'
                      ,u'🎨',u'🎯',u'🎱',u'🎳',u'🎰',u'🎲',u'🎮',u'🎴',u'🃏',u'🀄',u'🎠',u'🎡',u'🎢',u'🚃',u'🚞'
                      ,u'🚂',u'🚋',u'🚝',u'🚄',u'🚅',u'🚆',u'🚇',u'🚈',u'🚉',u'🚊',u'🚌',u'🚍',u'🚎',u'🚐',u'🚑'
                      ,u'🚒',u'🚓',u'🚔',u'🚨',u'🚕',u'🚖',u'🚗',u'🚘',u'🚙',u'🚚',u'🚛',u'🚜',u'🚲',u'🚏',u'⛽'
                      ,u'🚧',u'🚦',u'🚥',u'🚀',u'🚁',u'💺',u'⚓',u'🚢',u'🚤',u'⛵',u'🚡',u'🚠',u'🚟',u'🛂',u'🛃'
                      ,u'🛄',u'🛅',u'💴',u'💶',u'💷',u'💵',u'🗽',u'🗿',u'🌁',u'🗼',u'⛲',u'🏰',u'🏯',u'🌇',u'🌆'
                      ,u'🌃',u'🌉',u'🏠',u'🏡',u'🏢',u'🏬',u'🏭',u'🏣',u'🏤',u'🏥',u'🏨',u'🏩',u'💒',u'⛪',u'🏪'
                      ,u'⌚',u'📱',u'📲',u'💻',u'⏰',u'⏳',u'⌛',u'📷',u'📹',u'🎥',u'📺',u'📻',u'📟',u'📞',u'📠'
                      ,u'💽',u'💾',u'💿',u'📀',u'📼',u'🔋',u'🔌',u'💡',u'🔦',u'📡',u'💳',u'💸',u'💰',u'💎',u'🌂'
                      ,u'👝',u'👛',u'👜',u'💼',u'🎒',u'💄',u'👓',u'👒',u'👡',u'👠',u'👢',u'👞',u'👟',u'👙',u'👗'
                      ,u'👘',u'👚',u'👕',u'👔',u'👖',u'🚪',u'🚿',u'🛁',u'🚽',u'💈',u'💉',u'💊',u'🔬',u'🔭',u'🔮'
                      ,u'🔧',u'🔪',u'🔩',u'🔨',u'💣',u'🚬',u'🔫',u'🔖',u'📰',u'🔑',u'📩',u'📨',u'📧',u'📥',u'📤'
                      ,u'📦',u'📯',u'📮',u'📪',u'📫',u'📬',u'📭',u'📄',u'📃',u'📑',u'📈',u'📉',u'📊',u'📅',u'📆'
                      ,u'🔅',u'🔆',u'📜',u'📋',u'📖',u'📓',u'📔',u'📒',u'📕',u'📗',u'📘',u'📙',u'📚',u'📇',u'🔗'
                      ,u'📎',u'📌',u'📐',u'📍',u'📏',u'🚩',u'📁',u'📂',u'📝',u'🔏',u'🔐',u'🔒',u'🔓',u'📣',u'📢'
                      ,u'🔈',u'🔉',u'🔊',u'🔇',u'💤',u'🔔',u'🔕',u'💭',u'💬',u'🚸',u'🔍',u'🔎',u'🎁',u'🚫',u'⛔'
                      ,u'📛',u'🚷',u'🚯',u'🚳',u'🚱',u'📵',u'🔞',u'🉑',u'🉐',u'💮',u'㊗️',u'➕',u'➖',u'〰️',u'➗'
                      ,u'🔃',u'💱',u'💲',u'➰',u'➿',u'〽️',u'❗',u'❓',u'❕',u'❔',u'❌',u'⭕',u'💯',u'🔚',u'🔙'
                      ,u'🔛',u'🔝',u'🔜',u'🌀',u'Ⓜ️',u'⛎',u'🔯',u'🔰',u'🔱',u'⚠️',u'♻️',u'💢',u'💠',u'⚪️',u'⚫️'
                      ,u'🔘',u'🔴',u'🔵',u'🔺',u'🔻',u'🔸',u'🔹',u'🔶',u'🔷',u'⬛',u'⬜',u'◾',u'◽️',u'🔲',u'🔳'
                      ,u'🕐',u'🕜',u'🕑',u'🕝',u'🕒',u'🕞',u'🕓',u'🕟',u'🕔',u'🕠',u'🕕',u'🕡',u'🕖',u'🕢',u'🕗'
                      ,u'🕣',u'🕘',u'🕤',u'🕙',u'🕥',u'🕦',u'🕛',u'🕧',u'🈴',u'🈵',u'🈲',u'🈶',u'🈚',u'🈸',u'🈺'
                      ,u'🈹',u'🈳',u'🈁',u'🈯',u'💹',u'❎',u'✅',u'📳',u'📴',u'🆚',u'🅰️',u'🅱️',u'🆎',u'🆑',u'🅾️'
                      ,u'🆘',u'🆔',u'🅿️',u'🚾',u'🆒',u'🆓',u'🆕',u'🆖',u'🆗',u'🆙',u'🏧',u'♈️',u'♉️',u'♊️',u'♋️'
                      ,u'♌️',u'♍️',u'♎️',u'♏️',u'♐️',u'♑️',u'♒️',u'♓️',u'🚻',u'🚹',u'🚺',u'🚼',u'♿️',u'🚰',u'🚭'
                      ,u'🚮',u'🔢',u'🔤',u'🔡',u'🔠',u'📶']
emoji_set = set(emoji_list)
# 絵文字検出正規表現
emoji_g = u"("+u"|".join(emoji_list)+u")"
emoji_p = re.compile(emoji_g)

# URL の正規表現
url_p = re.compile(u"https?:[A-z/.0-9]*")
# アカウントの正規表現
account_p = re.compile(u"@[A-z_0-9]*")

emoji_freq = dict([(e,0) for e in emoji_list])
def update_emoji_freq(e):
    emoji_freq[e] += 1

word_freq = {}
def update_word_freq(w):
    if w not in word_freq:
        word_freq[w] = 1
    else:
        word_freq[w] += 1

emoji_with_emoji = dict([(e1,dict([(e2,0) for e2 in emoji_list])) for e1 in emoji_list])
def update_emoji_with_emoji(e1,e2):
    emoji_with_emoji[e1][e2] += 1
    if e1 != e2:
        emoji_with_emoji[e2][e1] += 1
    
emoji_with_word = dict([(e,{}) for e in emoji_list])
def update_emoji_with_word(e,w):
    if w not in emoji_with_word[e]:
        emoji_with_word[e][w] = 1
    else:
        emoji_with_word[e][w] += 1

# ツイート本文をトークンのリストに分割する関数
def split_sent(sentence):
    emoji_list = []
    word_list = []
    temp = emoji_p.split(sentence)
    if len(temp) < 2:
        return False
    else:
        for each in temp:
            if each in emoji_set:
                emoji_list.append(each)
            elif each:
                try:
                    chunks = cabocha.parsed2chunks(cabocha.parse(each.encode("utf-8")))
                    for c in chunks.values():
                        for m in c.morphs:
                            if m.pos in ["動詞","形容詞","名詞"]:
                                if m.base == "*":
                                    word_list.append(m.surface)
                                else:
                                    word_list.append(m.base)
                except:
                    pass
        return emoji_list, word_list

tw = tweet_iter()
i = 0
while True:
    if i % 1000 == 0:
        print i
    i += 1
    line = tw.next()
    if not line:
        print "DONE"
        break
    temp  = split_sent(account_p.sub(" ACCOUNT ",url_p.sub(" URL ",line)))
    if temp:
        emoji_list, word_list = temp[0], temp[1]
        for e in emoji_list:
            update_emoji_freq(e)
        for w in word_list:
            update_word_freq(w)
        if len(emoji_list) > 1:
            for e1,e2 in itertools.combinations(emoji_list,2):
                update_emoji_with_emoji(e1,e2)
        for e, w in itertools.product(emoji_list,word_list):
             update_emoji_with_word(e,w)
    
data = {"emoji_with_emoji":emoji_with_emoji,
        "emoji_with_word":emoji_with_word,
        "emoji_freq":emoji_freq,
        "word_freq":word_freq}

with open(file_name + ".result.json", 'w') as f:
    json.dump(data, f)

