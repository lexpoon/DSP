        print(feature_correct_dict.get(feature))

        if len(features) == 1:
            if performance >= 0.7:
                feature_correct_dict[feature] = feature_correct_dict.get([feature]) + 1
            else:
                feature_incorrect_dict[feature] = feature_incorrect_dict.get([feature]) + 1
        else:
            if performance >= 0.5:
                feature_correct_dict[feature] = feature_correct_dict.get([feature]) + 1
            else:
                feature_incorrect_dict[feature] = feature_incorrect_dict.get([feature]) + 1
    print(feature_correct_dict)
    return feature_correct_dict, feature_incorrect_dict
