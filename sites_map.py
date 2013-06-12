from inspections import application as app

def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        links.append(rule)
    return links

if __name__ == '__main__':
    site_map()
