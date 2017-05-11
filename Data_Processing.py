def filteredResults(companies, critDict):
    # Create a deep copy we can change
    filteredCompanies = copy.deepcopy(companies)
    for company in companies:
        deleteCompany = False
        if critDict["URL"].get() == 1:
            if company["URL"] == "NA":
                deleteCompany = True
        if critDict["Email"].get() == 1 and deleteCompany is False:
            if company["Email"] == "NA":
                deleteCompany = True
        if critDict["Phone"].get() == 1 and deleteCompany is False:
            if company["Phone"] == "NA":
                deleteCompany = True
        if critDict["Founding date"].get() == 1 and deleteCompany is False:
            if company["Founding date"] == "NA":
                deleteCompany = True
        if critDict["Employees"].get() == 1 and deleteCompany is False:
            if company["Employees"] == "NA":
                deleteCompany = True
        if critDict["Description"].get() == 1 and deleteCompany is False:
            if company["Description"] == "NA":
                deleteCompany = True
        if critDict["Revenue"].get() == 1 and deleteCompany is False:
            if company["Revenue"] == "NA":
                deleteCompany = True
        if critDict["Associates"].get() == 1 and deleteCompany is False:
            if company["Associates"] == ["NA"]:
                deleteCompany = True

        if deleteCompany:
            filteredCompanies.remove(company)

    return filteredCompanies