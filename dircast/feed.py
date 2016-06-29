from feedgen.feed import FeedGenerator

def format_itunes_duration(td):
    return "{hours:02d}:{minutes:02d}:{seconds:02d}".format(
        hours=td.seconds//3600,
        minutes=(td.seconds//60)%60,
        seconds=int(td.seconds%60)
    )

def add_entry(fg, md):
    fe = fg.add_entry()
    fe.id(md.id)
    fe.title(md.title)
    fe.enclosure(md.link, str(md.length), "audio/mpeg")
    if md.duration is not None:
        fe.podcast.itunes_duration(format_itunes_duration(md.duration))

def generate_feed(channel_dict, file_metadatas):
    fg = FeedGenerator()
    fg.load_extension("podcast")
    fg.link(href=channel_dict["url"], rel="self")
    fg.title(channel_dict["title"])
    fg.description(channel_dict["description"])

    try:
        category = channel_dict["category"]
    except KeyError:
        category = None
    try:
        subcategory = channel_dict["subcategory"]
    except KeyError:
        subcategory = None
    fg.podcast.itunes_category(category, subcategory)

    try:
        image = channel_dict["itunes_image"]
    except KeyError:
        image = None
    try:
        owner = channel_dict["itunes_owner"]
    except KeyError:
        owner = None
    try:
        owner_email = channel_dict["itunes_email"]
    except KeyError:
        owner_email = None

    fg.podcast.itunes_image(image)
    fg.podcast.itunes_owner(owner, owner_email)

    for file_metadata in file_metadatas:
        add_entry(fg, file_metadata)

    return fg.rss_str(pretty=True)

