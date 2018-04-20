import re
import json
import xml.etree.ElementTree as ET

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)


def remove_tags2(text):
    return ''.join(ET.fromstring(text).itertext())


test_text = "<p>I am in <b>charge</b> o <code>remove me</code></p>"

print(remove_tags(test_text))
print(remove_tags2(test_text))


def getTextWithoutHTMLTags(text):
    return text

def getTextWithoutHTMLTagsAndWithoutCode(text):
    return text

def remove_special_chars(text):
    #return re.sub("[^a-z0-9]+","", text, flags=re.IGNORECASE)    
    return text.replace(r'\n', '')




# - remove crlf
# - remove tags
# - remove code
def clean(text):
    return remove_special_chars(text)


test_text = r"""
<p>I have a number of products in WC that have bundled equivalents where each bundle is just multiple 
quantities of the single product (e.g. pack of 6, 9, etc).</p>
\n\n<p>During checkout on a purchased bundle, I need to get the attributes of the parent product and 
the quantity multiplier for the bundle to multiply by the amount they added to thecart.</p>
\n\n<p>How do I do do this when I\'m looping thru each item on the order?</p>
\n\n<pre><code>foreach ( $order-&gt;get_items() as $item ) {\n    // ...\n}\n</code></pre>
\n\n<p>I checked and could not find the methods in <code>$item-&gt;get_product()</code> when called in the
action <code>woocommerce_checkout_order_processed</code>.</p>
\n\n<p><a href="https://i.stack.imgur.com/vT56h.png" rel="nofollow noreferrer">
<img src="https://i.stack.imgur.com/vT56h.png" alt="enter image description here"></a></p>
\n
"""

print(clean(test_text))

#read merged
#merged = json.load(open('./res/merge.json'))

#iterate questions
#result = {}
#for q in merged:    
#    result[q] = clean(merged[q]['body'])

#with open('./res/htmlcleaned.json', 'w') as f:
#    json.dump(result, f, sort_keys=True, indent=4, ensure_ascii=False)

