import re
def get_mongo_query(query):
    if validate(query):
        #print 'Right query'
        print query
        mongo_query = handle(query)
        return True,mongo_query
        '''
        if len(mongo_query) > 1:
            peeps =  devices.find(mongo_query[0],mongo_query[1])
        else:
            peeps =  devices.find(mongo_query[0])

        #peeps1 = device.find({'$and':[{"$or":[{"Company":"Samsung"},{"Company":"Motorola"}]},{'OS':{'$regex':'.*Android.*'}}]},{'Company':1,'OS':1})
        
        #print peeps1.count()
        #for each_elem in peeps1:
            #print each_elem
        #peeps1 =  peoplea.find({'frontcamera': {'$lt':12}})
        print peeps.count()
        '''
    else:
        return False,"Wrong Query"
    

def validate(query_string):
    
                
		#SELECT mobiles FROM Samsung WITH operatingsystem = windows
                #select_clause = "(operatingsystem|talktime|type|GPS|price|rearcamera|frontcamera|thickness|company|all)"
                regex0 = "SELECT "
                regex1 = "(OS|Talk time|type|all|Company|GPS|Brand|Image)"
                regex2 = " FROM (\w* )(OR (\w*) )*WITH "
                regex3 = "(OS|Talk time|Price group|type|GPS|price|rearcamera|frontcamera|thickness|Company|Bluetooth|GPRS|Brand) (=|>|<|:) (\w*)"
                query_pattern = regex0 + regex1 + "( AND " + regex1 + ")*" + regex2 + regex3 + "( AND " + regex3 + ")*"
		#print query_pattern
                m = re.match(query_pattern,query_string)
                if m:
                    return True
                else:
                    return False


def handle(query_string):
    
    required_data = {}
    company_string = query_string[query_string.find('FROM') + len('FROM') + 1:query_string.find('WITH')].strip()
    print company_string
    companies_list = company_string.replace(" ","").split('OR')
    print companies_list
    
    #print 'The Company is', required_data['Company']
    required_data['Company'] = companies_list
    required_data['required_features'] = []
    features_list = query_string[query_string.find('W') + 5:].strip().split('AND')
    print 'Features List:', features_list
    select_clause = query_string[query_string.find('SELECT') + len('SELECT') + 1:query_string.find('FROM')].strip()
    print 'Select_Clause' , select_clause
    select_clause_list = select_clause.replace(" ","").split('AND')
    

    for eachFeature in features_list:
        eachFeature = eachFeature.lstrip().rstrip()
        if '=' in eachFeature:
            operator = '='
        
        elif '>' in eachFeature:
            operator = '>'
        elif '<' in eachFeature:
            operator = '<'
        elif ':' in eachFeature:
            operator = ':'
        feature_details = {}
        temp = eachFeature.split(operator)
        feature_details[temp[0]] = operator + temp[1]
        required_data['required_features'].append(feature_details)
        #print eachFeature
    #print 'dict'
    #print required_data
    li = answer(required_data,select_clause_list)
    return li
def answer(required_data,select_clause):
    find_company = {}
    select_clause_dict ={}
    final_dict = {}
    find_list = []
    for each_key in required_data:
        if not 'all' in required_data['Company']:
            OR_dict = {}
            or_list = []
            for each_elem in required_data['Company']:
                or_dict = {}
                or_dict['Company'] = each_elem
                or_list.append(or_dict)
            find_company['$or'] = or_list
            find_list.append(find_company)
            #del find_dict['company']
            
        if required_data.has_key('required_features'):
            for each_dict in required_data['required_features']:
                #print each_dict , 'These r the dicts'
                feature_names = each_dict.keys()
                for each_feature_name in feature_names:
                    find_dict = {}
                    outer_dict = {}
                    if '<' in each_dict[each_feature_name]:
                        number = each_dict[each_feature_name].split('<')
                        find_dict['$lt'] = int(number[1])
                        outer_dict[each_feature_name.strip()] = find_dict
                        find_list.append(outer_dict)
        
                    elif '>' in each_dict[each_feature_name]:
                        number = each_dict[each_feature_name].split('>')
                        find_dict['$gt'] = int(number[1])
                        outer_dict[each_feature_name.strip()] = find_dict
                        find_list.append(outer_dict)
                        
                    elif '=' in each_dict[each_feature_name]:
                        number = each_dict[each_feature_name].split('=')
                        find_dict[each_feature_name] = int(number[1])
                        
                        find_list.append(find_dict)
                        
                    else:
                        field = each_dict[each_feature_name].split(':')
                        find_dict[each_feature_name] = field[1]
                        outer_dict['$regex'] = '.*' + find_dict[each_feature_name].lstrip(' ').rstrip(' ') + '.*'
                        utmost_outer_dict = {}
                        utmost_outer_dict[each_feature_name.rstrip(' ').lstrip(' ')] = outer_dict
                        find_list.append(utmost_outer_dict)

    
    if len(find_list) > 1:        
        final_dict['$and'] = find_list
        #print final_dict
    else:
        final_dict = find_list[0]

    if 'all' not in select_clause:
        for each_elem in select_clause:
            select_clause_dict[each_elem] = 1
        select_clause_dict['Image'] = 1
        select_clause_dict['Brand'] = 1
        final_list = []
        final_list.append(final_dict)
        final_list.append(select_clause_dict)
        print " MONGODB QUERY"
        print final_list
        return final_list
    else:
        final_list = []
        final_list.append(final_dict)
        print final_list
        return final_list


def main():
    query = raw_input("Enter the query\n")
    print get_mongo_query(query)
if __name__ =="__main__":
    main()
