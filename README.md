# bio2bioes

First, git clone the src!

You can replace the 'bio' file to your raw bio data
> Warning: your data format must be adjust as the same as "my bio file data format"


Try follow code for test:  

    from bio2bioes import DataDeal
    dd = DataDeal('bio')
    data_list, label_list = dd.reform_data()                    # preprocessing the raw data
    bioes_data_label = dd.dict_or_list(data_list, label_list)   # bio2bioes
