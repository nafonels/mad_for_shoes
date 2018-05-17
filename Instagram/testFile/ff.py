import requests


def connect_main():
    tag = "plebiscito"
    links_photos = []
    links2_photos = []
    links3_photos = []  # Save all links of ID.
    main_page_tag = ("https://www.instagram.com/explore/tags/%s/?__a=1" % tag)

    if (flag):
        url_get = requests.get(main_page_tag)
        load_json = json.loads(url_get.text)
        end_cursor = load_json['tag']['media']['page_info']['end_cursor']
        next_page = ("https://www.instagram.com/explore/tags/%s/?__a=1&%s" % (
        tag, end_cursor))
        count = 0
        while count < 40:
            try:
                # print(load_json['tag']['media']['nodes'][count]['code'])
                # print(load_json['tag']['top_posts']["nodes"][count]['code'])
                links_photos.append(
                    load_json['tag']['media']['nodes'][count]['code'])
                links2_photos.append(
                    load_json['tag']['top_posts']["nodes"][count]['code'])
                count = count + 1
            except:
                count = count + 1

        # for save in load_json['tag']['media']['nodes'][count]['code']:
        # print(save)
        # Guardamos en la lista el ID de la foto, por ejemplo BMMbJkRAQfX, BMMbJkRAQfX, BMMZpRAg_Gn.
        # links_photos.append(save)
        for node1 in links_photos:
            links3_photos.append(node1)
        for node2 in links2_photos:
            links3_photos.append(node2)
        # for nodes in links3_photos:
        #    print(mirar)
        get_comments_data(links3_photos)

    else:
        # flag_id = True
        links_photos_next = []
        links2_photos_next2 = []
        links3_photos_nodes = []  # Save all links of ID.
        # url_get = requests.get(next_page)
        # if(flag_id)
        url_get = requests.get(next_page)
        iterate_max_ids(next_page)
        url_get = requests.get(
            "https://www.instagram.com/explore/tags/%s/?__a=1&%s" % (
            tag, end_cursor_update))
        load_json2 = json.loads(url_get.text)
        count = 0
        while count < 40:
            try:
                # print(load_json['tag']['media']['nodes'][count]['code'])
                # print(load_json['tag']['top_posts']["nodes"][count]['code'])
                links_photos_next.append(
                    load_json2['tag']['media']['nodes'][count]['code'])
                links2_photos_next2.append(
                    load_json2['tag']['top_posts']["nodes"][count]['code'])
                count = count + 1
            except:
                count = count + 1

        # for save in load_json['tag']['media']['nodes'][count]['code']:
        # print(save)
        # Guardamos en la lista el ID de la foto, por ejemplo BMMbJkRAQfX, BMMbJkRAQfX, BMMZpRAg_Gn.
        # links_photos.append(save)
        for node1 in links_photos_next:
            links3_photos.append(node1)
        for node2 in links2_photos_next2:
            links3_photos_nodes.append(node2)
        # for nodes in links3_photos:
        #    print(mirar)
        get_comments_data(links3_photos_nodes)