class univariate():

    def QuanQual(dataset):
        Qual = []
        Quan = []
        for ColumnName in dataset.columns:
            if dataset[ColumnName].dtype == "O":
                Qual.append(ColumnName)
            else:
                Quan.append(ColumnName)
        return Qual,Quan


