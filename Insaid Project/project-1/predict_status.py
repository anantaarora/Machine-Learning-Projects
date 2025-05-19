# Importing packages

import pandas as pd
import numpy as np
import os
import pickle
#from feature_builder import FeatureBuilder
import configparser

#model_local_path = config["Paths"]["Train-out"]

config = configparser.ConfigParser()
config.read("luigi.cfg")
with open(config.get("Paths","Train-out"),"rb") as f:
    obj = pickle.load(f)

#with open("C:/Users/Ananta Arora/Documents/Major Project/project-1/ml_model","rb") as f:
#    obj = pickle.load(f)


def get_dataframe(json):
    df = pd.DataFrame.from_dict([dict(json)])
    return df


def assigner(di_df):

    Mnc =  ['Google','Microsoft','TCS','CTS','Wipro','Tech Mahindra','Infosys','Accenture','HCL','Deloitte','IBM','Amazon','CapGemini','Genpact']

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

    #----------------------------------------------------------------

    # South = ['Bangalore','Mysore','Chennai','Pondicherry',\
    #         'Madurai','kochi', 'Coimbatore','Hyderabad',' Thiruvananthapuram']

    # North = ['Delhi','Gurgaon',\
    #         'Faridabad','Lucknow','Meerut','Chandigarh','Srinagar',\
    #         'Ludhiana','kanpur','Varanasi','Amritsar','Aligarh','Jalandhar',\
    #         'Ghaziabad','Moradabad','Bareilly','Agra','Gwalior',\
    #         'Jabalpur','Jodhpur','Kota','Srinagar','Patna','Bhopal','Indore']

    # East = ['Patna','Allahabad','Darjeeling',\
    #         'Bhubaneshwar','Gangtok','Kohima','Tezpur','Dhubri',\
    #         'Tinsukia','Nagaon','Jorhat','Silchar','Imphal','Aizwal',\
    #         'Shillong','Dimapur','Guwuhati','Agartala']

    # West = ['Ahemdabad','Goa','Bhopal','Aurangabad',\
    #         'Lonavala','Mahabaleshwar','Mumbai','Nagpur','Nasik',\
    #         'Surat','Solapur','Thane','Pachmarhi','Rajkot','Satara']


    South = ['Kerela','Karnataka','Tamil Nadu','Telangana','Andhra Pradesh',\
            'Puducherry','Lakshadweep','Andaman and Nicobar Islands']
    North = ['Jammu and Kashmir', 'Haryana', 'Punjab', 'Uttarakhand', 'Himachal Pradesh',\
            'Delhi','Madhya Pradesh','Uttar Pradesh']
    East = ['Bihar','Jharkhand','Odisha','Assam','Meghalaya','West Bengal','Manipur',\
        'Tripura','Arunachal Pradesh', 'Mizoram','Nagaland','Sikkim','Chattisgarh']
    West = ['Gujarat','Goa','Rajasthan','Daman and Diu','Maharashtra']



    #----------------------------------------------------------------------

    df_predict = pd.DataFrame(np.zeros(19).reshape(-1,19),columns = ['engagement_score', 'age', 'marital_status', 'gender', 'experience',
        'company_size', 'department_DataBase', 'department_Finance',
        'department_HumanResources', 'department_IT', 'department_Marketing',
        'department_Operations', 'department_Other',
        'department_Research and Development', 'department_Sales', 'zone_East',
        'zone_North', 'zone_South', 'zone_West'] )

    df_predict.engagement_score = di_df.engagement_score[0]
    df_predict.age = di_df.age[0]

    if di_df.marital_status[0] == 'Single':
        df_predict.marital_status = 1
    else:
        df_predict.marital_status = 0
        
        
    if di_df.gender[0] == 'Male':
        df_predict.gender = 1
    else:
        df_predict.gender = 0
        
    df_predict.experience = di_df.experience[0]

    if di_df.company[0] in Mnc:
        df_predict.company_size = 1
    else:
        df_predict.comapny_size = 0


    if di_df.department[0] == 'DataBase':
        df_predict.department_DataBase = 1
        df_predict.department_Finance = 0
        df_predict.department_HumanResources = 0
        df_predict.department_IT = 0
        df_predict.department_Marketing = 0
        df_predict.department_Operations = 0
        df_predict.department_Other = 0
        df_predict.department_Sales = 0
        df_predict['department_Research and Development'] = 0
        
    elif di_df.department[0] == 'Finance':
        df_predict.department_DataBase = 0
        df_predict.department_Finance = 1
        df_predict.department_HumanResources = 0
        df_predict.department_IT = 0
        df_predict.department_Marketing = 0
        df_predict.department_Operations = 0
        df_predict.department_Other = 0
        df_predict.department_Sales = 0
        df_predict['department_Research and Development'] = 0
        
    elif di_df.department[0] == 'HumanResources':
        df_predict.department_DataBase = 0
        df_predict.department_Finance = 0
        df_predict.department_HumanResources = 1
        df_predict.department_IT = 0
        df_predict.department_Marketing = 0
        df_predict.department_Operations = 0
        df_predict.department_Other = 0
        df_predict.department_Sales = 0
        df_predict['department_Research and Development'] = 0
        
        
    elif di_df.department[0] == 'IT':
        df_predict.department_DataBase = 0
        df_predict.department_Finance = 0
        df_predict.department_HumanResources = 0
        df_predict.department_IT = 1
        df_predict.department_Marketing = 0
        df_predict.department_Operations = 0
        df_predict.department_Other = 0
        df_predict.department_Sales = 0
        df_predict['department_Research and Development'] = 0
        
    elif di_df.department[0] == 'Marketing':
        df_predict.department_DataBase = 0
        df_predict.department_Finance = 0
        df_predict.department_HumanResources = 0
        df_predict.department_IT = 0
        df_predict.department_Marketing = 1
        df_predict.department_Operations = 0
        df_predict.department_Other = 0
        df_predict.department_Sales = 0
        df_predict['department_Research and Development'] = 0
        
    elif di_df.department[0] == 'Operations':
        df_predict.department_DataBase = 0
        df_predict.department_Finance = 0
        df_predict.department_HumanResources = 0
        df_predict.department_IT = 0
        df_predict.department_Marketing = 0
        df_predict.department_Operations = 1
        df_predict.department_Other = 0
        df_predict.department_Sales = 0
        df_predict['department_Research and Development'] = 0
        
    elif di_df.department[0] == 'Other':
        df_predict.department_DataBase = 0
        df_predict.department_Finance = 0
        df_predict.department_HumanResources = 0
        df_predict.department_IT = 0
        df_predict.department_Marketing = 0
        df_predict.department_Operations = 0
        df_predict.department_Other = 1
        df_predict.department_Sales = 0
        df_predict['department_Research and Development'] = 0
        
    elif di_df.department[0] == 'Sales':
        df_predict.department_DataBase = 0
        df_predict.department_Finance = 0
        df_predict.department_HumanResources = 0
        df_predict.department_IT = 0
        df_predict.department_Marketing = 0
        df_predict.department_Operations = 0
        df_predict.department_Other = 0
        df_predict.department_Sales = 1
        df_predict['department_Research and Development'] = 0
        
    elif di_df.department[0] == 'Research and Development':
        df_predict.department_DataBase = 0
        df_predict.department_Finance = 0
        df_predict.department_HumanResources = 0
        df_predict.department_IT = 0
        df_predict.department_Marketing = 0
        df_predict.department_Operations = 0
        df_predict.department_Other = 0
        df_predict.department_Sales = 0
        df_predict['department_Research and Development'] = 1
        
    if di_df.city[0] in South:
        df_predict.zone_South = 1
        df_predict.zone_East = 0
        df_predict.zone_North = 0
        df_predict.zone_West = 0
        
    elif di_df.city[0] in East:
        df_predict.zone_South = 0
        df_predict.zone_East = 1
        df_predict.zone_North = 0
        df_predict.zone_West = 0
        
    elif di_df.city[0] in North:
        df_predict.zone_South = 0
        df_predict.zone_East = 0
        df_predict.zone_North = 1
        df_predict.zone_West = 0
        
    elif di_df.city[0] in West:
        df_predict.zone_South = 0
        df_predict.zone_East = 0
        df_predict.zone_North = 0
        df_predict.zone_West = 1
    # else:
    #     df_predict.zone_South = 0
    #     df_predict.zone_East = 0
    #     df_predict.zone_North = 0
    #     df_predict.zone_West = 1
        
    return df_predict



def predict(model_obj=None, dataframe_predict=None):
    #for trained_feature in trained_features:
    #    if trained_feature not in dataframe_predict.columns:
    #        dataframe_predict[trained_feature] = 0
    #dataframe_predict = dataframe_predict[trained_features]
    y_pred = model_obj.predict(dataframe_predict)
    return y_pred


def predict_status(json_data=None):
    if json_data is not None:
        df_to_predict = get_dataframe(json_data)
        dataframe = assigner(df_to_predict)
        #print('predict:',dataframe)

        result = predict(obj,dataframe)

        #print('result type:',type(result))
        #print('result shape: ',result.shape)
        #print(result)
        return result[0]
    else:
        return "No Data"



if __name__ == "__main__":
    data = {

    "engagement_score": 234,
    "age":24,
    "marital_status":"Married",
    "gender": "Female",
    "experience": "High",
    "area":"North",
    "company":"Mnc"

	}
    predict_status(data)
