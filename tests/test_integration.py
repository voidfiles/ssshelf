from datetime import datetime
from itertools import permutations
import simpleflake
import json

from strainer import (serializer, field, child, multiple_field,
                      formatters, validators,
                      ValidationException)
from strainer.formatters import export_formatter
from strainer.validators import export_validator
from ssshelf.items import ItemManager
from ssshelf.collections import Collection
from ssshelf.utils import convert_datetime_to_str, json_dump
from ssshelf.manager import Manager
from ssshelf.storages.inmemory import InMemoryStorage

# Item stuff
base_fields = [
  field('link', validators=[validators.required()]),
  multiple_field('tags'),
  field('created_at',
        validators=[validators.datetime()],
        formatters=[formatters.format_datetime()]),
]

bookmark_create_schema = serializer(*[
    field('pk'),
] + base_fields)

bookmark_update_schema = serializer(*[
    field('pk', validators=[validators.required(), validators.integer()]),
] + base_fields)


def create_bookmark(data, created_at=None):
    bookmark = bookmark_create_schema.deserialize(data)
    bookmark['pk'] = simpleflake.simpleflake()
    if created_at:
        bookmark['created_at'] = validators.datetime()(created_at)
    else:
        bookmark['created_at'] = datetime.utcnow()

    return bookmark

# Item Manager


class Bookmark(ItemManager):
    def get_pk(self, item):
        return str(item['pk'])

    def serialize_item(self, item):
        return bytes(json_dump(item), 'utf8')

    def deserialize_item(self, data):
        return json.loads(data)


class AllBookmarks(Collection):
    def get_pk(self, item):
        return str(item['pk'])

    def key(self, item):
        print(item['created_at'])
        return convert_datetime_to_str(item['created_at'])


class TaggedBookmarks(Collection):
    def get_pk(self, item):
        return str(item['pk'])

    def key(self, item):
        tag_combos = []

        tags = [x.lower() for x in item.get('tags', [])]

        tags = sorted(tags)

        possible_tag_combos = list(permutations(tags, r=2))
        possible_tag_combos += list(permutations(tags, r=3))
        possible_tag_combos += [tuple([x]) for x in tags]

        for combo in possible_tag_combos:
            clean_combo = tuple(sorted(combo))
            if clean_combo not in tag_combos:
                tag_combos.append(clean_combo)
                yield clean_combo


class BookmarkManager(Manager):
    item_manager = Bookmark()


def create_bookmarks():
    return [
        create_bookmark({"link": "http://aftertheflood.co/projects/atf-spark", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://www.kalzumeus.com/2017/09/09/identity-theft-credit-reports/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/fastcompany/status/907952827858911232", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/FastCompany/status/907952827858911232", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://medium.com/startup-grind/what-every-software-engineer-should-know-about-search-27d1df99f80d", "tags": ['search', 'artificial-intelligence', 'natural-language-processing', 'MAX-GRIGOREV']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/i/web/status/907701103281807362", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/concreteniche/status/907700055817289728/photo/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/mic/status/907367576816074752/video/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://faviconographer.com/", "tags": ['software', 'mac', 'safari', 'favicon']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.sublimetext.com/blog/articles/sublime-text-3-point-0", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://lite.cnn.io/en", "tags": ['Irma']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.fastcompany.com/40466047/two-ex-googlers-want-to-make-bodegas-and-mom-and-pop-corner-stores-obsolete", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.buzzfeed.com/bensmith/theres-blood-in-the-water-in-silicon-valley", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/blackmirror/status/907695792202317832/photo/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://krebsonsecurity.com/2017/09/ayuda-help-equifax-has-my-data/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://comp.social.gatech.edu/papers/cscw18-chand-hate.pdf", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://blog.jessfraz.com/post/windows-for-linux-nerds/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://fillmem.com/post/fast-secured-and-free-static-site/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://developer.apple.com/videos/play/fall2017/801/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://bradfrost.com/blog/post/facebook-you-needy-sonofabitch/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.newyorker.com/news/john-cassidy/a-new-way-to-learn-economics", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/thehill/status/908047394062958592", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/tomgauld/status/907176391959080960/photo/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/vojtastavik/status/907911237983449088/video/1", "tags": ['iphoneX']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/mic/status/907367576816074752", "tags": ['InsecureHBO']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.recode.net/2017/9/13/16299086/apple-park-steve-jobs-theater-iphone-event-photos", "tags": ['SteveJobsTheater']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.theverge.com/2017/9/11/16290730/equifax-chatbots-ai-joshua-browder-security-breach", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://www.paulplowman.com/stuff/house-address-twins-proximity/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://blog.atom.io/2017/09/12/announcing-atom-ide.html", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://gridlesskits.com/2017/09/06/burning-man-update.html", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.theuncomfortable.com/", "tags": ['design']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/motherofincest/status/907082650653020162", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.gq.com/story/harrison-ford-gq-cover-story-2017", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/jonjones/status/907339393379311617/photo/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://www.craigkerstiens.com/2017/09/10/better-postgres-migrations/", "tags": ['postgres', 'tips', 'database', 'sql']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/AM2DM/status/907314669655916544/video/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/nypost/status/907248567563276289", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.nytimes.com/2017/09/11/opinion/equifax-accountability-security.html", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/GWillowWilson/status/907396999338647552", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/dog_rates/status/775410014383026176", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/thedailybeast/status/907229570436403200", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.cl.cam.ac.uk/~lp15/MLbook/pub-details.html", "tags": ['book', 'ml', 'sml', 'programming', 'free', 'computerscience']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://dougvitale.wordpress.com/2011/12/21/deprecated-linux-networking-commands-and-their-replacements/", "tags": ['linux', 'network']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://blog.sessionstack.com/how-javascript-works-memory-management-how-to-handle-4-common-memory-leaks-3f28b94cfbec", "tags": ['javascript', 'programming', 'memory', 'profdev']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.theatlantic.com/magazine/archive/2017/10/will-donald-trump-destroy-the-presidency/537921/", "tags": ['IFTTT', 'tokindlelite39']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://bleacherreport.com/articles/2732670-colin-kaepernick-anthem-race-in-america", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/ComicPrintingUK/status/907714163564273664/photo/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://www.hollywoodreporter.com/features/curb-your-enthusiasm-oral-history-larry-david-crazy-auditions-art-cringe-1036626", "tags": ['Archive']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/internetofshit/status/907558038881669120/photo/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/Attenboroughs_D/status/907510344226152448/video/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://joreteg.com/blog/betting-on-the-web", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://stratechery.com/2017/the-lessons-and-questions-of-the-iphone-x-and-the-iphone-8/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/Fired4Truth/status/908016532835287040", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/okSuse/status/907488292194660352/photo/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/Mikel_Jollett/status/907314606833516544/video/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://www.thedailybeast.com/exclusive-russia-used-facebook-events-to-organize-anti-immigrant-rallies-on-us-soil", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://theintercept.com/2017/09/11/make-mark-zuckerberg-testify/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/i/web/status/907622761786253312", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/RespectableLaw/status/907360800326774784/photo/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://krebsonsecurity.com/2017/09/the-equifax-breach-what-you-should-know/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.nytimes.com/2017/09/13/magazine/rt-sputnik-and-russias-new-theory-of-war.html", "tags": ['IFTTT', 'Pocket', 'instapaper']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://replicationindex.wordpress.com/2017/02/02/reconstruction-of-a-train-wreck-how-priming-research-went-of-the-rails/#comment-1454", "tags": ['psychology', 'thinkingfastandslow', 'danielkahneman', 'metascience', 'takedowns', 'awesome']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/fet_complains/status/908066282485956608/photo/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/StigAbell/status/907233394672762881/photo/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/i/web/status/907980368917151744", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/JonyIveParody/status/907940596702220290/photo/1", "tags": ['OneMoreThing']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://arstechnica.com/information-technology/2017/09/bluetooth-bugs-open-billions-of-devices-to-attacks-no-clicking-required/", "tags": ['security', 'mobile']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://makezine.com/2017/09/07/secure-your-raspberry-pi-against-attackers/", "tags": ['rpi', 'security']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.dataquest.io/blog/making-538-plots/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.washingtonpost.com/lifestyle/style/facebooks-role-in-trumps-win-is-clear-no-matter-what-mark-zuckerberg-says/2017/09/07/b5006c1c-93c7-11e7-89fa-bb822a46da5b_story.html", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://www.core-econ.org/the-economy/", "tags": ['book', 'online', 'economics', 'education']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/davidgura/status/907242147027582977", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://developer.apple.com/ios/human-interface-guidelines/overview/themes/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/i/web/status/907323903890128896", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.theatlantic.com/magazine/archive/2017/10/the-first-white-president-ta-nehisi-coates/537909/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/goodmanw/status/907955431737139200/photo/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://xkcd.com/1888/", "tags": ['LECTURAS', 'FEEDLY']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://www.politico.com/story/2017/09/11/facebook-fake-news-fact-checks-242567", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/harrytuckerr/status/907102518504693761/photo/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://www.core-econ.org/the-economy/book/text/0-3-contents.html", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.reddit.com/r/YouShouldKnow/comments/6znofc/ysk_what_your_options_for_responding_to_equifax/", "tags": ['credit', 'freeze', 'equifax']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://danielfm.me/posts/painless-nginx-ingress.html", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://www.cincinnati.com/pages/interactives/seven-days-of-heroin-epidemic-cincinnati/?from=global&sessionKey=&autologin=", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/todbot/status/907335250195374081/photo/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.macstories.net/news/itunes-removes-the-app-store-and-more-to-focus-on-music-movies-tv-shows-podcasts-and-audiobooks/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://fladdict.net/blog/2017/09/iphonex.html", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.macstories.net/news/iphone-8-and-iphone-x-the-macstories-overview/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://theintercept.com/2017/09/12/in-surprise-vote-house-passes-amendment-to-restrict-asset-forfeiture/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/cabel/status/907827853554720768/photo/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://github.com/mplewis/src2png", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/dallasgoldtooth/status/907110216612941824", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://paulgraham.com/sun.html", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://daringfireball.net/2017/09/welcome_to_the_steve_jobs_theater", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://deque.blog/2017/09/13/monoids-what-they-are-why-they-are-useful-and-what-they-teach-us-about-software/", "tags": ['monoid']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://twitter.com/danielradosh/status/907983580462186496/photo/1", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://abcnews.go.com/Politics/treasury-secretary-mnuchin-requested-government-jet-european-honeymoon/story?id=49777076", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://blogs.dropbox.com/tech/2017/09/optimizing-web-servers-for-high-throughput-and-low-latency/", "tags": ['']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "http://www.politico.com/agenda/story/2017/09/13/food-nutrients-carbon-dioxide-000511", "tags": ['Department:Global.Health', 'Politico', '!UWitM', '2017', 'Ebi.Kristie', 'UW:Medicine', 'School:Public.Health']}, created_at="2017-09-14T14:12:01Z"),
        create_bookmark({"link": "https://www.armis.com/blueborne/", "tags": ['security', 'android', 'bluebourne', 'bluetooth', 'iot']}, created_at="2017-09-14T14:12:01Z"),
    ]


def test_bookmark(loop):
    bm = BookmarkManager(InMemoryStorage())
    bm.add_collection('all', AllBookmarks())
    bm.add_collection('tagged', TaggedBookmarks())
    bookmarks = create_bookmarks()
    for i in bookmarks:
        loop.run_until_complete(bm.add_item(i))

    resp = loop.run_until_complete(bm.get_items_for_collection('all', max_keys=10))
    assert 'items' in resp
    assert len(resp['items']) == 10
    links = [x['link'] for x in resp['items']]
    assert 'http://aftertheflood.co/projects/atf-spark' in links
