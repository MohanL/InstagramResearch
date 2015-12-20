from stemming.porter2 import stem
import nltk
print "SnowballStemmer english"
sno = nltk.stem.SnowballStemmer('english')
print sno.stem('grows')
print sno.stem('leaves')
print sno.stem('fairly')

print "---------------------------------------------------------------------------------"
print "PorterStemmer"
ps = nltk.stem.porter.PorterStemmer()
print ps.stem('grows')
print ps.stem('leaves')
print ps.stem('fairly')

print "---------------------------------------------------------------------------------"
print "LancasterStemmer"
st = nltk.stem.lancaster.LancasterStemmer()
print st.stem('grows')     
print st.stem('leaves')
print st.stem('fairly')

print "---------------------------------------------------------------------------------"
print "WordNetlemmatizer"
lemma = nltk.stem.WordNetLemmatizer()
print lemma.lemmatize('grows')
print lemma.lemmatize('leaves')
print lemma.lemmatize('fairly')

print "---------------------------------------------------------------------------------"
print "porter2"
print stem('grows')     
print stem('leaves')
print stem('fairly')
