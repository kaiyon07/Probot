from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'polls/Probot_Interface.html', {})
# Create your views here.



@csrf_exempt
def submit_query(request):
	name = request.POST.get('some-name')
	name = name.lower()
	ans = ''
	if name == 'hi' or  name == 'hey':
		ans = 'Hello! Probot here. Do you have any query?'
	elif name == 'hello':
		ans = 'Hi! Probot here. Do you have any query?'
	elif name=='what can you do' or name == 'what can you do'  :
		ans = 'Please check the description down :)'
	else:	
		import tensorflow as ts
		import pandas as pd
		import numpy as np
		from gensim.models import word2vec
		from gensim.models import KeyedVectors
		from sklearn.metrics import pairwise_distances
		import math
		from sklearn.feature_extraction.text import CountVectorizer
		from sklearn.feature_extraction.text import TfidfVectorizer
		from sklearn.metrics.pairwise import cosine_similarity
		import warnings
		import re
		import requests
		from bs4 import BeautifulSoup as bs

		warnings.filterwarnings("ignore")

		data=pd.read_csv(r'E:\training_data.csv')



		model = KeyedVectors.load_word2vec_format('E:\GoogleNews-vectors-negative300.bin\GoogleNews-vectors-negative300.bin', binary=True)

		vocab = model.vocab.keys()


		idf_title_vectorizer=CountVectorizer()
		idf_title_features=idf_title_vectorizer.fit_transform(data["title"])
		#it is giving the sparse matrix of dimension data points*total words in corpse
		#print(idf_title_features) working

		def n_containing(word):
		    #print(sum(1 for blob in data["title"] if word in blob.split()))
		    return( sum(1 for blob in data["title"] if word in blob.split()))

		def idf(word):
		    #print(math.log(data.shape[0]/n_containing(word)))
		    return math.log(data.shape[0]/n_containing(word))



		def avg_vec(sentence,num_feature,doc_id,m_name):
		    
		    
		    featureVec=np.zeros((num_feature,), dtype="float32")
		    nwords=0
		    
		    for word in sentence.split():
		        nwords+=1
		        if word in vocab:
		            if m_name=='weighted' and word in idf_title_vectorizer.vocabulary_:
		                #featureVec = np.add(featureVec, idf_title_features[doc_id, idf_title_vectorizer.vocabulary_[word]] * model[word])
		                print("yo")
		            elif m_name=="avg":
		                featureVec = np.add(featureVec, model[word])
		                
		    if (nwords>0):
		        featureVec=np.divide(featureVec,nwords)
		        
		    return featureVec


		 #idf model for creating word to vector
		doc_id = 0
		w2v_title_weight=[]

		for i in data['title']:
		    w2v_title_weight.append(avg_vec(i,300,doc_id,"avg"))
		    doc_id += 1
		    
		w2v_title_weight=np.array(w2v_title_weight)




		def compare_dist(sent, n_matches,final):
		    
		    pairwise_dist = pairwise_distances(w2v_title_weight, sent.reshape(1,-1))
		    
		    ind = np.argsort(pairwise_dist.flatten())[0:n_matches]
		    
		    pdists  = np.sort(pairwise_dist.flatten())[0:n_matches]

		    d_ind = list(data.index[ind])
		    
		    #print(pdists)
		    
		    for i in range(len(ind)):
		        print(data['title'].loc[d_ind[i]])
		        
		        
		    if(data['title'][d_ind[0]]=='biology research'):
		        output_var="Biology Research"
		    elif(data['title'][d_ind[0]]=='mechanical Research' or data['title'][d_ind[0]]=='mechanical Engineering' ):
		        output_var="""The areas where research is happening in this field at IITGN are:
		                        Bio-Nano Materials
		                        Combustion & Energetics
		                        Continuum Damage Mechanics
		                        Energy Systems
		                        Flow instabilities and transition to turbulence
		                        Robotics
		                        System Identification, Data-based Estimation & Analysis"""
		    elif(data['title'][d_ind[0]]=='computer science research'):
		        output_var="""The areas where research is happening in this field at IITGN are:
		        At present, the members of the CS&E are engaged broadly in the following research areas:
		        Computational complexity theory
		        Cryptography, information security and data privacy
		        Data mining, algorithms for big data and social networks
		        Machine learning and computational neuroscience
		        Computer Vision and Computational Photography
		        Computer Architecture and Distributed Systems
		        Performance Engineering"""

		    elif(data['title'][d_ind[0]]=='computer science and engineering'):
		        output_var="""    """
		        
		    elif(data['title'][d_ind[0]]=='electrical engineering research'):
		        output_var="""The areas where research is happening in this field at IITGN are:
		        Cost-effective integration of 20-40V n/p LDMOS devices in SCL's 0.18um CMOS process
					Extended Depth of Field Imaging using Coded Camera Architecture
					Printed Document Security Using Intrinsic Characteristics of Imaging Devices
					Integrating Robotic Gait Training System with Virtual Reality for Gait Rehabilitation - a novel approach in Neurorehabilitation
					Towards ultra-thin optical wavefront manipulation devices based on all-dielectric high-efficiency transmissive metasurfaces: demonstration of beam focusing and investigation of polychromatic designs.
					Intelligent Adaptive Reality based Stoke Rehabilitation Platform for Elderly
					Post Stroke tele-neurohabilitation using an operant conditioning paradigm under volitionally driven transcutaneous neuromuscular electrical stimulation
					Design and development of a low cost binaural hearing aid
					Investigation of Object Motion Categories in Dynamic Natural Scenes and their Applications
					Development of low cost intelligent headphones for improving social interactions of children with autism spectrum disorders
					"""
		    elif(data['title'][d_ind[0]]=='civil engineering research'):
		        output_var="""The areas where research is happening in this field at IITGN are:
		        Joint Development of Low cost Automatic Triaxial Apparatus
			River Basin scale Hydrological investigation & characterization using Variable Infiltration capacity Model
			Hydrologic Modelling and Climate Change Impact Assessment in the Ganga River Basin
			Measurement to management (M2M): improved water use efficiency and agricultural productivity through experimental sensor network
			Implications of land cover/land use and climate changes on soil moisture variability in India
			Characterization of Rotational Seismic Excitation
			Virtual geotechnical laboratory
			Development of a rapid visual assessment method for seismic assessment of RC frame buildings in India """
		    elif(data['title'][d_ind[0]]=='material science research' or data['title'][d_ind[0]]=='material science and engineering'):
		        output_var="""The areas where research is happening in this field at IITGN are:
		        Transparent conductors
		Thin film solar cells
		Interface thermodynamics and kinetics
		Oxidation
		Solid -Solid interfaces structure
		Interface thermodynamics and kinetics
		Grain boundary dynamics
		Friction stir welding
		Heat transfer and visco-plastic flow
		Mineral Processing and Process Metallurgy
		Transport Phenomena
		Extractive Metallurgy.
		Thermodynamic modeling of materials
		Kinetic modeling of metallurgical processes such as solidification and diffusion
		Application of thermodynamic modeling to industrial processes
		Mathematical Modelling & Simulation
		Process Design and Development
		Process Control in Mineral Processing and Extractive Metallurgy
		Numerical modeling of joining processes
		"""
		    elif(data['title'][d_ind[0]]=='chemical research'):
		        output_var=""""chemical research
			Aiming to be a center for pioneering research and innovation the chemistry discipline at IIT-Gn is home to fundamental and applied research in the areas of asymmetric catalysis, applied biochemistry, drug discovery, medicinal chemistry, organic photochemistry, synthetic pigments, materials catalysis and computational chemistry. The research lines in the discipline are driven the faculty who bring with them years of research experience and international exposure.

		With a strong focus on interdisciplinary research the discipline is engaged in active collaboration with other disciplines at IIT-Gn and institutes across India and around the world."""
		    elif(data['title'][d_ind[0]]=='professor'):
		        output_var="The Profs are very good here."
		    elif(data['title'][d_ind[0]]=='biological engineering'):
		        output_var="""Biological Engineering
		The discipline of Biological Engineering at IITGN was started in 2012 with a Ph.D. program. The discipline currently hosts research activities which can be broadly classified into:

		Peptide therapeutics and protein misfolding
		Protein biochemistry and molecular biology
		Neuroscience and Neurobiology
		Neurodegenerative disorders and movement disorders
		Macromolecular X-ray Crystallography
		Cancer Biology
		The research facilities, which are continously being upgraded, currently include:

		Fully equipped molecular biology and cell culture lab
		NMR (500 MHz)
		Fluorimeter
		AKTA-FPLC
		Inverted fluorescence microscope
		peptide synthesizer
		Ultracentrifuge
		Microplate reader
		LC-MS/MS
		AFM
		SEM
		CD"""
		    elif(data['title'][d_ind[0]]=='chemsitry'):
		        output_var="Research in the field of Chemsitry"
		    elif(data['title'][d_ind[0]]=='chemical engineering'):
		        output_var="""Chemical Engineering
		The discipline of Chemical Engineering at IITGN was started in 2009 with undergraduate and Ph.D. programs and was expanded in 2011to include an M.Tech degree program in Chemical Engineering. The discipline currently hosts research activities which can be broadly classified into:

		Nanosciences, Colloidal Sciences, Polymer Sciences
		Pharmaceutical Processing
		Process Design, Process Systems Engineering, Process Safety
		Crystallization
		The research facilities, which are continously being upgraded currently include:

		A range of wet lab equipment
		High Performance Computing facilities
		Inverted Fluorescence Microscope
		XRD
		AFM
		FESEM
		Zeta Sizer
		In order to meet current and future research and teaching requirements, the discipline of Chemical Engineering at IIT Gandhinagar seeks outstanding applicants from all areas of Chemical Engineering to fill multiple positions at all levels.

		For queries or information regarding faculty recruitment specifically in Chemical Engineering at IITGN, please contact Prof. Kaustubh Rane [kaustubhrane@iitgn.ac.in]. For general questions related to faculty recruitment at IITGN, please write to faculty.recruitment@iitgn.ac.in"""
		        
		    elif(data['title'][d_ind[0]]=='civil engineering'):
		        output_var="""The areas where research is happening in this field at IITGN are:
		        Joint Development of Low cost Automatic Triaxial Apparatus
			River Basin scale Hydrological investigation & characterization using Variable Infiltration capacity Model
			Hydrologic Modelling and Climate Change Impact Assessment in the Ganga River Basin
			Measurement to management (M2M): improved water use efficiency and agricultural productivity through experimental sensor network
			Implications of land cover/land use and climate changes on soil moisture variability in India
			Characterization of Rotational Seismic Excitation
			Virtual geotechnical laboratory
			Development of a rapid visual assessment method for seismic assessment of RC frame buildings in India """
		    
		    elif(data['title'][d_ind[0]]=="electrical engineering"):
		        output_var="""The areas where research is happening in this field at IITGN are:
		        Cost-effective integration of 20-40V n/p LDMOS devices in SCL's 0.18um CMOS process
					Extended Depth of Field Imaging using Coded Camera Architecture
					Printed Document Security Using Intrinsic Characteristics of Imaging Devices
					Integrating Robotic Gait Training System with Virtual Reality for Gait Rehabilitation - a novel approach in Neurorehabilitation
					Towards ultra-thin optical wavefront manipulation devices based on all-dielectric high-efficiency transmissive metasurfaces: demonstration of beam focusing and investigation of polychromatic designs.
					Intelligent Adaptive Reality based Stoke Rehabilitation Platform for Elderly
					Post Stroke tele-neurohabilitation using an operant conditioning paradigm under volitionally driven transcutaneous neuromuscular electrical stimulation
					Design and development of a low cost binaural hearing aid
					Investigation of Object Motion Categories in Dynamic Natural Scenes and their Applications
					Development of low cost intelligent headphones for improving social interactions of children with autism spectrum disorders
					"""
		        
		    elif(data['title'][d_ind[0]]=='humanities'):
		        output_var="The discipline of Humanities and Social Sciences at IITGN was started in 2009 with a Ph.D. program. In 2014, a Master’s (M.A.) program in Society and Culture was started under the aegis of the Humanities and Social Sciences discipline. The discipline currently hosts research activities which can be broadly classified into: South Asian studies, Region studies, Population studies, Translation studies, Political science, Public health, Cognitive Science, Archaeology and Archaeological Sciences"
		    elif(data['title'][d_ind[0]]=='about iit gandhinagar'):
		        output_var="The Indian Institute of Technology Gandhinagar strives to offer the best undergraduate and graduate education in India with unmatched innovations in curriculum. The institute promotes critical thinking and an appreciation of the interdisciplinary character of knowledge, with an emphasis on the liberal arts, project oriented learning, compulsory courses in design and the life sciences, diversity and globalization. The five-week immersion Foundation Programme for all new undergraduate students was recognized with the World Education Award 2013 by the World Education Summit for innovations in engineering education. Nearly a quarter of its undergraduate students receive study abroad experience during their academic career.  IIT Gandhinagar is committed to promoting excellence in science, technology, as well as the humanities and social sciences and to the development of rounded and nuanced minds."
		    
		    #return(output_var)
		    elif(data['title'][d_ind[0]]=='hi' or data['title'][d_ind[0]]=='hey there'):
		        output_var="hey "
		    elif(data['title'][d_ind[0]]=='hello'):
		        output_var="yo"
		    elif(data['title'][d_ind[0]]=='hey'):
		        output_var="hi"
		    
		    for k in final:
		        if (data['title'][d_ind[0]]==k[0]):
		            h="Name of professor- "+k[0]+"\n"+"Department- "+k[1]+"\n"+"Qualification- "+k[2]+"\n"+"Email- "+k[3]+"\n"+"Reserach interest"+k[4]
		            output_var=h
		            
		            
		        
		    return(output_var)

		l0 = ['faculty/biology/virupakshi.htm','faculty/chemistry/bhaskar.htm','faculty/chemical/sameer.htm','faculty/civil/dhiman.htm','faculty/comp/manu.htm','faculty/earth-sciences/vikrant.htm','faculty/electrical/arup.htm','faculty/humanities/sharmitalahiri.htm','faculty/maths/indranath.htm','faculty/mechanical/atul.htm','faculty/mems/emila.htm','faculty/physics/krishna.htm','faculty/Social%20Sciences/ambika.htm']
		l01 = {}
		final = [['Name','Department','Post','Qualification','Email','Research Interests']]
		for ns in l0:
			lm= []
			r1 = requests.get("http://www.iitgn.ac.in/" + ns)
			soup = bs(r1.content,"html.parser")
			x = soup.find_all('h2', {'class':'title block-title'})
			x1 = str(x[0])
			x1 = x1[x1.find('>')+1:x1.rfind('<')]
			y = soup.find_all('ul', {'class':'menu'})
			z = re.findall(r'pdrf.+?(?=")',str(y[0]))
			z1 = re.findall(r'faculty.+?(?=")',str(y[0]))
			lm+=z+z1
			for ns1 in lm:
				r2 = requests.get("http://www.iitgn.ac.in/" + ns1)
				soup1 = bs(r2.content,"html.parser")
				p = soup1.text.strip()
				l = p.split("\n")
				flag = 0
				l1 =[]
				for i in l:
					i = i.strip()
					if i[:7] == "You are":
						flag = 1
					if i[:5]=='Work ' or i[:5] == 'Award' or i[:5] == 'Paten':
						break
					if flag==1:
						if i.strip()!='':
							l1.append(i.strip())
					else:
						continue
				if 'Personal Webpage' in l1:
					l1.remove('Personal Webpage')
				if 'Personal Website' in l1:
					l1.remove('Personal Website')
				if l1[1] not in l01:
					l01[l1[1]]= len(l01)+1
					qual = l1[3]
					i1=0
					i2=0
					for el in l1[4:]:
						if el[:5]=='Email':
							i1 = l1.index(el)
							break
						elif el[:5] == 'Resea' or el[:5] =='Area ':
							i2 =  l1.index(el)
							break
						else:
							qual+=', ' + el
					if i1!=0:
						if l1[i1][-1]=='e':
							email = l1[i1][l1[i1].find(" ")+1:l1[i1].find("P")]
						else:
							email = l1[i1][l1[i1].find(" ")+1:]
						ri=l1[i1+2]
						for el1 in l1[i1+3:]:
							ri+=', '+el1
					elif i2!=0:
						email = '-'
						ri=l1[i2+1]
						for el1 in l1[i2+2:]:
							ri+=', '+el1
					else:
						email = '-'
						ri = '-'
					final.append([l1[1],x1,l1[2],qual,email,ri])
				else:
					final[l01[l1[1]]][1]+=", " + x1

		for k in final:
		    k[0]=k[0].lower()





		def sentence_avg_vector(query,num_feature):
		    
		    f_Vec = np.zeros((num_feature,), dtype="float32")
		    n_w = 0
		    
		    for word in query.split():
		        n_w += 1
		        if word in vocab:
		            f_Vec = np.add(f_Vec, model[word])
		    if(n_w>0):
		        f_Vec = np.divide(f_Vec, n_w)
		    
		    return f_Vec





		vector=sentence_avg_vector(name,300)
		ans=(compare_dist(vector,100,final))




		    
		    
		    


		    
		    

	return render(request, 'polls/Probot_Interface.html', { 'answer': ans })