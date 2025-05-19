import pandas as pd


class FeatureBuilder():
    def __init__(self, dataframe,training=True):
        self.dataframe = dataframe
        self.dataframe = self.dataframe.rename(columns={'Name': 'name','Mobile Number':'mobile_number','Email Address': 'email_address',\
            'EngagementScore':'engagement_score','Company' : 'company','Age':'age','MaritalStatus':'marital_status',\
            'gender':'gender','Exp' :'experience','Interested':'interested','department':'department','City':'city'})

        self.dataframe.drop(['name','mobile_number', 'email_address'], axis =1,inplace = True)
        self.continuous_features = ['engagement_score', 'age','experience']
        self.categorical_features = ['company', 'marital_status', 'gender','department', 'city']
        self.target = ['interested']
        self.training=training

    def featurize(self):
        print("Subsetting Dataframe")
        self.subset_dataframe()
        interested_map = {'Yes': 1, 'No': 0 }
        self.dataframe['interested'] = self.dataframe['interested'].map(interested_map)
        self.dataframe["company_size"] = None

        Mnc =  ['Google','Microsoft','TCS','CTS','Wipro','Tech Mahindra','Infosys','Accenture','HCL','Deloitte','IBM',\
            'Amazon','CapGemini','Genpact']

        small_companies = ['VeServ','Eclature Technologies','Harini Informatics','Info Edge Solutions',\
                        'Hi Caliber IT Solutions','Brio Technologies Private Limited','I2Space Technologies', \
                        'Jaro Education','Omniscient IT Solutions Pvt Ltd','Esalemedia','Askmeguru',\
                        'Metacube Software Pvt. Ltd','Accuracy','Mindtree','IntelloLabs','Intelex Systems'\
                        ,'Sopra Steria','IBrand Solutions','Team Embedded','Cravaka Info Systems','Brihaspathi Technologies'\
                        'MBR Informatics','Impecsoft Solutions','Innvectra Softech','Yana Software Private Limited'\
                        'Olympiasoft','Techno Brain Ltd','Software Solutions','EON Technologies','Rapidsoft Technologies Pvt Ltd',\
                        'Toshiba Software India Pvt ltd', 'Embassy IT Solutions']
        small_companies2 =  ['Gayatri Software Services Pvt Ltd','Sonata Software Limited', 'Deforay Technologies Pvt. Ltd',\
                            'ZOVIL TECHNOLOGIES', 'Aspire Software Solutions','Pramati Technologies','Hakuna Matata Solutions',\
                            'Prodapt Solutions Pvt Ltd','I S INFOTECH PVT LTD','Gislen Software','OG Software Solutions India Pvt Ltd',\
                            'CA Technologies','Infotech Enterprises','Persistent Systems','Mahindra Satyam']

        small = small_companies + small_companies2

        for i in range(self.dataframe.shape[0]):
            if self.dataframe.iloc[i,3] in Mnc:
                self.dataframe.iloc[i,9] = 1
            else:
                self.dataframe.iloc[i,9] = 0

        self.dataframe = self.dataframe.drop('company', axis = 1)

        gender_map = {'Male': 1, 'Female': 0 }
        self.dataframe['gender'] = self.dataframe['gender'].map(gender_map)
        
        marital_map = {'Single': 1, 'Married': 0 }
        self.dataframe['marital_status'] = self.dataframe['marital_status'].map(marital_map)

        self.dataframe = self.dataframe.sample(frac=1).reset_index(drop=True)

        South = ['Bangalore','Mysore','Chennai','Pondicherry',\
                'Madurai','kochi', 'Coimbatore','Hyderabad',' Thiruvananthapuram']

        North = ['Delhi','Gurgaon',\
                'Faridabad','Lucknow','Meerut','Chandigarh','Srinagar',\
                'Ludhiana','kanpur','Varanasi','Amritsar','Aligarh','Jalandhar',\
                'Ghaziabad','Moradabad','Bareilly','Agra','Gwalior',\
                'Jabalpur','Jodhpur','Kota','Srinagar','Patna','Bhopal','Indore']

        East = ['Patna','Allahabad','Darjeeling',\
                'Bhubaneshwar','Gangtok','Kohima','Tezpur','Dhubri',\
                'Tinsukia','Nagaon','Jorhat','Silchar','Imphal','Aizwal',\
                'Shillong','Dimapur','Guwuhati','Agartala']

        West = ['Ahemdabad','Goa','Bhopal','Aurangabad',\
                'Lonavala','Mahabaleshwar','Mumbai','Nagpur','Nasik',\
                'Surat','Solapur','Thane','Pachmarhi','Rajkot','Satara']

        self.dataframe['zone'] = None

        for i in range(self.dataframe.shape[0]):
            if self.dataframe.iloc[i,6] in South:
                self.dataframe.iloc[i,9] = 'South'
            
            elif self.dataframe.iloc[i,6] in North:
                self.dataframe.iloc[i,9] = 'North'
                
            elif self.dataframe.iloc[i,6] in East:
                self.dataframe.iloc[i,9] = 'East'
                
            elif self.dataframe.iloc[i,6] in West:
                self.dataframe.iloc[i,9] = 'West'

            else:
                self.dataframe.iloc[i,9] = 'West'

        self.dataframe.drop('city',axis = 1, inplace = True)

        dataframe = pd.get_dummies(self.dataframe)

        #print(dataframe.head())
        return dataframe


    def subset_dataframe(self):
        if self.training:
            self.dataframe = self.dataframe[self.continuous_features+self.categorical_features+self.target]
        else:
            self.dataframe = self.dataframe[self.continuous_features + self.categorical_features]

