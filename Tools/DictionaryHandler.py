def query_dictionary(data, query):
    if not data:
        return {}

    if not query:
        return data

    results = {}
    query_results = {}
    query_counter = 0
    for query_key, query_value in query.items():
        # For each query, iterate dictionary
        query_results[query_counter] = {}
        for data_key, data_value in data.items():
            if data_value[query_key] == query_value:
                query_results[query_counter].update({data_key: data_value})
        if not query_counter == 0:
            previous_counter = query_counter - 1
            results = query_results[previous_counter].keys() & query_results[query_counter].keys()
        else:
            results = query_results[query_counter].keys()
        query_counter = query_counter + 1
    response = {}
    for result in results:
        response[result] = data[result]

    return response
