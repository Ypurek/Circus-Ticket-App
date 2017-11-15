from .forms import AddPerformanceForm


def performance_to_json(performance):
    feature_list = []
    for feature in performance.features.filter():
        feature_list.append(feature.feature)
    return {'id': performance.id,
            'date': performance.date,
            'time': performance.time,
            'description': performance.description,
            'price': performance.price,
            'features': feature_list,
            'ticketsNumber': performance.tickets.count()}
