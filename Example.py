
import os,sys,re,pickle

os.chdir('/data/duongdb/pyConTextNLP')


import pyConTextNLP.pyConTextGraph as pyConText
import pyConTextNLP.itemData as itemData
from textblob import TextBlob
import networkx as nx
import pyConTextNLP.display.html as html
from IPython.display import display, HTML

reports = [
    """IMPRESSION: Evaluation limited by lack of IV contrast; however, no evidence of
      bowel obstruction or mass identified within the abdomen or pelvis. Non-specific interstitial opacities and bronchiectasis seen at the right
     base, suggestive of post-inflammatory changes.""",
    """IMPRESSION: Evidence of early pulmonary vascular congestion and interstitial edema. Probable scarring at the medial aspect of the right lung base, with no
     definite consolidation."""
    ,
    """IMPRESSION:
     
     1.  2.0 cm cyst of the right renal lower pole.  Otherwise, normal appearance
     of the right kidney with patent vasculature and no sonographic evidence of
     renal artery stenosis.
     2.  Surgically absent left kidney.""",
    """IMPRESSION:  No pneumothorax.""",
    """IMPRESSION: No definite pneumothorax""",
    """IMPRESSION:  New opacity at the left lower lobe consistent with pneumonia.""", 

    """Patient is 8 years old.""", 
    """She is 7 yr old.""",
    """This person is not 7 years of age.""",
    """Jack is 10 months old.""",
    """Age 7 yrs.""", 
    """Age: 7""", 
    """He has depression for 2 years."""
    
]

modifiers = itemData.instantiateFromCSVtoitemData(
    "/data/duongdb/pyConTextNLP/KB/lexical_kb_05042016.tsv")
targets = itemData.instantiateFromCSVtoitemData(
    "/data/duongdb/pyConTextNLP/KB/utah_crit.tsv")


def markup_sentence(s, modifiers, targets, prune_inactive=True):
    """
    """
    markup = pyConText.ConTextMarkup()
    markup.setRawText(s)
    markup.cleanText()
    markup.markItems(modifiers, mode="modifier")
    markup.markItems(targets, mode="target")
    markup.pruneMarks()
    markup.dropMarks('Exclusion')
    # apply modifiers to any targets within the modifiers scope
    markup.applyModifiers()
    markup.pruneSelfModifyingRelationships()
    if prune_inactive:
        markup.dropInactiveModifiers()
    return markup


context = pyConText.ConTextDocument()

rslts = []
for report in reports: 
  # report = reports[0]
  # print(report)
  blob = TextBlob(report.lower())
  for s in blob.sentences:
      m = markup_sentence(s.raw, modifiers=modifiers, targets=targets)
      rslts.append(m)

  # 

print (rslts)


# for r in rslts:
#     context.addMarkup(r)


# clrs = {\
#     "bowel_obstruction": "blue",
#     "inflammation": "blue",
#     "definite_negated_existence": "red",
#     "probable_negated_existence": "indianred",
#     "ambivalent_existence": "orange",
#     "probable_existence": "forestgreen",
#     "definite_existence": "green",
#     "historical": "goldenrod",
#     "indication": "pink",
#     "acute": "golden"
# }



# html.mark_document_with_html(context,colors = clrs, default_color="black")

